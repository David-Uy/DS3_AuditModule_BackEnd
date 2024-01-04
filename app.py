from flask import Flask, jsonify
from flask import request
from flask_mysqldb import MySQL
from pyngrok import ngrok
from flask_cors import CORS
from collections import defaultdict
from datetime import datetime


app = Flask(__name__)
CORS(app)

port_no = 5000
ngrok.set_auth_token("2ZqqRwyoNLoM75HBgRnRU2J9VmK_5J47dnupcTMizboiNrzFg")
public_url = ngrok.connect(port_no).public_url
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql@123'
app.config['MYSQL_DB'] = 'auditmodule'

mysql = MySQL(app)
mysql.init_app(app)
@app.route('/')
def note_for_frontend():
    return f"Add / then name of the table you want. E.g. {public_url}/auditors"

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
        cur.execute("SELECT * FROM Survey ORDER BY FIELD(Survey_Status, 'Processing', 'New', 'Audited')")
        data = cur.fetchall()
        cur.close()

        surveys_list = []
        for row in data:
            survey = {
                'Survey_ID': row[0],
                'Survey_Title': row[1],
                'Survey_Description': row[2],
                'Survey_Start_Date': row[3],
                'Survey_End_Date': row[4],
                'Survey_Status': row[5]
                # Add more fields as needed
            }
            surveys_list.append(survey)

        return surveys_list
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
def add_audit():
    try:
        if 'survey_title' not in request.json:
            return jsonify({'error': 'Survey title not provided'}), 400

        # Get survey title from the frontend
        survey_title = request.json.get('survey_title')  # Assuming it's sent in the request body

        # Get current date
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Fetch survey_id based on survey_title
        with app.app_context():
            conn = mysql.connect
            cur = conn.cursor()
        cur.execute("SELECT Survey_ID FROM Survey WHERE Survey_Title = %s", (survey_title,))
        survey_id = cur.fetchone()

        if survey_id:
            # Add new audit with auditor_id = 1 and received survey_id and current date
            cur.execute("""
                INSERT INTO Audit (Auditor_ID, Survey_ID, Start_Date)
                VALUES (1, %s, %s)
            """, (survey_id[0], current_date))
            mysql.connection.commit()
            cur.close()

            return {'message': 'Audit added successfully'}
        else:
            return {'error': 'Survey title not found'}

    except Exception as e:
        return {'error': str(e)}



if __name__ == '__main__':
    app.run(debug=True)

print(f"Please click {public_url}")