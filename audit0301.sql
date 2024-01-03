-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: auditmodule
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `audit`
--

DROP TABLE IF EXISTS `audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit` (
  `Audit_ID` int NOT NULL,
  `Auditor_ID` int NOT NULL,
  `Survey_ID` int NOT NULL,
  `Audit_Content` varchar(255) DEFAULT NULL,
  `Audit_Start_Date` date DEFAULT NULL,
  `Audit_End_Date` date DEFAULT NULL,
  PRIMARY KEY (`Audit_ID`),
  KEY `fk_Audit_Auditor1_idx` (`Auditor_ID`),
  KEY `fk_Audit_Survey1_idx` (`Survey_ID`),
  CONSTRAINT `fk_Audit_Auditor1` FOREIGN KEY (`Auditor_ID`) REFERENCES `auditor` (`Auditor_ID`),
  CONSTRAINT `fk_Audit_Survey1` FOREIGN KEY (`Survey_ID`) REFERENCES `survey` (`Survey_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit`
--

LOCK TABLES `audit` WRITE;
/*!40000 ALTER TABLE `audit` DISABLE KEYS */;
INSERT INTO `audit` VALUES (1,1,1,'Quarterly Audit','2023-03-01','2023-03-15'),(2,2,1,'Annual Compliance Check','2023-05-01','2023-05-10'),(3,3,1,'Quality Assurance Audit','2023-07-01','2023-07-15');
/*!40000 ALTER TABLE `audit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit_manager`
--

DROP TABLE IF EXISTS `audit_manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_manager` (
  `Audit_Manager_ID` int NOT NULL,
  `Audit_Manager_Name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Audit_Manager_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_manager`
--

LOCK TABLES `audit_manager` WRITE;
/*!40000 ALTER TABLE `audit_manager` DISABLE KEYS */;
INSERT INTO `audit_manager` VALUES (1,'Michael Johnson'),(2,'Emily Davis'),(3,'Daniel Smith');
/*!40000 ALTER TABLE `audit_manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit_note`
--

DROP TABLE IF EXISTS `audit_note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_note` (
  `Audit_Note_ID` int NOT NULL AUTO_INCREMENT,
  `Public_Note` text,
  `Private_Note` text,
  `Survey_Respond_ID` int NOT NULL,
  `Audit_ID` int NOT NULL,
  PRIMARY KEY (`Audit_Note_ID`),
  KEY `fk_Audit_Note_survey_respond1_idx` (`Survey_Respond_ID`),
  KEY `fk_Audit_Note_audit1_idx` (`Audit_ID`),
  CONSTRAINT `fk_Audit_Note_audit1` FOREIGN KEY (`Audit_ID`) REFERENCES `audit` (`Audit_ID`),
  CONSTRAINT `fk_Audit_Note_survey_respond1` FOREIGN KEY (`Survey_Respond_ID`) REFERENCES `survey_respond` (`Survey_Respond_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_note`
--

LOCK TABLES `audit_note` WRITE;
/*!40000 ALTER TABLE `audit_note` DISABLE KEYS */;
/*!40000 ALTER TABLE `audit_note` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit_team`
--

DROP TABLE IF EXISTS `audit_team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_team` (
  `Audit_Manager_ID` int NOT NULL,
  `Audit_ID` int NOT NULL,
  `Auditor_ID` int NOT NULL,
  PRIMARY KEY (`Audit_Manager_ID`,`Audit_ID`,`Auditor_ID`),
  KEY `fk_Audit_Team_Audit_Manager1_idx` (`Audit_Manager_ID`),
  KEY `fk_Audit_Team_Audit1_idx` (`Audit_ID`),
  KEY `fk_Audit_Team_Auditor1_idx` (`Auditor_ID`),
  CONSTRAINT `fk_Audit_Team_Audit1` FOREIGN KEY (`Audit_ID`) REFERENCES `audit` (`Audit_ID`),
  CONSTRAINT `fk_Audit_Team_Audit_Manager1` FOREIGN KEY (`Audit_Manager_ID`) REFERENCES `audit_manager` (`Audit_Manager_ID`),
  CONSTRAINT `fk_Audit_Team_Auditor1` FOREIGN KEY (`Auditor_ID`) REFERENCES `auditor` (`Auditor_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_team`
--

LOCK TABLES `audit_team` WRITE;
/*!40000 ALTER TABLE `audit_team` DISABLE KEYS */;
INSERT INTO `audit_team` VALUES (1,1,1),(2,2,2),(3,3,3);
/*!40000 ALTER TABLE `audit_team` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auditee`
--

DROP TABLE IF EXISTS `auditee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auditee` (
  `Auditee_ID` int NOT NULL,
  `Auditee_Name` varchar(45) DEFAULT NULL,
  `Auditee_Age` int DEFAULT NULL,
  `Auditee_Department` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Auditee_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auditee`
--

LOCK TABLES `auditee` WRITE;
/*!40000 ALTER TABLE `auditee` DISABLE KEYS */;
INSERT INTO `auditee` VALUES (1,'Alice Johnson',28,'Sales'),(2,'Bob Smith',35,'Marketing'),(3,'Eva Martinez',30,'Customer Support'),(4,'Sophia Clark',25,'HR'),(5,'Noah Gonzalez',32,'Finance'),(6,'Isabella Allen',27,'Operations'),(7,'Liam Carter',29,'IT'),(8,'Mia Perez',26,'Marketing'),(9,'Alexander Wright',31,'Sales'),(10,'Harper King',28,'Customer Support');
/*!40000 ALTER TABLE `auditee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auditor`
--

DROP TABLE IF EXISTS `auditor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auditor` (
  `Auditor_ID` int NOT NULL,
  `Auditor_Name` varchar(45) DEFAULT NULL,
  `Auditor_Email` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Auditor_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auditor`
--

LOCK TABLES `auditor` WRITE;
/*!40000 ALTER TABLE `auditor` DISABLE KEYS */;
INSERT INTO `auditor` VALUES (1,'Sarah Johnson','sarah@example.com'),(2,'David Lee','david@example.com'),(3,'Jennifer Miller','jennifer@example.com'),(4,'Rachel Adams','rachel@example.com'),(5,'Kevin Wilson','kevin@example.com'),(6,'Olivia Garcia','olivia@example.com'),(7,'William Martinez','william@example.com'),(8,'Emma Hernandez','emma@example.com'),(9,'James Turner','james@example.com'),(10,'Ava Cooper','ava@example.com');
/*!40000 ALTER TABLE `auditor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meeting`
--

DROP TABLE IF EXISTS `meeting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meeting` (
  `Meeting_ID` int NOT NULL,
  `Meeting_Content` varchar(255) DEFAULT NULL,
  `Meeting_Time` datetime DEFAULT NULL,
  `Auditee_ID` int NOT NULL,
  `Audit_ID` int NOT NULL,
  `Auditor_ID` int NOT NULL,
  `Meeting_Status` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Meeting_ID`),
  KEY `fk_Meeting_Auditee1_idx` (`Auditee_ID`),
  KEY `fk_Meeting_Audit1_idx` (`Audit_ID`),
  KEY `fk_Meeting_Auditor1_idx` (`Auditor_ID`),
  CONSTRAINT `fk_Meeting_Audit1` FOREIGN KEY (`Audit_ID`) REFERENCES `audit` (`Audit_ID`),
  CONSTRAINT `fk_Meeting_Auditee1` FOREIGN KEY (`Auditee_ID`) REFERENCES `auditee` (`Auditee_ID`),
  CONSTRAINT `fk_Meeting_Auditor1` FOREIGN KEY (`Auditor_ID`) REFERENCES `auditor` (`Auditor_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meeting`
--

LOCK TABLES `meeting` WRITE;
/*!40000 ALTER TABLE `meeting` DISABLE KEYS */;
INSERT INTO `meeting` VALUES (1,'Quarterly Review Meeting','2023-03-05 09:00:00',1,1,1,'Waiting'),(2,'Compliance Discussion','2023-05-10 14:30:00',2,2,2,'Confirm'),(3,'Quality Assurance Meeting','2023-07-15 11:00:00',3,3,3,'Processing'),(4,'Finised Meeting','2024-01-02 00:00:00',4,1,1,'Finished');
/*!40000 ALTER TABLE `meeting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meeting_note`
--

DROP TABLE IF EXISTS `meeting_note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meeting_note` (
  `Survey_Respond_ID` int NOT NULL,
  `Audit_ID` int NOT NULL,
  `Meeting_ID` int NOT NULL,
  `Note_Content` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Survey_Respond_ID`,`Audit_ID`,`Meeting_ID`),
  KEY `fk_Audit_Note_Survey_Respond1_idx` (`Survey_Respond_ID`),
  KEY `fk_Audit_Note_Audit1_idx` (`Audit_ID`),
  KEY `fk_Audit_Note_Meeting1_idx` (`Meeting_ID`),
  CONSTRAINT `fk_Meeeting_Note_Survey_Respond1` FOREIGN KEY (`Survey_Respond_ID`) REFERENCES `survey_respond` (`Survey_Respond_ID`),
  CONSTRAINT `fk_Meeting_Note_Audit1` FOREIGN KEY (`Audit_ID`) REFERENCES `audit` (`Audit_ID`),
  CONSTRAINT `fk_Meeting_Note_Meeting1` FOREIGN KEY (`Meeting_ID`) REFERENCES `meeting` (`Meeting_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meeting_note`
--

LOCK TABLES `meeting_note` WRITE;
/*!40000 ALTER TABLE `meeting_note` DISABLE KEYS */;
INSERT INTO `meeting_note` VALUES (1,1,1,'Okay'),(2,2,2,'Bad'),(3,3,3,'Good'),(109,1,1,'Positive feedback received'),(112,2,2,'Needs improvement in training programs'),(115,3,3,'Further discussions required'),(118,1,1,'Satisfactory work-life balance'),(121,2,2,'Requires attention to reduce stress'),(124,3,3,'Improvement needed in flexible work hours');
/*!40000 ALTER TABLE `meeting_note` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question` (
  `Question_ID` int NOT NULL,
  `Survey_ID` int NOT NULL,
  `Question_Text` text,
  `Question_Category` varchar(45) DEFAULT NULL,
  `Option` json DEFAULT NULL,
  PRIMARY KEY (`Question_ID`),
  KEY `fk_Question_Survey1_idx` (`Survey_ID`),
  CONSTRAINT `fk_Question_Survey1` FOREIGN KEY (`Survey_ID`) REFERENCES `survey` (`Survey_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES (1,1,'How satisfied are you with the work environment?','Work Environment Satisfaction','{\"Options\": [\"Very Satisfied\", \"Satisfied\", \"Neutral\", \"Dissatisfied\", \"Very Dissatisfied\"]}'),(2,1,'Do you feel valued in the workplace?','Employee Value','{\"Options\": [\"Yes\", \"No\"]}'),(3,1,'Are you satisfied with the communication within the team?','Team Communication Satisfaction','{\"Options\": [\"Highly Satisfied\", \"Satisfied\", \"Neutral\", \"Dissatisfied\", \"Highly Dissatisfied\"]}'),(4,2,'How motivated are you in your role?','Employee Motivation','{\"Options\": [\"Highly Motivated\", \"Motivated\", \"Neutral\", \"Demotivated\", \"Highly Demotivated\"]}'),(5,2,'Does the company provide adequate training opportunities?','Training Satisfaction','{\"Options\": [\"Yes\", \"No\"]}'),(6,2,'Do you feel recognized for your contributions?','Employee Recognition','{\"Options\": [\"Strongly Agree\", \"Agree\", \"Neutral\", \"Disagree\", \"Strongly Disagree\"]}'),(7,3,'Are you able to maintain a healthy work-life balance?','Work-Life Balance','{\"Options\": [\"Yes, consistently\", \"Most of the time\", \"Sometimes\", \"Rarely\", \"Never\"]}'),(8,3,'Does the company support flexible working hours?','Flexible Work Hours Support','{\"Options\": [\"Strongly Support\", \"Support\", \"Neutral\", \"Oppose\", \"Strongly Oppose\"]}'),(9,3,'Do you feel stressed due to work demands?','Work-Related Stress','{\"Options\": [\"Not at all\", \"A little\", \"Moderately\", \"Very much\", \"Extremely\"]}');
/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `survey`
--

DROP TABLE IF EXISTS `survey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `survey` (
  `Survey_ID` int NOT NULL,
  `Survey_Title` varchar(45) DEFAULT NULL,
  `Survey_Description` varchar(45) DEFAULT NULL,
  `Survey_Start_Date` datetime DEFAULT NULL,
  `Survey_End_Date` datetime DEFAULT NULL,
  `Survey_Status` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Survey_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `survey`
--

LOCK TABLES `survey` WRITE;
/*!40000 ALTER TABLE `survey` DISABLE KEYS */;
INSERT INTO `survey` VALUES (1,'Employee Feedback Survey','Gathering feedback from employees','2023-01-01 00:00:00','2023-01-31 00:00:00','Processing'),(2,'Employee Engagement Survey','Measuring employee engagement levels','2023-04-01 00:00:00','2023-04-30 00:00:00','New'),(3,'Work-Life Balance Survey','Assessing work-life balance satisfaction','2023-06-01 00:00:00','2023-06-30 00:00:00','Audited'),(4,'New Survey Title','New Survey Description','2024-01-01 00:00:00','2024-01-31 00:00:00','Processing');
/*!40000 ALTER TABLE `survey` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `survey_respond`
--

DROP TABLE IF EXISTS `survey_respond`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `survey_respond` (
  `Survey_Respond_ID` int NOT NULL,
  `Survey_ID` int NOT NULL,
  `Auditee_ID` int NOT NULL,
  `Question_ID` int NOT NULL,
  `Answer_Text` text,
  PRIMARY KEY (`Survey_Respond_ID`),
  KEY `fk_Survey_Respond_Survey_idx` (`Survey_ID`),
  KEY `fk_Survey_Respond_Auditee1_idx` (`Auditee_ID`),
  KEY `fk_Survey_Respond_Question1_idx` (`Question_ID`),
  CONSTRAINT `fk_Survey_Respond_Auditee1` FOREIGN KEY (`Auditee_ID`) REFERENCES `auditee` (`Auditee_ID`),
  CONSTRAINT `fk_Survey_Respond_Question1` FOREIGN KEY (`Question_ID`) REFERENCES `question` (`Question_ID`),
  CONSTRAINT `fk_Survey_Respond_Survey` FOREIGN KEY (`Survey_ID`) REFERENCES `survey` (`Survey_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `survey_respond`
--

LOCK TABLES `survey_respond` WRITE;
/*!40000 ALTER TABLE `survey_respond` DISABLE KEYS */;
INSERT INTO `survey_respond` VALUES (1,1,1,1,'Very Satisfied'),(2,1,1,2,'Yes'),(3,1,1,3,'Highly Satisfied'),(4,1,2,1,'Satisfied'),(5,1,2,2,'Yes'),(6,1,2,3,'Satisfied'),(7,1,3,1,'Neutral'),(8,1,3,2,'No'),(9,1,3,3,'Neutral'),(10,1,4,1,'Satisfied'),(11,1,4,2,'Yes'),(12,1,4,3,'Neutral'),(13,1,5,1,'Neutral'),(14,1,5,2,'No'),(15,1,5,3,'Neutral'),(16,1,6,1,'Very Satisfied'),(17,1,6,2,'Yes'),(18,1,6,3,'Highly Satisfied'),(19,1,7,1,'Very Dissatisfied'),(20,1,7,2,'No'),(21,1,7,3,'Dissatisfied'),(22,1,8,1,'Dissatisfied'),(23,1,8,2,'No'),(24,1,8,3,'Neutral'),(25,1,9,1,'Neutral'),(26,1,9,2,'Yes'),(27,1,9,3,'Neutral'),(28,1,10,1,'Satisfied'),(29,1,10,2,'Yes'),(30,1,10,3,'Satisfied'),(109,2,1,4,'Highly Motivated'),(110,2,1,5,'Yes'),(111,2,1,6,'Strongly Agree'),(112,2,2,4,'Motivated'),(113,2,2,5,'No'),(114,2,2,6,'Neutral'),(115,2,3,4,'Demotivated'),(116,2,3,5,'Yes'),(117,2,3,6,'Disagree'),(118,3,1,7,'Yes, consistently'),(119,3,1,8,'Strongly Support'),(120,3,1,9,'Not at all'),(121,3,2,7,'Most of the time'),(122,3,2,8,'Support'),(123,3,2,9,'A little'),(124,3,3,7,'Sometimes'),(125,3,3,8,'Neutral'),(126,3,3,9,'Moderately');
/*!40000 ALTER TABLE `survey_respond` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-03 17:04:07
