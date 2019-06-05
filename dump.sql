-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: 127.0.0.1    Database: teamupdb
-- ------------------------------------------------------
-- Server version	5.5.62

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `Adminaccount` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  PRIMARY KEY (`Adminaccount`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `class` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `limit` int(11) NOT NULL,
  `creater` varchar(255) NOT NULL,
  `pwd` varchar(255) NOT NULL,
  `intro` varchar(511) DEFAULT NULL,
  `teacher` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_class_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES ('1','wer',123,'oGWOa5W0W04J5rKEzODc7wVcvWfY','34234','erwe','qwe'),('2','yyy',5,'oGWOa5W0W04J5rKEzODc7wVcvWfY','12345','qwer','aaa');
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;



--
-- Table structure for table `invite_request`
--

DROP TABLE IF EXISTS `invite_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `invite_request` (
  `invite_request_id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` varchar(255) DEFAULT NULL,
  `guest_id` varchar(255) DEFAULT NULL,
  `request_state` int(11) DEFAULT '2',
  `request_read` int(11) DEFAULT '0',
  PRIMARY KEY (`invite_request_id`),
  KEY `guest_id` (`guest_id`),
  KEY `team_id` (`team_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invite_request`
--

LOCK TABLES `invite_request` WRITE;
/*!40000 ALTER TABLE `invite_request` DISABLE KEYS */;
INSERT INTO `invite_request` VALUES (1,'001','1',0,1),(2,'002','1',0,1),(3,'17','11111',2,0);
/*!40000 ALTER TABLE `invite_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `join_request`
--

DROP TABLE IF EXISTS `join_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `join_request` (
  `join_request_id` int(11) NOT NULL AUTO_INCREMENT,
  `applicant_id` varchar(255) DEFAULT NULL,
  `team_id` varchar(255) DEFAULT NULL,
  `request_state` int(11) DEFAULT NULL,
  `request_read` int(11) DEFAULT '0',
  PRIMARY KEY (`join_request_id`),
  KEY `applicant_id` (`applicant_id`),
  KEY `team_id` (`team_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `join_request`
--

LOCK TABLES `join_request` WRITE;
/*!40000 ALTER TABLE `join_request` DISABLE KEYS */;
INSERT INTO `join_request` VALUES (1,'001','001',0,1),(2,'oGWOa5W0W04J5rKEzODc7wVcvWfY','13',2,0),(3,'oGWOa5W0W04J5rKEzODc7wVcvWfY','13',2,0),(4,'oGWOa5W0W04J5rKEzODc7wVcvWfY','1',2,0),(5,'oGWOa5W0W04J5rKEzODc7wVcvWfY','16',2,0),(6,'oGWOa5W0W04J5rKEzODc7wVcvWfY','16',2,0),(7,'oGWOa5W0W04J5rKEzODc7wVcvWfY','1',2,0),(8,'oGWOa5W0W04J5rKEzODc7wVcvWfY','13',2,0);
/*!40000 ALTER TABLE `join_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `SNo` varchar(255) NOT NULL,
  `Project` varchar(255) DEFAULT NULL,
  `Award` varchar(255) DEFAULT NULL,
  `Code` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `ix_project_SNo` (`SNo`),
  CONSTRAINT `project_ibfk_1` FOREIGN KEY (`SNo`) REFERENCES `student` (`SNo`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `SNo` varchar(255) NOT NULL,
  `Avatar` varchar(255) DEFAULT NULL,
  `SName` varchar(255) NOT NULL,
  `Grade` varchar(255) NOT NULL,
  `Group` varchar(255) NOT NULL,
  `Telephone` varchar(255) DEFAULT NULL,
  `WeChat` varchar(255) DEFAULT NULL,
  `QQ` varchar(255) DEFAULT NULL,
  `MailBox` varchar(255) DEFAULT NULL,
  `Other` varchar(255) DEFAULT NULL,
  `Occupation` varchar(255) DEFAULT NULL,
  `WorkAddress` varchar(255) DEFAULT NULL,
  `Direction` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`SNo`),
  KEY `ix_student_SNo` (`SNo`),
  KEY `ix_student_Avatar` (`Avatar`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team`
--

DROP TABLE IF EXISTS `team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team` (
  `id` varchar(255) NOT NULL,
  `cap` varchar(255) DEFAULT NULL,
  `class_id` varchar(255) DEFAULT NULL,
  `full` int(11) DEFAULT NULL,
  `msg` varchar(255) DEFAULT NULL,
  `leader_id` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cap` (`cap`),
  KEY `class_id` (`class_id`),
  KEY `ix_team_id` (`id`),
  CONSTRAINT `team_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `class` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team`
--

LOCK TABLES `team` WRITE;
/*!40000 ALTER TABLE `team` DISABLE KEYS */;
INSERT INTO `team` VALUES ('1','3','1',0,'234','11111'),('12','2','2',0,'123','oGWOa5W0W04J5rKEzODc7wVcvWfY'),('14','123','2',0,'','2222'),('15','123','2',0,'','3333'),('16','123','1',0,'','11111'),('17','123','1',0,'','5555');
/*!40000 ALTER TABLE `team` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `openId` varchar(255) NOT NULL,
  `Sno` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_users_id` (`openId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('10069','贺潇潇','oGWOa5W0W04J5rKEzODc7wVcvWfY','2016202227'),('123','b','22222','234'),('234','a','11111','123');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;


--
-- Table structure for table `class_has_stu`
--

DROP TABLE IF EXISTS `class_has_stu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `class_has_stu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class_id` varchar(255) DEFAULT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `team_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_class_has_stu_id` (`id`),
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
LOCK TABLES `class_has_stu` WRITE;
/*!40000 ALTER TABLE `class_has_stu` DISABLE KEYS */;
INSERT INTO `class_has_stu` VALUES (1,'1','11111','1'),(2,'1','22222','1'),(5,'1','oGWOa5W0W04J5rKEzODc7wVcvWfY',NULL);
/*!40000 ALTER TABLE `class_has_stu` ENABLE KEYS */;
UNLOCK TABLES;
--
-- Dumping data for table `class_has_stu`
--
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-05  8:55:56
