import json
from flask import Flask, jsonify
from flask import request
from flask_mysqldb import MySQL
# from pyngrok import ngrok
from flask_cors import CORS
from flask_cors import cross_origin
from collections import defaultdict
from datetime import datetime
# import mysql.connector
import logging

app = Flask(__name__)
CORS(app, origin='*')

# Add this at the beginning of your Flask application
logging.basicConfig(level=logging.DEBUG)

# port_no = 5000
# ngrok.set_auth_token("2ZqqRwyoNLoM75HBgRnRU2J9VmK_5J47dnupcTMizboiNrzFg")
# public_url = ngrok.connect(port_no).public_url
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql@123'
app.config['MYSQL_DB'] = 'auditmodule'

mysql = MySQL(app)
mysql.init_app(app)
# @app.route('/')
# def note_for_frontend():
#     return f"Add / then name of the table you want. E.g. {public_url}/auditors"

@app.get('/auditors')
def get_auditors():
    try:
        with app.app_context():
            conn = mysql.connect
            cur = conn.cursor()
            cur.execute("SELECT * FROM Auditor")
            data = cur.fetchall()
            cur.close()

        auditors_list = []
        for row in data:
            auditor = {
                'Auditor_ID': row[0],
                'Auditor_Name': row[1],
                'Auditor_Email': row[2]
                # Add more fields as needed
            }
            auditors_list.append(auditor)

        return auditors_list
    except Exception as e:
        return [{'error': str(e)}]

@app.get('/members') #same team
def get_auditors_by_auditor_id():
    try:
        with app.app_context():
            conn = mysql.connect
            cur = conn.cursor()

        # Fetch the survey_id associated with the given auditor_id
        cur.execute("SELECT Survey_ID FROM Audit WHERE Auditor_ID = 1")
        survey_id = cur.fetchone()[0]  # Assuming the first result contains the survey_id

        # Fetch auditors who audited the same survey as the given auditor_id
        cur.execute("""
            SELECT DISTINCT a.Auditor_ID, a.Auditor_Name, a.Auditor_Email
            FROM Audit au
            JOIN Auditor a ON au.Auditor_ID = a.Auditor_ID
            WHERE au.Survey_ID = %s AND au.Auditor_ID != 1
        """, (survey_id,))
        data = cur.fetchall()
        cur.close()

        auditors_list = []
        for row in data:
            auditor = {
                'Auditor_ID': row[0],
                'Auditor_Name': row[1],
                'Auditor_Email': row[2]
                # Add more fields as needed
            }
            auditors_list.append(auditor)

        return auditors_list
    except Exception as e:
        return [{'error': str(e)}]

@app.route('/auditees', methods=['GET'])
def get_auditees():
    try:
        with app.app_context():
            conn = mysql.connect
            cur = conn.cursor()
        cur.execute("SELECT * FROM Auditee")
        data = cur.fetchall()
        cur.close()

        auditees_list = []
        for row in data:
            auditee = {
                'Auditee_ID': row[0],
                'Auditee_Name': row[1],
                'Auditee_Age': row[2],
                'Auditee_Department': row[3]
                # Add more fields as needed
            }
            auditees_list.append(auditee)

        return jsonify({'auditees': auditees_list})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/surveys', methods=['GET'])
