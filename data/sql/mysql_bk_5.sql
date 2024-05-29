-- MariaDB dump 10.19  Distrib 10.8.3-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: testdb
-- ------------------------------------------------------
-- Server version	10.8.3-MariaDB-debug

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `t_7sdcgd`
--

DROP TABLE IF EXISTS `t_7sdcgd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_7sdcgd` (
  `wkey` int(11) DEFAULT NULL,
  `pkey` int(11) NOT NULL,
  `c_9r_tqc` double DEFAULT NULL,
  `c_ziole` int(11) DEFAULT NULL,
  `c_2i67t` double DEFAULT NULL,
  `c_ql_o2` text DEFAULT NULL,
  PRIMARY KEY (`pkey`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_7sdcgd`
--

LOCK TABLES `t_7sdcgd` WRITE;
/*!40000 ALTER TABLE `t_7sdcgd` DISABLE KEYS */;
INSERT INTO `t_7sdcgd` VALUES
(1,11000,35.14,61,47.23,'1xqweb'),
(1,12000,NULL,51,28.8,'eg5h5d'),
(1,13000,71.84,25,82.39,'kzfxxc'),
(1,14000,3.71,76,98.81,'n2544d'),
(1,15000,64.55,72,NULL,'gjcvo'),
(2,16000,91.16,49,NULL,'bzbjhb'),
(2,17000,74.11,81,NULL,'h6soib'),
(2,18000,7.48,43,NULL,NULL),
(2,19000,14.84,75,NULL,'iifhc'),
(7,42000,NULL,33,85.1,'uq2pcd'),
(7,43000,NULL,34,74.86,'lidfl'),
(7,44000,NULL,17,41.33,'xflpn'),
(7,45000,NULL,42,17.61,'4pi57c'),
(8,46000,48.99,44,NULL,NULL),
(8,47000,40.79,73,NULL,NULL),
(8,48000,31.81,76,17.73,NULL),
(8,49000,12.25,25,76.2,NULL),
(8,50000,73.84,60,98.78,NULL),
(8,51000,100.21,25,55.93,NULL),
(8,52000,50.85,84,48.7,NULL),
(11,63000,74.26,68,24.46,'z0swrb'),
(11,64000,95.69,56,38.7,NULL),
(11,65000,36.58,66,NULL,'2y1cdc'),
(11,66000,63.31,61,44.82,NULL),
(11,67000,16.23,34,91.29,'qgwttd'),
(11,68000,NULL,63,29.63,'fhtpec'),
(11,69000,27.41,9,37.2,'4wx7bc'),
(11,70000,42.63,98,100.96,'mlxx5c'),
(13,77000,11.67,30,72.75,'j9w37b'),
(13,78000,NULL,18,11.8,NULL),
(13,79000,97.33,68,80.17,NULL);
/*!40000 ALTER TABLE `t_7sdcgd` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_euhshb`
--

DROP TABLE IF EXISTS `t_euhshb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_euhshb` (
  `wkey` int(11) DEFAULT NULL,
  `pkey` int(11) NOT NULL,
  `c_vjmlyd` text DEFAULT NULL,
  `c_0ebuz` int(11) DEFAULT NULL,
  `c_yhipfc` int(11) DEFAULT NULL,
  `c_qzu9zd` double DEFAULT NULL,
  `c_oyg4yd` int(11) DEFAULT NULL,
  `c_hwgpdd` double DEFAULT NULL,
  `c_obioac` int(11) DEFAULT NULL,
  `c_wdjd7` text DEFAULT NULL,
  PRIMARY KEY (`pkey`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_euhshb`
--

LOCK TABLES `t_euhshb` WRITE;
/*!40000 ALTER TABLE `t_euhshb` DISABLE KEYS */;
INSERT INTO `t_euhshb` VALUES
(3,20000,'mlq__c',85,28,75.25,62,33.17,18,'2sbob'),
(3,21000,'4uk8ib',87,44,51.12,37,27.74,60,'jklwcc'),
(3,22000,'t_mptd',47,72,63.87,100,NULL,77,'wi6gzd'),
(3,23000,'o9l70',17,66,49.48,100,30.26,6,'xtntyd'),
(3,24000,'oktybd',61,99,65.42,57,44.3,84,NULL),
(4,25000,'clqprd',82,28,30.99,62,27.81,73,NULL),
(4,26000,'uabykc',86,71,99.4,48,5.92,85,NULL),
(4,27000,NULL,31,56,NULL,20,4.62,59,NULL),
(4,28000,'crtnud',31,73,22.35,65,34.73,50,NULL),
(4,29000,'sgg__c',93,46,21.96,9,82.97,28,NULL),
(4,30000,'bcp4xb',97,39,96.13,81,22.55,67,NULL),
(4,31000,NULL,89,55,12.36,16,41.75,81,NULL),
(5,32000,NULL,83,NULL,81.94,NULL,NULL,60,NULL),
(5,33000,NULL,75,NULL,22.3,NULL,31.59,3,'lgidyb'),
(5,34000,NULL,70,NULL,79.15,NULL,96.1,16,'djz2eb'),
(5,35000,NULL,52,NULL,39.56,NULL,15.4,63,'xsektd'),
(5,36000,NULL,73,NULL,83.56,NULL,84.38,23,'gwdg0c'),
(5,37000,NULL,62,NULL,33.41,NULL,17.49,97,'tcuxeb'),
(6,38000,NULL,30,NULL,22.38,93,82.86,100,'fuytdc'),
(6,39000,NULL,99,NULL,50.72,16,25.22,64,'hwptmc'),
(6,40000,NULL,99,NULL,10.84,28,36.34,55,'c01dub'),
(6,41000,NULL,89,NULL,12.3,47,72.88,69,'db9mm'),
(9,53000,'upcf8c',64,10,5.37,35,6.81,86,'vw7xrc'),
(9,54000,'msw1hc',82,2,90.2,64,44.52,20,'k1havb'),
(9,55000,'c6yei',13,65,NULL,14,95.9,93,'i3ckrd'),
(9,56000,'bdgvec',96,54,97.67,96,52.3,89,'hnxb8b'),
(9,57000,'p691ed',57,58,47.44,25,5.31,1,'18ikud'),
(9,58000,'fbu1pb',88,49,43.57,35,47.3,44,'8w0sbb'),
(10,59000,'47bxjc',37,NULL,18.32,31,40.18,39,'feogod'),
(10,60000,'ydcsxb',30,NULL,78.32,25,56.17,34,'f_2u_'),
(10,61000,'kibimb',64,NULL,78.39,29,4.58,77,'m8nlqd'),
(10,62000,NULL,42,NULL,82.81,69,16.6,25,'oikowc'),
(12,71000,NULL,NULL,9,NULL,18,90.1,28,'zht3bc'),
(12,72000,NULL,NULL,27,93.2,12,58.33,27,'rdq_l'),
(12,73000,NULL,NULL,63,37.67,34,75.63,84,'tz5evc'),
(12,74000,NULL,NULL,4,18.3,54,89.57,5,NULL),
(12,75000,NULL,NULL,50,NULL,87,91.4,21,'r9uynb'),
(12,76000,NULL,NULL,89,2.27,25,9.94,67,NULL),
(14,80000,NULL,NULL,1,64.92,59,69.67,83,NULL),
(14,81000,NULL,NULL,82,89.7,16,55.32,85,NULL),
(14,82000,NULL,NULL,28,2147483648.1,80,2.34,76,NULL);
/*!40000 ALTER TABLE `t_euhshb` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-23 16:56:02