def get_surveys():
    try:
        with app.app_context():
            conn = mysql.connect
            cur = conn.cursor()

            # Fetch surveys from the Survey table
            cur.execute("SELECT * FROM Survey ORDER BY FIELD(Survey_Status, 'Processing', 'New', 'Audited')")
            data = cur.fetchall()

            for row in data:
                survey_id = row[0]
                cur.execute("SELECT COUNT(*) FROM Audit WHERE Survey_ID = %s", (survey_id,))
                count = cur.fetchone()[0]

                if count > 0:
                    # Check if audit_end_date is set for the survey_id in the Audit table
                    cur.execute("SELECT COUNT(*) FROM Audit WHERE Survey_ID = %s AND audit_end_date IS NOT NULL", (survey_id,))
                    audit_with_end_date = cur.fetchone()[0]

                    if audit_with_end_date > 0:
                        # If audit_end_date is set, update Survey_Status to 'Audited'
                        cur.execute("UPDATE Survey SET Survey_Status = 'Audited' WHERE Survey_ID = %s", (survey_id,))
                    else:
                        # Otherwise, update Survey_Status to 'Processing' if it's 'New'
                        cur.execute("UPDATE Survey SET Survey_Status = 'Processing' WHERE Survey_ID = %s AND Survey_Status = 'New'", (survey_id,))

                    conn.commit()

            # Fetch the updated list of surveys
            cur.execute("SELECT * FROM Survey ORDER BY FIELD(Survey_Status, 'Processing', 'New', 'Audited')")
            updated_data = cur.fetchall()
            cur.close()

            updated_surveys_list = []
            for row in updated_data:
                survey = {
                    'Survey_ID': row[0],
                    'Survey_Title': row[1],
                    'Survey_Description': row[2],
                    'Survey_Start_Date': row[3],
                    'Survey_End_Date': row[4],
                    'Survey_Status': row[5]
                    # Add more fields as needed
                }
                updated_surveys_list.append(survey)

            return updated_surveys_list

    except Exception as e:
        return [{'error': str(e)}]

@app.route('/questions/survey/<int:survey_id>', methods=['GET'])
def get_questions_by_survey_id(survey_id):
    try:
        with app.app_context():
            conn = mysql.connect
            cur = conn.cursor()

        # Fetch survey title and status
        survey_query = "SELECT Survey_Title, Survey_Status FROM survey WHERE Survey_ID = %s"
        cur.execute(survey_query, (survey_id,))
        survey_data = cur.fetchone()

        if survey_data:
            survey_title = survey_data[0]
            survey_status = survey_data[1]

            # Fetch questions and user responses
            question_query = "SELECT Question_ID, Question_Text FROM question WHERE Survey_ID = %s"
            cur.execute(question_query, (survey_id,))
            questions_data = cur.fetchall()

            questions_list = []
            for question_row in questions_data:
                question_id = question_row[0]
                question_text = question_row[1]

                # Fetch user responses for each question
                user_response_query = "SELECT Answer_Text FROM survey_respond WHERE Question_ID = %s"
                cur.execute(user_response_query, (question_id,))
                user_responses_data = cur.fetchall()

                # Count occurrences of each response
                response_count = defaultdict(int)
                for user_response_row in user_responses_data:
                    response = user_response_row[0]
                    response_count[response] += 1

                user_responses_list = [
                    {'response': response, 'count': count}
                    for response, count in response_count.items()
                ]

                question_data = {
                    'question_id': question_id,
                    'question': question_text,
                    'user_responses': user_responses_list
                }
                questions_list.append(question_data)

            cur.close()

            # Construct the final response
            survey_response = {
                'survey_title': survey_title,
                'survey_status': survey_status,
                'questions': questions_list
            }

            return jsonify(survey_response)
        else:
            return jsonify({'error': 'Survey not found'})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/survey_respond/<int:question_id>', methods=['GET'])
def get_user_responses(question_id):
    try:
        with app.app_context():
            conn = mysql.connect
            cur = conn.cursor()

        # Fetch question text
        question_query = "SELECT Question_Text FROM question WHERE Question_ID = %s"
        cur.execute(question_query, (question_id,))
        question_text = cur.fetchone()

        if question_text:
            # Fetch user responses for the specified question
            user_response_query = """
                SELECT sr.Survey_Respond_ID, a.Auditee_Name, a.Auditee_Age, a.Auditee_Department, sr.Answer_Text
                FROM survey_respond sr
                INNER JOIN auditee a ON sr.Auditee_ID = a.Auditee_ID
                WHERE sr.Question_ID = %s
            """
            cur.execute(user_response_query, (question_id,))
            user_responses_data = cur.fetchall()

            user_responses_list = []
            for user_response_row in user_responses_data:
                respond_id, auditee_name, auditee_age, auditee_department, answer_text = user_response_row

                user_response = {
                    'respond_id': f'{respond_id}',
                    'auditee_name': auditee_name,
                    'auditee_age': auditee_age,
                    'auditee_department': auditee_department,
                    'answer_text': answer_text
                }
                user_responses_list.append(user_response)

            cur.close()

            response_data = {
                'question_id': f'{question_id}',
                'question': question_text[0],
                'user_responses': user_responses_list

            }

            return jsonify(response_data)
        else:
            return jsonify({'error': 'Question not found'})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/add_audit', methods=['POST'])
@cross_origin()
def add_audit():
    try:
        if 'survey_title' not in request.json:
            return jsonify({'error': 'Survey title not provided'}), 400

        # Get survey title from the frontend
        survey_title = request.json.get('survey_title')

        # Get current date
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Establish MySQL connection
        # conn = mysql.connector.connect(
        #     host="your_host",
        #     user="your_username",
        #     password="your_password",
        #     database="your_database"
        # )
        conn=mysql.connect

        # Create a cursor object
        cur = conn.cursor()

        # Get the last audit_id
        cur.execute("SELECT MAX(audit_id) FROM Audit")
        last_audit_id = cur.fetchone()[0]

        # Calculate the new audit_id
        new_audit_id = last_audit_id + 1 if last_audit_id is not None else 1

        # Fetch survey_id based on survey_title
        cur.execute("SELECT Survey_ID FROM Survey WHERE Survey_Title = %s", (survey_title,))
        survey_id = cur.fetchone()

        if survey_id:
            # Add new audit with auditor_id = 1 and received survey_id and current date
            # cur.execute("""
            #     INSERT INTO Audit (audit_id, Auditor_ID, Survey_ID, Audit_Start_Date)
            #     VALUES (%s, 1, %s, %s)
            # """, (new_audit_id, survey_id[0], current_date))

            audit_content = f'Audit - {survey_title}'

            # Add new audit with auditor_id = 1, received survey_id, current date, and updated audit content
            cur.execute("""
                INSERT INTO Audit (audit_id, Auditor_ID, Survey_ID, Audit_Content, Audit_Start_Date)
                VALUES (%s, 1, %s, %s, %s)
            """, (new_audit_id, survey_id[0], audit_content, current_date))


            conn.commit()
            cur.close()
            conn.close()

            return {'message': 'Audit added successfully'}
        else:
            return {'error': 'Survey title not found'}, 404

    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/end_audit', methods=['POST'])
@cross_origin()
def end_audit():
    try:
        if 'survey_title' not in request.json:
            return jsonify({'error': 'Survey title not provided'}), 400

        # Get survey title from the frontend
        survey_title = request.json.get('survey_title')

        # Get current date
        current_date = datetime.now().strftime('%Y-%m-%d')

        conn=mysql.connect

        # Create a cursor object
        cur = conn.cursor()

        # Fetch survey_id based on survey_title
        cur.execute("SELECT Survey_ID FROM Survey WHERE Survey_Title = %s", (survey_title,))
        survey_id = cur.fetchone()

        if survey_id:

            # Update Audit with the found audit_id and set Audit_End_Date to the current date
            cur.execute("""
                UPDATE Audit
                SET Audit_End_Date = %s
                WHERE Survey_ID = %s
            """, (current_date, survey_id))

            conn.commit()
            cur.close()
            conn.close()

            return {'message': 'Audit added successfully'}
        else:
            return {'error': 'Survey title not found'}, 404

    except Exception as e:
        return {'error': str(e)}, 500


@app.route('/add_audit_note', methods=['POST'])
@cross_origin()
def add_audit_note():
    try:
        with app.app_context():
            conn = mysql.connect
            cur = conn.cursor()

        if 'responseId' not in request.json or 'publicNote' not in request.json or 'privateNote' not in request.json:
            return jsonify({'error': 'Survey respond ID, public note, or private note not provided'}), 400

        survey_respond_id = request.json.get('responseId')
        public_note = request.json.get('publicNote')
        private_note = request.json.get('privateNote')
        print(survey_respond_id)

        cur.execute("SELECT Survey_ID FROM survey_respond WHERE Survey_Respond_ID = %s", (survey_respond_id,))
        survey_id = cur.fetchone()

        if survey_id:
            cur.execute("SELECT MAX(Audit_Note_ID) FROM audit_note")
            last_audit_note_id = cur.fetchone()[0]

            new_audit_note_id = last_audit_note_id + 1 if last_audit_note_id is not None else 1

            cur.execute("SELECT Audit_ID FROM audit WHERE Survey_ID = %s AND Auditor_ID = 1", (survey_id,))
            audit_id = cur.fetchone()

            if audit_id:
                cur.execute("""
                    INSERT INTO audit_note (Audit_Note_ID, Public_Note, Private_Note, Survey_Respond_ID, Audit_ID)
                    VALUES (%s, %s, %s, %s, %s)
                """, (new_audit_note_id, public_note, private_note, survey_respond_id, audit_id))

                conn.commit()
                cur.close()
                conn.close()

                return {'message': 'Audit note added successfully'}
            else:
                return jsonify({'error': 'Audit ID not found for the provided Survey ID and Auditor ID'}), 404
        else:
            return jsonify({'error': 'Survey ID not found for the provided Survey Respond ID'}), 404

    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/add_meeting', methods=['POST'])
@cross_origin()
def add_meeting():
    try:
        with app.app_context():
            conn = mysql.connect
            cur = conn.cursor()

            if 'responseIds' not in request.json or 'auditeeId' not in request.json:
                return jsonify({'error': 'Survey respond ID or Auditee_ID not provided'}), 400

            survey_respond_ids = request.json.get('responseIds')
            if not (survey_respond_ids and isinstance(survey_respond_ids, list) and len(survey_respond_ids) > 0):
                return jsonify({'error': 'No valid Survey respond ID provided'}), 400

            respond_id = survey_respond_ids[0]
            auditee_id = request.json.get('auditeeId')
            current_date = datetime.now().strftime('%Y-%m-%d')

            # Fetch the Audit_ID using Survey_Respond_ID
            cur.execute("SELECT Audit_ID FROM audit_note WHERE Survey_Respond_ID = %s", (respond_id,))
            audit_ids = cur.fetchone()
            if not audit_ids:
                return jsonify({'error': 'No Audit_ID found for the given Survey_Respond_ID'}), 404
            audit_id = audit_ids[0]

            # Get the maximum Meeting_ID
            cur.execute("SELECT MAX(Meeting_ID) FROM meeting")
            last_meeting_id = cur.fetchone()[0]

            # Calculate the new Meeting_ID
            new_meeting_id = last_meeting_id + 1 if last_meeting_id is not None else 1

            # Insert a new meeting with the manually incremented Meeting_ID
            insert_query = "INSERT INTO meeting (Meeting_ID, Meeting_Content, Meeting_Time, Auditee_ID, Audit_ID, Auditor_ID, Meeting_Status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur.execute(insert_query,
                        (new_meeting_id, "Meeting content", current_date, auditee_id, audit_id, 1, 'Waiting'))

            conn.commit()
            cur.close()
            conn.close()

            return jsonify({'success': 'Meeting added successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auditor_note_data')
def get_auditor_data():
    try:
        with app.app_context():
            conn = mysql.connect
            cur = conn.cursor()

        cur.execute("""
                        SELECT Audit_Note_ID, Public_Note, Private_Note
                        FROM audit_note
                        WHERE Audit_ID IN (SELECT Audit_ID FROM audit WHERE Auditor_ID = 1)
                    """)
        auditor_notes = cur.fetchall()
        formatted_auditor_notes = [
            {
                "note_id": item[0],
                "public_note": item[1],
                "private_note": item[2]
            }
            for item in auditor_notes
        ]

        cur.execute("""
            SELECT *
            FROM auditee
            WHERE Auditee_ID IN (
                SELECT DISTINCT sr.Auditee_ID
                FROM survey_respond sr
                WHERE sr.Survey_Respond_ID IN (
                    SELECT an.Survey_Respond_ID
                    FROM audit_note an
                )
            )
        """)
        auditees = cur.fetchall()

        formatted_auditees = [
            {
                "auditee_id": item[0],
                "auditee_name": item[1],
                "age": item[2],
                "department": item[3]
            }
            for item in auditees
        ]



        cur.execute("SELECT * FROM question WHERE Survey_ID IN (SELECT Survey_ID FROM audit WHERE Auditor_ID = 1)")
        survey_questions = cur.fetchall()
        formatted_survey_questions = [
            {
                "question_id": item[0],
                "survey_id": item[1],
                "question": item[2]
            }
            for item in survey_questions
        ]



        cur.execute("""
    SELECT sr.*, an.Audit_Note_ID
    FROM survey_respond sr
    JOIN audit_note an ON sr.Survey_Respond_ID = an.Survey_Respond_ID
    WHERE sr.Survey_ID IN (SELECT Survey_ID FROM audit WHERE Auditor_ID = 1)
""")
        survey_responses = cur.fetchall()
        formatted_survey_responses = [
            {
                "response_id": item[0],
                "survey_id": item[1],
                "auditee_id": item[2],
                "question_id": item[3],
                "response": item[4],
                "note_id": item[5]
            }
            for item in survey_responses
        ]

        # Construct response data
        response_data = {
            "survey_responses": formatted_survey_responses,
            "survey_questions": formatted_survey_questions,
            "auditees": formatted_auditees ,
            "auditor_notes": formatted_auditor_notes
        }

        return jsonify(response_data)
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        cur.close()
        conn.close()


@app.route('/meeting/<meeting_status>', methods=['GET'])
def get_meeting_data(meeting_status):
    try:
        with app.app_context():
            conn = mysql.connect
            cur = conn.cursor()

            # Fetching meeting data based on Auditor_ID and Meeting_Status received from the front-end
            cur.execute("""
                SELECT Meeting_ID, Meeting_Content, Meeting_Time, Meeting_Status, Audit_ID
                FROM meeting
                WHERE Auditor_ID = 1 AND Meeting_Status = %s
            """, (meeting_status,))
            meetings = cur.fetchall()

            formatted_meetings = [
                {
                    "meeting_id": item[0],
                    "meeting_content": item[1],
                    "meeting_time": item[2].strftime("%Y-%m-%d %H:%M:%S"),
                    "meeting_status": item[3],
                    "audit_id": item[4]  # Assuming Audit_ID is included in the query result
                }
                for item in meetings
            ]

            cur.execute("""
                        SELECT DISTINCT a.*
                        FROM auditee a
                        JOIN meeting m ON a.Auditee_ID = m.Auditee_ID
                        WHERE m.Meeting_Status = %s
            """, (meeting_status,))

            auditees = cur.fetchall()

            formatted_auditees = [
                {
                    "auditee_id": item[0],
                    "auditee_name": item[1],
                    "age": item[2],
                    "department": item[3]
                }
                for item in auditees
            ]

            cur.execute("SELECT * FROM question WHERE Survey_ID IN (SELECT Survey_ID FROM audit WHERE Auditor_ID = 1)")
            survey_questions = cur.fetchall()
            formatted_survey_questions = [
                {
                    "question_id": item[0],
                    "survey_id": item[1],
                    "question": item[2]
                }
                for item in survey_questions
            ]

            cur.execute("""
                SELECT sr.*, an.Audit_Note_ID
                FROM survey_respond sr
                JOIN audit_note an ON sr.Survey_Respond_ID = an.Survey_Respond_ID
                WHERE sr.Survey_ID IN (SELECT Survey_ID FROM audit WHERE Auditor_ID = 1)
            """)
            survey_responses = cur.fetchall()
            formatted_survey_responses = [
                {
                    "response_id": item[0],
                    "survey_id": item[1],
                    "auditee_id": item[2],
                    "question_id": item[3],
                    "response": item[4],
                    "note_id": item[5]
                }
                for item in survey_responses
            ]

            cur.execute("""
                             SELECT Audit_Note_ID, Public_Note, Private_Note
                             FROM audit_note
                             WHERE Audit_ID IN (SELECT Audit_ID FROM audit WHERE Auditor_ID = 1)
                         """)
            auditor_notes = cur.fetchall()
            formatted_auditor_notes = [
                {
                    "note_id": item[0],
                    "public_note": item[1],
                    "private_note": item[2]
                }
                for item in auditor_notes
            ]
            # Construct response data
            response_data = {
                "meetings": formatted_meetings,
                "auditor_notes": formatted_auditor_notes,
                "auditees": formatted_auditees,
                "survey_questions": formatted_survey_questions,
                "survey_responses": formatted_survey_responses
            }

            return jsonify(response_data)
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)

# print(f"Please click {public_url}")