-- MySQL dump 10.13  Distrib 9.6.0, for macos15.7 (arm64)
--
-- Host: localhost    Database: property_management
-- ------------------------------------------------------
-- Server version	9.7.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '3df11118-4399-11f1-aa6f-659ad65f5ba8:1-2666';

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add 权限',6,'add_permission'),(22,'Can change 权限',6,'change_permission'),(23,'Can delete 权限',6,'delete_permission'),(24,'Can view 权限',6,'view_permission'),(25,'Can add role',7,'add_role'),(26,'Can change role',7,'change_role'),(27,'Can delete role',7,'delete_role'),(28,'Can view role',7,'view_role'),(29,'Can add 菜单',8,'add_menu'),(30,'Can change 菜单',8,'change_menu'),(31,'Can delete 菜单',8,'delete_menu'),(32,'Can view 菜单',8,'view_menu'),(33,'Can add 用户',9,'add_user'),(34,'Can change 用户',9,'change_user'),(35,'Can delete 用户',9,'delete_user'),(36,'Can view 用户',9,'view_user'),(37,'Can add 小区',10,'add_community'),(38,'Can change 小区',10,'change_community'),(39,'Can delete 小区',10,'delete_community'),(40,'Can view 小区',10,'view_community'),(41,'Can add 楼栋',11,'add_building'),(42,'Can change 楼栋',11,'change_building'),(43,'Can delete 楼栋',11,'delete_building'),(44,'Can view 楼栋',11,'view_building'),(45,'Can add 单元',12,'add_unit'),(46,'Can change 单元',12,'change_unit'),(47,'Can delete 单元',12,'delete_unit'),(48,'Can view 单元',12,'view_unit'),(49,'Can add 房屋',13,'add_house'),(50,'Can change 房屋',13,'change_house'),(51,'Can delete 房屋',13,'delete_house'),(52,'Can view 房屋',13,'view_house'),(53,'Can add 业主',14,'add_owner'),(54,'Can change 业主',14,'change_owner'),(55,'Can delete 业主',14,'delete_owner'),(56,'Can view 业主',14,'view_owner'),(57,'Can add 车位',15,'add_parking'),(58,'Can change 车位',15,'change_parking'),(59,'Can delete 车位',15,'delete_parking'),(60,'Can view 车位',15,'view_parking'),(61,'Can add 报修',16,'add_repair'),(62,'Can change 报修',16,'change_repair'),(63,'Can delete 报修',16,'delete_repair'),(64,'Can view 报修',16,'view_repair'),(65,'Can add fee',17,'add_fee'),(66,'Can change fee',17,'change_fee'),(67,'Can delete fee',17,'delete_fee'),(68,'Can view fee',17,'view_fee'),(69,'Can add 公告',18,'add_notice'),(70,'Can change 公告',18,'change_notice'),(71,'Can delete 公告',18,'delete_notice'),(72,'Can view 公告',18,'view_notice'),(73,'Can add operation log',19,'add_operationlog'),(74,'Can change operation log',19,'change_operationlog'),(75,'Can delete operation log',19,'delete_operationlog'),(76,'Can view operation log',19,'view_operationlog'),(77,'Can add login log',20,'add_loginlog'),(78,'Can change login log',20,'change_loginlog'),(79,'Can delete login log',20,'delete_loginlog'),(80,'Can view login log',20,'view_loginlog'),(81,'Can add 车辆',21,'add_car'),(82,'Can change 车辆',21,'change_car'),(83,'Can delete 车辆',21,'delete_car'),(84,'Can view 车辆',21,'view_car'),(85,'Can add 访客',22,'add_visitor'),(86,'Can change 访客',22,'change_visitor'),(87,'Can delete 访客',22,'delete_visitor'),(88,'Can view 访客',22,'view_visitor');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `building`
--

DROP TABLE IF EXISTS `building`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `building` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `code` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `floor_count` int NOT NULL,
  `unit_count` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `community_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `building_code_2139c77a_uniq` (`code`),
  KEY `building_community_id_963d7f7e_fk_community_id` (`community_id`),
  CONSTRAINT `building_community_id_963d7f7e_fk_community_id` FOREIGN KEY (`community_id`) REFERENCES `community` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `building`
--

LOCK TABLES `building` WRITE;
/*!40000 ALTER TABLE `building` DISABLE KEYS */;
INSERT INTO `building` VALUES (1,'1号楼','B001',18,2,'2026-05-29 07:00:08.383917',1),(2,'1栋','BLD0001',30,4,'2026-01-01 09:00:00.000000',1),(3,'2栋','BLD0002',30,4,'2026-01-01 09:00:00.000000',1),(4,'3栋','BLD0003',30,4,'2026-01-01 09:00:00.000000',1),(5,'4栋','BLD0004',30,4,'2026-01-01 09:00:00.000000',1),(6,'5栋','BLD0005',30,4,'2026-01-01 09:00:00.000000',1),(7,'6栋','BLD0006',30,4,'2026-01-01 09:00:00.000000',1),(8,'7栋','BLD0007',30,4,'2026-01-01 09:00:00.000000',1),(9,'8栋','BLD0008',30,4,'2026-01-01 09:00:00.000000',1),(10,'9栋','BLD0009',30,4,'2026-01-01 09:00:00.000000',1),(11,'10栋','BLD0010',30,4,'2026-01-01 09:00:00.000000',1),(12,'1栋','BLD0011',30,4,'2026-01-01 09:00:00.000000',2),(13,'2栋','BLD0012',30,4,'2026-01-01 09:00:00.000000',2),(14,'3栋','BLD0013',30,4,'2026-01-01 09:00:00.000000',2),(15,'4栋','BLD0014',30,4,'2026-01-01 09:00:00.000000',2),(16,'5栋','BLD0015',30,4,'2026-01-01 09:00:00.000000',2),(17,'6栋','BLD0016',30,4,'2026-01-01 09:00:00.000000',2),(18,'7栋','BLD0017',30,4,'2026-01-01 09:00:00.000000',2),(19,'8栋','BLD0018',30,4,'2026-01-01 09:00:00.000000',2),(20,'9栋','BLD0019',30,4,'2026-01-01 09:00:00.000000',2),(21,'10栋','BLD0020',30,4,'2026-01-01 09:00:00.000000',2),(22,'1栋','BLD0021',30,4,'2026-01-01 09:00:00.000000',3),(23,'2栋','BLD0022',30,4,'2026-01-01 09:00:00.000000',3),(24,'3栋','BLD0023',30,4,'2026-01-01 09:00:00.000000',3),(25,'4栋','BLD0024',30,4,'2026-01-01 09:00:00.000000',3),(26,'5栋','BLD0025',30,4,'2026-01-01 09:00:00.000000',3),(27,'6栋','BLD0026',30,4,'2026-01-01 09:00:00.000000',3),(28,'7栋','BLD0027',30,4,'2026-01-01 09:00:00.000000',3),(29,'8栋','BLD0028',30,4,'2026-01-01 09:00:00.000000',3),(30,'9栋','BLD0029',30,4,'2026-01-01 09:00:00.000000',3),(31,'10栋','BLD0030',30,4,'2026-01-01 09:00:00.000000',3),(32,'1栋','BLD0031',30,4,'2026-01-01 09:00:00.000000',4),(33,'2栋','BLD0032',30,4,'2026-01-01 09:00:00.000000',4),(34,'3栋','BLD0033',30,4,'2026-01-01 09:00:00.000000',4),(35,'4栋','BLD0034',30,4,'2026-01-01 09:00:00.000000',4),(36,'5栋','BLD0035',30,4,'2026-01-01 09:00:00.000000',4),(37,'6栋','BLD0036',30,4,'2026-01-01 09:00:00.000000',4),(38,'7栋','BLD0037',30,4,'2026-01-01 09:00:00.000000',4),(39,'8栋','BLD0038',30,4,'2026-01-01 09:00:00.000000',4),(40,'9栋','BLD0039',30,4,'2026-01-01 09:00:00.000000',4),(41,'10栋','BLD0040',30,4,'2026-01-01 09:00:00.000000',4),(42,'1栋','BLD0041',30,4,'2026-01-01 09:00:00.000000',5),(43,'2栋','BLD0042',30,4,'2026-01-01 09:00:00.000000',5),(44,'3栋','BLD0043',30,4,'2026-01-01 09:00:00.000000',5),(45,'4栋','BLD0044',30,4,'2026-01-01 09:00:00.000000',5),(46,'5栋','BLD0045',30,4,'2026-01-01 09:00:00.000000',5),(47,'6栋','BLD0046',30,4,'2026-01-01 09:00:00.000000',5),(48,'7栋','BLD0047',30,4,'2026-01-01 09:00:00.000000',5),(49,'8栋','BLD0048',30,4,'2026-01-01 09:00:00.000000',5),(50,'9栋','BLD0049',30,4,'2026-01-01 09:00:00.000000',5),(51,'10栋','BLD0050',30,4,'2026-01-01 09:00:00.000000',5);
/*!40000 ALTER TABLE `building` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `car`
--

DROP TABLE IF EXISTS `car`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `car` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `plate_no` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `brand` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `color` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `owner_id` bigint NOT NULL,
  `parking_id` bigint DEFAULT NULL,
  `car_type` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `car_owner_id_d38c9ce4_fk_owner_id` (`owner_id`),
  KEY `car_parking_id_73c9773b_fk_parking_id` (`parking_id`),
  CONSTRAINT `car_owner_id_d38c9ce4_fk_owner_id` FOREIGN KEY (`owner_id`) REFERENCES `owner` (`id`),
  CONSTRAINT `car_parking_id_73c9773b_fk_parking_id` FOREIGN KEY (`parking_id`) REFERENCES `parking` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car`
--

LOCK TABLES `car` WRITE;
/*!40000 ALTER TABLE `car` DISABLE KEYS */;
INSERT INTO `car` VALUES (2,'京A12345','特斯拉','白色','2026-06-05 07:06:34.365329',2,5,'monthly','disabled');
/*!40000 ALTER TABLE `car` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `community`
--

DROP TABLE IF EXISTS `community`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `community` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `code` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `address` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `contact_phone` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `contact_name` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `remark` longtext COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `community_name_c343716d_uniq` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `community`
--

LOCK TABLES `community` WRITE;
/*!40000 ALTER TABLE `community` DISABLE KEYS */;
INSERT INTO `community` VALUES (1,'阳光花园','YG001','北京市朝阳区','10000000000','2026-05-29 06:42:20.197981','张三',NULL),(2,'演示小区1','COMM001','北京市演示地址1号','10000000001','2026-01-01 09:00:00.000000','管理员1',''),(3,'演示小区2','COMM002','北京市演示地址2号','10000000002','2026-01-01 09:00:00.000000','管理员2',''),(4,'演示小区3','COMM003','北京市演示地址3号','10000000003','2026-01-01 09:00:00.000000','管理员3',''),(5,'演示小区4','COMM004','北京市演示地址4号','10000000004','2026-01-01 09:00:00.000000','管理员4',''),(6,'演示小区5','COMM005','北京市演示地址5号','10000000005','2026-01-01 09:00:00.000000','管理员5','');
/*!40000 ALTER TABLE `community` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_sys_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_sys_user_id` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-05-28 11:08:42.434829','1','管理员',1,'[{\"added\": {}}]',7,1),(2,'2026-05-28 11:08:53.721145','1','管理员',2,'[]',7,1),(3,'2026-05-28 11:12:32.061067','2','维修员',1,'[{\"added\": {}}]',7,1),(4,'2026-05-28 11:38:40.007105','1','admin',2,'[{\"changed\": {\"fields\": [\"\\u771f\\u5b9e\\u59d3\\u540d\", \"\\u89d2\\u8272\"]}}]',9,1),(5,'2026-05-29 04:29:43.852925','1','用户列表',1,'[{\"added\": {}}]',8,1),(6,'2026-05-29 04:29:56.724539','2','角色列表',1,'[{\"added\": {}}]',8,1),(7,'2026-05-29 04:30:51.152958','3','权限列表',1,'[{\"added\": {}}]',8,1),(8,'2026-05-29 04:31:05.966121','4','报修列表',1,'[{\"added\": {}}]',8,1),(9,'2026-05-29 04:35:05.931854','1','用户列表',2,'[{\"changed\": {\"fields\": [\"\\u83dc\\u5355\"]}}]',6,1),(10,'2026-05-29 04:35:13.013786','3','角色列表',2,'[{\"changed\": {\"fields\": [\"\\u83dc\\u5355\"]}}]',6,1),(11,'2026-05-29 04:35:21.596592','4','权限列表',2,'[{\"changed\": {\"fields\": [\"\\u83dc\\u5355\"]}}]',6,1),(12,'2026-05-29 07:59:41.889283','1','101',1,'[{\"added\": {}}]',13,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(21,'cars','car'),(11,'community','building'),(10,'community','community'),(13,'community','house'),(12,'community','unit'),(4,'contenttypes','contenttype'),(17,'finance','fee'),(20,'logs','loginlog'),(19,'logs','operationlog'),(18,'notice','notice'),(14,'owners','owner'),(15,'parking','parking'),(16,'repairs','repair'),(5,'sessions','session'),(8,'users','menu'),(6,'users','permission'),(7,'users','role'),(9,'users','user'),(22,'visitors','visitor');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-05-28 07:55:18.069463'),(2,'contenttypes','0002_remove_content_type_name','2026-05-28 07:55:18.082968'),(3,'auth','0001_initial','2026-05-28 07:55:18.122351'),(4,'auth','0002_alter_permission_name_max_length','2026-05-28 07:55:18.133085'),(5,'auth','0003_alter_user_email_max_length','2026-05-28 07:55:18.135499'),(6,'auth','0004_alter_user_username_opts','2026-05-28 07:55:18.140453'),(7,'auth','0005_alter_user_last_login_null','2026-05-28 07:55:18.143622'),(8,'auth','0006_require_contenttypes_0002','2026-05-28 07:55:18.144640'),(9,'auth','0007_alter_validators_add_error_messages','2026-05-28 07:55:18.146957'),(10,'auth','0008_alter_user_username_max_length','2026-05-28 07:55:18.149066'),(11,'auth','0009_alter_user_last_name_max_length','2026-05-28 07:55:18.151130'),(12,'auth','0010_alter_group_name_max_length','2026-05-28 07:55:18.155531'),(13,'auth','0011_update_proxy_permissions','2026-05-28 07:55:18.158966'),(14,'auth','0012_alter_user_first_name_max_length','2026-05-28 07:55:18.161271'),(15,'users','0001_initial','2026-05-28 07:55:18.271420'),(16,'admin','0001_initial','2026-05-28 07:55:18.300388'),(17,'admin','0002_logentry_remove_auto_add','2026-05-28 07:55:18.304030'),(18,'admin','0003_logentry_add_action_flag_choices','2026-05-28 07:55:18.307377'),(19,'community','0001_initial','2026-05-28 07:55:18.311321'),(20,'community','0002_building','2026-05-28 07:55:18.323025'),(21,'community','0003_alter_community_options_unit','2026-05-28 07:55:18.335952'),(22,'community','0004_house','2026-05-28 07:55:18.348680'),(23,'owners','0001_initial','2026-05-28 07:55:18.365123'),(27,'sessions','0001_initial','2026-05-28 07:55:18.425628'),(28,'users','0002_role_permissions','2026-05-28 10:58:28.817144'),(29,'users','0003_alter_user_phone_alter_user_real_name','2026-05-28 11:40:11.541996'),(30,'users','0004_permission_menu','2026-05-29 04:20:36.189699'),(31,'community','0005_remove_community_contact_person_and_more','2026-05-29 06:31:02.987066'),(32,'community','0006_alter_building_options_remove_building_status_and_more','2026-05-29 06:45:46.429898'),(33,'community','0007_alter_unit_options_remove_unit_house_count_and_more','2026-05-29 07:07:48.289417'),(34,'community','0008_alter_house_options_remove_house_floor_and_more','2026-05-29 07:27:24.343062'),(35,'owners','0002_alter_owner_options_remove_owner_address_and_more','2026-05-29 07:27:24.447000'),(36,'parking','0001_initial','2026-05-29 08:50:23.292236'),(40,'users','0005_remove_menu_roles_menu_menu_type','2026-06-01 07:41:21.854420'),(41,'owners','0003_remove_owner_move_in_date_owner_birthday_and_more','2026-06-01 09:53:02.307811'),(42,'owners','0004_owner_relationship','2026-06-01 10:11:04.709058'),(43,'parking','0002_remove_parking_house_parking_owner_and_more','2026-06-02 02:28:13.717211'),(44,'finance','0001_initial','2026-06-02 02:58:51.159547'),(47,'finance','0002_fee_fee_type_alter_fee_amount_alter_fee_house_and_more','2026-06-03 03:10:35.608742'),(48,'repairs','0001_initial','2026-06-03 05:05:52.023864'),(49,'notice','0001_initial','2026-06-03 06:41:55.095228'),(50,'logs','0001_initial','2026-06-03 09:16:52.352632'),(51,'owners','0005_owner_id_card_image','2026-06-04 05:10:16.001036'),(52,'logs','0002_loginlog','2026-06-04 07:17:06.953460'),(53,'owners','0006_owner_avatar','2026-06-04 10:05:58.206934'),(54,'cars','0001_initial','2026-06-05 06:14:54.217371'),(55,'visitors','0001_initial','2026-06-05 08:26:21.421129'),(56,'visitors','0002_visitor_approve_remark_visitor_approve_time_and_more','2026-06-08 08:33:28.395226'),(57,'visitors','0003_visitor_enter_time_alter_visitor_approve_user_and_more','2026-06-09 02:43:58.668675'),(58,'cars','0002_alter_car_options_car_car_type_car_plate_number_and_more','2026-06-09 03:38:45.130695'),(59,'repairs','0002_repair_finish_time_repair_remark_repair_repair_user_and_more','2026-06-09 04:17:03.373222'),(60,'cars','0003_car_status','2026-06-09 04:20:20.026744'),(61,'repairs','0003_remove_repair_remark_repair_phone_and_more','2026-06-09 05:01:44.760105'),(62,'cars','0004_remove_car_plate_number','2026-06-10 05:13:22.458713');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('84e0bsypuo3ifexzs6wl9pbqgao7hssm','.eJxVjMsOgyAQRf-FdUNGR15ddu83EGCg2DaQiK6a_ruauLDbc869X2bdumS7tjjbididdex2Zd6FdyyHoJcrz8pDLcs8eX4k_LSNj5Xi53G2fwfZtbyvPXS9gCFFCoQmgACBBpxMylPyREqjREmxR70TgUoHQUkSgDIwKM1-G-afN6o:1wSYST:Q-LZgtFgkDbSL-laPoFyZVLBuz96qk4FHto8UFpQq2s','2026-06-11 10:59:25.017214');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fee`
--

DROP TABLE IF EXISTS `fee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fee` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fee_month` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `pay_time` datetime(6) DEFAULT NULL,
  `remark` longtext COLLATE utf8mb4_general_ci,
  `created_at` datetime(6) NOT NULL,
  `house_id` bigint NOT NULL,
  `fee_type` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fee_house_id_5efaaa3f_fk_house_id` (`house_id`),
  CONSTRAINT `fee_house_id_5efaaa3f_fk_house_id` FOREIGN KEY (`house_id`) REFERENCES `house` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fee`
--

LOCK TABLES `fee` WRITE;
/*!40000 ALTER TABLE `fee` DISABLE KEYS */;
INSERT INTO `fee` VALUES (2,'2026-06',300.00,'unpaid',NULL,NULL,'2026-06-03 03:14:29.569697',1,'property'),(3,'2026-06',100.00,'paid',NULL,'','2026-06-03 04:08:51.082608',2,'water');
/*!40000 ALTER TABLE `fee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `house`
--

DROP TABLE IF EXISTS `house`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `house` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `area` decimal(10,2) NOT NULL,
  `house_type` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `unit_id` bigint NOT NULL,
  `owner_count` int NOT NULL,
  `remark` longtext COLLATE utf8mb4_general_ci,
  `resident_count` int NOT NULL,
  `room_no` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `house_unit_id_d36899f9_fk_unit_id` (`unit_id`),
  CONSTRAINT `house_unit_id_d36899f9_fk_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `unit` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1006 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `house`
--

LOCK TABLES `house` WRITE;
/*!40000 ALTER TABLE `house` DISABLE KEYS */;
INSERT INTO `house` VALUES (1,89.50,'两室一厅','vacant','2026-05-29 07:59:41.879601',1,0,'',0,'101'),(2,89.50,'三室两厅','occupied','2026-06-01 09:31:48.077396',1,1,'精装修',3,'101'),(3,89.50,'三室两厅','vacant','2026-06-02 08:12:28.554952',1,0,NULL,0,'102'),(4,95.50,'三室两厅','vacant','2026-06-02 09:11:51.916482',2,0,NULL,0,'102'),(5,50.00,'三室一厅','occupied','2026-06-03 09:57:16.626596',1,0,NULL,0,'104'),(6,79.91,'四室两厅','occupied','2026-01-01 09:00:00.000000',1,1,'',2,'0101'),(7,146.34,'四室两厅','occupied','2026-01-01 09:00:00.000000',1,2,'',5,'0201'),(8,91.99,'一室一厅','occupied','2026-01-01 09:00:00.000000',1,1,'',3,'0301'),(9,112.97,'两室一厅','renting','2026-01-01 09:00:00.000000',1,2,'',3,'0401'),(10,107.72,'一室一厅','occupied','2026-01-01 09:00:00.000000',1,2,'',4,'0501'),(11,140.31,'三室两厅','vacant','2026-01-01 09:00:00.000000',2,0,'',0,'0101'),(12,96.76,'三室两厅','vacant','2026-01-01 09:00:00.000000',2,0,'',0,'0201'),(13,70.47,'四室两厅','occupied','2026-01-01 09:00:00.000000',2,2,'',4,'0301'),(14,77.07,'四室两厅','renting','2026-01-01 09:00:00.000000',2,2,'',1,'0401'),(15,118.64,'三室两厅','renting','2026-01-01 09:00:00.000000',2,2,'',4,'0501'),(16,152.45,'一室一厅','occupied','2026-01-01 09:00:00.000000',3,2,'',5,'0101'),(17,125.55,'一室一厅','renting','2026-01-01 09:00:00.000000',3,1,'',5,'0201'),(18,139.73,'两室一厅','occupied','2026-01-01 09:00:00.000000',3,1,'',4,'0301'),(19,152.96,'四室两厅','vacant','2026-01-01 09:00:00.000000',3,0,'',0,'0401'),(20,135.43,'四室两厅','occupied','2026-01-01 09:00:00.000000',3,2,'',5,'0501'),(21,134.98,'四室两厅','occupied','2026-01-01 09:00:00.000000',4,2,'',4,'0101'),(22,88.25,'两室一厅','renting','2026-01-01 09:00:00.000000',4,1,'',1,'0201'),(23,133.56,'四室两厅','occupied','2026-01-01 09:00:00.000000',4,2,'',5,'0301'),(24,103.99,'四室两厅','occupied','2026-01-01 09:00:00.000000',4,2,'',4,'0401'),(25,148.80,'三室两厅','occupied','2026-01-01 09:00:00.000000',4,1,'',3,'0501'),(26,113.77,'三室两厅','renting','2026-01-01 09:00:00.000000',5,2,'',5,'0101'),(27,113.29,'一室一厅','repairing','2026-01-01 09:00:00.000000',5,2,'',4,'0201'),(28,132.85,'两室一厅','renting','2026-01-01 09:00:00.000000',5,2,'',1,'0301'),(29,142.76,'一室一厅','occupied','2026-01-01 09:00:00.000000',5,2,'',1,'0401'),(30,68.02,'两室一厅','occupied','2026-01-01 09:00:00.000000',5,1,'',5,'0501'),(31,92.78,'两室一厅','occupied','2026-01-01 09:00:00.000000',6,2,'',3,'0101'),(32,68.51,'两室一厅','occupied','2026-01-01 09:00:00.000000',6,2,'',2,'0201'),(33,115.30,'三室两厅','vacant','2026-01-01 09:00:00.000000',6,0,'',0,'0301'),(34,76.44,'三室两厅','occupied','2026-01-01 09:00:00.000000',6,1,'',5,'0401'),(35,118.77,'两室一厅','occupied','2026-01-01 09:00:00.000000',6,1,'',5,'0501'),(36,105.60,'一室一厅','repairing','2026-01-01 09:00:00.000000',7,2,'',1,'0101'),(37,151.38,'四室两厅','occupied','2026-01-01 09:00:00.000000',7,1,'',1,'0201'),(38,100.78,'四室两厅','occupied','2026-01-01 09:00:00.000000',7,2,'',1,'0301'),(39,162.88,'两室一厅','occupied','2026-01-01 09:00:00.000000',7,1,'',2,'0401'),(40,111.36,'四室两厅','occupied','2026-01-01 09:00:00.000000',7,1,'',1,'0501'),(41,71.42,'一室一厅','occupied','2026-01-01 09:00:00.000000',8,1,'',1,'0101'),(42,113.18,'一室一厅','renting','2026-01-01 09:00:00.000000',8,1,'',4,'0201'),(43,80.91,'两室一厅','occupied','2026-01-01 09:00:00.000000',8,1,'',2,'0301'),(44,107.00,'四室两厅','occupied','2026-01-01 09:00:00.000000',8,2,'',1,'0401'),(45,98.49,'四室两厅','occupied','2026-01-01 09:00:00.000000',8,2,'',4,'0501'),(46,167.92,'两室一厅','renting','2026-01-01 09:00:00.000000',9,2,'',4,'0101'),(47,100.58,'三室两厅','occupied','2026-01-01 09:00:00.000000',9,1,'',5,'0201'),(48,149.62,'一室一厅','renting','2026-01-01 09:00:00.000000',9,1,'',1,'0301'),(49,155.86,'两室一厅','occupied','2026-01-01 09:00:00.000000',9,2,'',5,'0401'),(50,164.12,'两室一厅','occupied','2026-01-01 09:00:00.000000',9,1,'',3,'0501'),(51,78.97,'三室两厅','occupied','2026-01-01 09:00:00.000000',10,1,'',5,'0101'),(52,124.28,'三室两厅','occupied','2026-01-01 09:00:00.000000',10,1,'',1,'0201'),(53,77.64,'三室两厅','occupied','2026-01-01 09:00:00.000000',10,1,'',1,'0301'),(54,140.24,'三室两厅','occupied','2026-01-01 09:00:00.000000',10,1,'',5,'0401'),(55,95.68,'两室一厅','renting','2026-01-01 09:00:00.000000',10,2,'',3,'0501'),(56,94.09,'四室两厅','vacant','2026-01-01 09:00:00.000000',11,0,'',0,'0101'),(57,154.65,'一室一厅','renting','2026-01-01 09:00:00.000000',11,2,'',4,'0201'),(58,73.73,'一室一厅','occupied','2026-01-01 09:00:00.000000',11,2,'',1,'0301'),(59,136.58,'四室两厅','occupied','2026-01-01 09:00:00.000000',11,2,'',3,'0401'),(60,128.73,'三室两厅','occupied','2026-01-01 09:00:00.000000',11,1,'',4,'0501'),(61,128.78,'三室两厅','occupied','2026-01-01 09:00:00.000000',12,2,'',1,'0101'),(62,154.13,'三室两厅','occupied','2026-01-01 09:00:00.000000',12,2,'',4,'0201'),(63,162.71,'三室两厅','occupied','2026-01-01 09:00:00.000000',12,2,'',1,'0301'),(64,137.53,'四室两厅','occupied','2026-01-01 09:00:00.000000',12,1,'',3,'0401'),(65,99.89,'一室一厅','renting','2026-01-01 09:00:00.000000',12,2,'',2,'0501'),(66,140.17,'一室一厅','vacant','2026-01-01 09:00:00.000000',13,0,'',0,'0101'),(67,79.83,'三室两厅','vacant','2026-01-01 09:00:00.000000',13,0,'',0,'0201'),(68,127.70,'四室两厅','repairing','2026-01-01 09:00:00.000000',13,2,'',1,'0301'),(69,125.81,'两室一厅','occupied','2026-01-01 09:00:00.000000',13,2,'',4,'0401'),(70,145.66,'一室一厅','occupied','2026-01-01 09:00:00.000000',13,1,'',2,'0501'),(71,134.16,'两室一厅','renting','2026-01-01 09:00:00.000000',14,2,'',3,'0101'),(72,90.83,'四室两厅','vacant','2026-01-01 09:00:00.000000',14,0,'',0,'0201'),(73,109.79,'一室一厅','repairing','2026-01-01 09:00:00.000000',14,1,'',5,'0301'),(74,151.96,'三室两厅','occupied','2026-01-01 09:00:00.000000',14,2,'',3,'0401'),(75,73.63,'一室一厅','renting','2026-01-01 09:00:00.000000',14,1,'',4,'0501'),(76,165.02,'三室两厅','occupied','2026-01-01 09:00:00.000000',15,1,'',4,'0101'),(77,163.10,'两室一厅','occupied','2026-01-01 09:00:00.000000',15,2,'',3,'0201'),(78,105.47,'四室两厅','occupied','2026-01-01 09:00:00.000000',15,2,'',5,'0301'),(79,157.70,'两室一厅','occupied','2026-01-01 09:00:00.000000',15,2,'',2,'0401'),(80,130.80,'四室两厅','occupied','2026-01-01 09:00:00.000000',15,1,'',3,'0501'),(81,147.54,'三室两厅','occupied','2026-01-01 09:00:00.000000',16,1,'',3,'0101'),(82,122.67,'两室一厅','occupied','2026-01-01 09:00:00.000000',16,1,'',1,'0201'),(83,152.98,'一室一厅','occupied','2026-01-01 09:00:00.000000',16,2,'',5,'0301'),(84,163.55,'一室一厅','occupied','2026-01-01 09:00:00.000000',16,1,'',5,'0401'),(85,76.55,'三室两厅','occupied','2026-01-01 09:00:00.000000',16,2,'',5,'0501'),(86,99.04,'三室两厅','occupied','2026-01-01 09:00:00.000000',17,1,'',2,'0101'),(87,97.53,'两室一厅','occupied','2026-01-01 09:00:00.000000',17,1,'',4,'0201'),(88,165.61,'三室两厅','occupied','2026-01-01 09:00:00.000000',17,2,'',4,'0301'),(89,149.21,'一室一厅','renting','2026-01-01 09:00:00.000000',17,1,'',5,'0401'),(90,85.96,'一室一厅','occupied','2026-01-01 09:00:00.000000',17,1,'',1,'0501'),(91,119.50,'一室一厅','renting','2026-01-01 09:00:00.000000',18,1,'',3,'0101'),(92,104.80,'两室一厅','occupied','2026-01-01 09:00:00.000000',18,1,'',5,'0201'),(93,80.65,'一室一厅','repairing','2026-01-01 09:00:00.000000',18,2,'',1,'0301'),(94,106.12,'四室两厅','occupied','2026-01-01 09:00:00.000000',18,1,'',3,'0401'),(95,158.95,'两室一厅','vacant','2026-01-01 09:00:00.000000',18,0,'',0,'0501'),(96,150.86,'三室两厅','occupied','2026-01-01 09:00:00.000000',19,2,'',5,'0101'),(97,76.25,'三室两厅','renting','2026-01-01 09:00:00.000000',19,1,'',4,'0201'),(98,94.53,'四室两厅','occupied','2026-01-01 09:00:00.000000',19,1,'',3,'0301'),(99,118.63,'三室两厅','occupied','2026-01-01 09:00:00.000000',19,2,'',4,'0401'),(100,85.67,'三室两厅','renting','2026-01-01 09:00:00.000000',19,1,'',3,'0501'),(101,108.97,'两室一厅','renting','2026-01-01 09:00:00.000000',20,2,'',2,'0101'),(102,112.17,'三室两厅','occupied','2026-01-01 09:00:00.000000',20,1,'',4,'0201'),(103,100.90,'三室两厅','vacant','2026-01-01 09:00:00.000000',20,0,'',0,'0301'),(104,152.12,'三室两厅','occupied','2026-01-01 09:00:00.000000',20,1,'',5,'0401'),(105,91.43,'三室两厅','repairing','2026-01-01 09:00:00.000000',20,1,'',3,'0501'),(106,125.44,'三室两厅','occupied','2026-01-01 09:00:00.000000',21,2,'',1,'0101'),(107,135.41,'两室一厅','occupied','2026-01-01 09:00:00.000000',21,2,'',5,'0201'),(108,110.44,'两室一厅','occupied','2026-01-01 09:00:00.000000',21,1,'',4,'0301'),(109,69.05,'三室两厅','occupied','2026-01-01 09:00:00.000000',21,2,'',2,'0401'),(110,125.90,'三室两厅','occupied','2026-01-01 09:00:00.000000',21,2,'',4,'0501'),(111,69.18,'三室两厅','renting','2026-01-01 09:00:00.000000',22,1,'',3,'0101'),(112,69.78,'三室两厅','occupied','2026-01-01 09:00:00.000000',22,2,'',5,'0201'),(113,130.28,'一室一厅','occupied','2026-01-01 09:00:00.000000',22,1,'',5,'0301'),(114,166.26,'两室一厅','occupied','2026-01-01 09:00:00.000000',22,1,'',4,'0401'),(115,128.61,'四室两厅','occupied','2026-01-01 09:00:00.000000',22,2,'',1,'0501'),(116,139.18,'一室一厅','occupied','2026-01-01 09:00:00.000000',23,1,'',1,'0101'),(117,95.09,'两室一厅','occupied','2026-01-01 09:00:00.000000',23,1,'',5,'0201'),(118,166.84,'三室两厅','renting','2026-01-01 09:00:00.000000',23,2,'',3,'0301'),(119,99.78,'三室两厅','occupied','2026-01-01 09:00:00.000000',23,2,'',3,'0401'),(120,71.67,'三室两厅','occupied','2026-01-01 09:00:00.000000',23,1,'',4,'0501'),(121,93.39,'三室两厅','renting','2026-01-01 09:00:00.000000',24,1,'',3,'0101'),(122,119.23,'一室一厅','occupied','2026-01-01 09:00:00.000000',24,2,'',2,'0201'),(123,149.49,'一室一厅','renting','2026-01-01 09:00:00.000000',24,2,'',4,'0301'),(124,153.30,'三室两厅','repairing','2026-01-01 09:00:00.000000',24,2,'',4,'0401'),(125,134.06,'两室一厅','occupied','2026-01-01 09:00:00.000000',24,1,'',5,'0501'),(126,143.93,'两室一厅','repairing','2026-01-01 09:00:00.000000',25,2,'',1,'0101'),(127,70.89,'两室一厅','occupied','2026-01-01 09:00:00.000000',25,2,'',5,'0201'),(128,119.37,'两室一厅','renting','2026-01-01 09:00:00.000000',25,2,'',4,'0301'),(129,123.89,'四室两厅','renting','2026-01-01 09:00:00.000000',25,2,'',3,'0401'),(130,121.27,'两室一厅','occupied','2026-01-01 09:00:00.000000',25,1,'',2,'0501'),(131,140.87,'一室一厅','vacant','2026-01-01 09:00:00.000000',26,0,'',0,'0101'),(132,148.19,'两室一厅','renting','2026-01-01 09:00:00.000000',26,2,'',3,'0201'),(133,81.92,'四室两厅','repairing','2026-01-01 09:00:00.000000',26,2,'',2,'0301'),(134,84.83,'四室两厅','occupied','2026-01-01 09:00:00.000000',26,1,'',2,'0401'),(135,132.12,'两室一厅','occupied','2026-01-01 09:00:00.000000',26,1,'',3,'0501'),(136,119.46,'四室两厅','renting','2026-01-01 09:00:00.000000',27,1,'',4,'0101'),(137,83.50,'一室一厅','occupied','2026-01-01 09:00:00.000000',27,1,'',4,'0201'),(138,73.82,'一室一厅','occupied','2026-01-01 09:00:00.000000',27,2,'',3,'0301'),(139,84.38,'四室两厅','occupied','2026-01-01 09:00:00.000000',27,1,'',4,'0401'),(140,87.94,'四室两厅','renting','2026-01-01 09:00:00.000000',27,1,'',2,'0501'),(141,89.27,'四室两厅','occupied','2026-01-01 09:00:00.000000',28,2,'',4,'0101'),(142,153.62,'四室两厅','occupied','2026-01-01 09:00:00.000000',28,2,'',4,'0201'),(143,77.18,'一室一厅','renting','2026-01-01 09:00:00.000000',28,1,'',1,'0301'),(144,103.39,'两室一厅','occupied','2026-01-01 09:00:00.000000',28,1,'',1,'0401'),(145,88.36,'两室一厅','occupied','2026-01-01 09:00:00.000000',28,2,'',1,'0501'),(146,132.82,'三室两厅','renting','2026-01-01 09:00:00.000000',29,2,'',3,'0101'),(147,107.83,'三室两厅','occupied','2026-01-01 09:00:00.000000',29,2,'',3,'0201'),(148,116.82,'两室一厅','vacant','2026-01-01 09:00:00.000000',29,0,'',0,'0301'),(149,123.96,'一室一厅','repairing','2026-01-01 09:00:00.000000',29,2,'',4,'0401'),(150,161.07,'一室一厅','occupied','2026-01-01 09:00:00.000000',29,2,'',3,'0501'),(151,114.10,'三室两厅','occupied','2026-01-01 09:00:00.000000',30,1,'',3,'0101'),(152,71.72,'四室两厅','occupied','2026-01-01 09:00:00.000000',30,1,'',5,'0201'),(153,124.44,'四室两厅','occupied','2026-01-01 09:00:00.000000',30,2,'',5,'0301'),(154,122.08,'一室一厅','occupied','2026-01-01 09:00:00.000000',30,2,'',2,'0401'),(155,78.52,'三室两厅','vacant','2026-01-01 09:00:00.000000',30,0,'',0,'0501'),(156,69.82,'一室一厅','vacant','2026-01-01 09:00:00.000000',31,0,'',0,'0101'),(157,143.26,'三室两厅','occupied','2026-01-01 09:00:00.000000',31,2,'',2,'0201'),(158,163.82,'四室两厅','occupied','2026-01-01 09:00:00.000000',31,2,'',2,'0301'),(159,91.84,'一室一厅','renting','2026-01-01 09:00:00.000000',31,2,'',4,'0401'),(160,116.90,'一室一厅','occupied','2026-01-01 09:00:00.000000',31,2,'',2,'0501'),(161,126.84,'一室一厅','occupied','2026-01-01 09:00:00.000000',32,2,'',5,'0101'),(162,117.90,'四室两厅','occupied','2026-01-01 09:00:00.000000',32,1,'',5,'0201'),(163,146.46,'四室两厅','occupied','2026-01-01 09:00:00.000000',32,2,'',3,'0301'),(164,154.36,'两室一厅','occupied','2026-01-01 09:00:00.000000',32,2,'',5,'0401'),(165,163.32,'三室两厅','vacant','2026-01-01 09:00:00.000000',32,0,'',0,'0501'),(166,148.58,'四室两厅','occupied','2026-01-01 09:00:00.000000',33,1,'',4,'0101'),(167,148.78,'一室一厅','renting','2026-01-01 09:00:00.000000',33,2,'',4,'0201'),(168,92.43,'两室一厅','vacant','2026-01-01 09:00:00.000000',33,0,'',0,'0301'),(169,120.47,'两室一厅','renting','2026-01-01 09:00:00.000000',33,1,'',3,'0401'),(170,161.67,'一室一厅','vacant','2026-01-01 09:00:00.000000',33,0,'',0,'0501'),(171,157.94,'四室两厅','occupied','2026-01-01 09:00:00.000000',34,1,'',3,'0101'),(172,152.09,'四室两厅','occupied','2026-01-01 09:00:00.000000',34,1,'',2,'0201'),(173,72.70,'一室一厅','vacant','2026-01-01 09:00:00.000000',34,0,'',0,'0301'),(174,95.91,'一室一厅','vacant','2026-01-01 09:00:00.000000',34,0,'',0,'0401'),(175,115.14,'两室一厅','occupied','2026-01-01 09:00:00.000000',34,1,'',5,'0501'),(176,117.53,'三室两厅','vacant','2026-01-01 09:00:00.000000',35,0,'',0,'0101'),(177,90.83,'一室一厅','occupied','2026-01-01 09:00:00.000000',35,1,'',2,'0201'),(178,69.51,'两室一厅','occupied','2026-01-01 09:00:00.000000',35,1,'',4,'0301'),(179,85.16,'三室两厅','occupied','2026-01-01 09:00:00.000000',35,1,'',5,'0401'),(180,107.98,'一室一厅','repairing','2026-01-01 09:00:00.000000',35,1,'',4,'0501'),(181,69.89,'两室一厅','vacant','2026-01-01 09:00:00.000000',36,0,'',0,'0101'),(182,166.10,'两室一厅','occupied','2026-01-01 09:00:00.000000',36,1,'',4,'0201'),(183,136.67,'一室一厅','occupied','2026-01-01 09:00:00.000000',36,2,'',5,'0301'),(184,81.87,'四室两厅','renting','2026-01-01 09:00:00.000000',36,1,'',4,'0401'),(185,135.08,'一室一厅','occupied','2026-01-01 09:00:00.000000',36,2,'',1,'0501'),(186,133.03,'三室两厅','occupied','2026-01-01 09:00:00.000000',37,2,'',2,'0101'),(187,127.47,'一室一厅','occupied','2026-01-01 09:00:00.000000',37,1,'',3,'0201'),(188,165.24,'一室一厅','occupied','2026-01-01 09:00:00.000000',37,1,'',4,'0301'),(189,92.27,'四室两厅','occupied','2026-01-01 09:00:00.000000',37,1,'',5,'0401'),(190,79.31,'三室两厅','vacant','2026-01-01 09:00:00.000000',37,0,'',0,'0501'),(191,82.76,'三室两厅','renting','2026-01-01 09:00:00.000000',38,1,'',4,'0101'),(192,162.84,'一室一厅','occupied','2026-01-01 09:00:00.000000',38,1,'',4,'0201'),(193,77.62,'四室两厅','renting','2026-01-01 09:00:00.000000',38,2,'',1,'0301'),(194,163.33,'三室两厅','occupied','2026-01-01 09:00:00.000000',38,2,'',3,'0401'),(195,112.59,'三室两厅','occupied','2026-01-01 09:00:00.000000',38,2,'',3,'0501'),(196,149.81,'一室一厅','vacant','2026-01-01 09:00:00.000000',39,0,'',0,'0101'),(197,88.46,'两室一厅','repairing','2026-01-01 09:00:00.000000',39,2,'',4,'0201'),(198,154.76,'两室一厅','occupied','2026-01-01 09:00:00.000000',39,1,'',1,'0301'),(199,106.52,'三室两厅','occupied','2026-01-01 09:00:00.000000',39,2,'',2,'0401'),(200,159.20,'三室两厅','occupied','2026-01-01 09:00:00.000000',39,2,'',3,'0501'),(201,154.56,'三室两厅','occupied','2026-01-01 09:00:00.000000',40,1,'',5,'0101'),(202,71.74,'两室一厅','occupied','2026-01-01 09:00:00.000000',40,1,'',3,'0201'),(203,152.77,'四室两厅','occupied','2026-01-01 09:00:00.000000',40,1,'',4,'0301'),(204,131.64,'三室两厅','occupied','2026-01-01 09:00:00.000000',40,2,'',1,'0401'),(205,124.18,'三室两厅','renting','2026-01-01 09:00:00.000000',40,1,'',5,'0501'),(206,148.11,'四室两厅','renting','2026-01-01 09:00:00.000000',41,2,'',3,'0101'),(207,120.58,'四室两厅','vacant','2026-01-01 09:00:00.000000',41,0,'',0,'0201'),(208,106.74,'四室两厅','renting','2026-01-01 09:00:00.000000',41,2,'',2,'0301'),(209,103.62,'两室一厅','occupied','2026-01-01 09:00:00.000000',41,1,'',1,'0401'),(210,89.53,'两室一厅','occupied','2026-01-01 09:00:00.000000',41,2,'',4,'0501'),(211,111.54,'一室一厅','occupied','2026-01-01 09:00:00.000000',42,1,'',5,'0101'),(212,166.18,'四室两厅','vacant','2026-01-01 09:00:00.000000',42,0,'',0,'0201'),(213,80.31,'两室一厅','occupied','2026-01-01 09:00:00.000000',42,1,'',4,'0301'),(214,100.12,'三室两厅','renting','2026-01-01 09:00:00.000000',42,1,'',1,'0401'),(215,133.89,'一室一厅','occupied','2026-01-01 09:00:00.000000',42,2,'',1,'0501'),(216,150.67,'两室一厅','occupied','2026-01-01 09:00:00.000000',43,2,'',3,'0101'),(217,80.46,'四室两厅','occupied','2026-01-01 09:00:00.000000',43,1,'',4,'0201'),(218,163.05,'一室一厅','renting','2026-01-01 09:00:00.000000',43,2,'',2,'0301'),(219,70.06,'四室两厅','occupied','2026-01-01 09:00:00.000000',43,1,'',4,'0401'),(220,74.13,'四室两厅','occupied','2026-01-01 09:00:00.000000',43,1,'',1,'0501'),(221,86.14,'两室一厅','occupied','2026-01-01 09:00:00.000000',44,2,'',5,'0101'),(222,110.46,'两室一厅','occupied','2026-01-01 09:00:00.000000',44,1,'',1,'0201'),(223,128.25,'一室一厅','renting','2026-01-01 09:00:00.000000',44,2,'',4,'0301'),(224,137.49,'一室一厅','occupied','2026-01-01 09:00:00.000000',44,1,'',4,'0401'),(225,125.79,'三室两厅','occupied','2026-01-01 09:00:00.000000',44,2,'',4,'0501'),(226,91.39,'四室两厅','renting','2026-01-01 09:00:00.000000',45,1,'',5,'0101'),(227,93.31,'四室两厅','occupied','2026-01-01 09:00:00.000000',45,2,'',5,'0201'),(228,97.01,'四室两厅','occupied','2026-01-01 09:00:00.000000',45,2,'',2,'0301'),(229,84.30,'三室两厅','renting','2026-01-01 09:00:00.000000',45,2,'',3,'0401'),(230,79.03,'三室两厅','occupied','2026-01-01 09:00:00.000000',45,1,'',2,'0501'),(231,137.72,'四室两厅','occupied','2026-01-01 09:00:00.000000',46,1,'',3,'0101'),(232,132.70,'三室两厅','occupied','2026-01-01 09:00:00.000000',46,2,'',1,'0201'),(233,154.94,'三室两厅','repairing','2026-01-01 09:00:00.000000',46,2,'',5,'0301'),(234,124.94,'三室两厅','occupied','2026-01-01 09:00:00.000000',46,2,'',4,'0401'),(235,147.23,'四室两厅','renting','2026-01-01 09:00:00.000000',46,1,'',3,'0501'),(236,114.60,'一室一厅','occupied','2026-01-01 09:00:00.000000',47,2,'',5,'0101'),(237,79.62,'三室两厅','occupied','2026-01-01 09:00:00.000000',47,2,'',4,'0201'),(238,159.45,'两室一厅','repairing','2026-01-01 09:00:00.000000',47,2,'',1,'0301'),(239,89.83,'两室一厅','vacant','2026-01-01 09:00:00.000000',47,0,'',0,'0401'),(240,72.97,'一室一厅','occupied','2026-01-01 09:00:00.000000',47,2,'',1,'0501'),(241,96.91,'四室两厅','vacant','2026-01-01 09:00:00.000000',48,0,'',0,'0101'),(242,90.94,'一室一厅','occupied','2026-01-01 09:00:00.000000',48,1,'',1,'0201'),(243,167.89,'两室一厅','renting','2026-01-01 09:00:00.000000',48,2,'',1,'0301'),(244,112.08,'四室两厅','renting','2026-01-01 09:00:00.000000',48,1,'',3,'0401'),(245,160.23,'一室一厅','occupied','2026-01-01 09:00:00.000000',48,2,'',2,'0501'),(246,109.47,'两室一厅','vacant','2026-01-01 09:00:00.000000',49,0,'',0,'0101'),(247,128.66,'四室两厅','occupied','2026-01-01 09:00:00.000000',49,1,'',4,'0201'),(248,150.13,'三室两厅','occupied','2026-01-01 09:00:00.000000',49,1,'',1,'0301'),(249,145.83,'两室一厅','vacant','2026-01-01 09:00:00.000000',49,0,'',0,'0401'),(250,110.98,'两室一厅','occupied','2026-01-01 09:00:00.000000',49,2,'',5,'0501'),(251,88.56,'一室一厅','occupied','2026-01-01 09:00:00.000000',50,2,'',1,'0101'),(252,87.33,'一室一厅','occupied','2026-01-01 09:00:00.000000',50,2,'',4,'0201'),(253,153.75,'一室一厅','vacant','2026-01-01 09:00:00.000000',50,0,'',0,'0301'),(254,95.64,'一室一厅','occupied','2026-01-01 09:00:00.000000',50,2,'',3,'0401'),(255,98.36,'四室两厅','occupied','2026-01-01 09:00:00.000000',50,1,'',2,'0501'),(256,123.82,'两室一厅','renting','2026-01-01 09:00:00.000000',51,1,'',2,'0101'),(257,87.42,'三室两厅','occupied','2026-01-01 09:00:00.000000',51,1,'',4,'0201'),(258,126.80,'两室一厅','occupied','2026-01-01 09:00:00.000000',51,1,'',2,'0301'),(259,161.81,'三室两厅','occupied','2026-01-01 09:00:00.000000',51,1,'',5,'0401'),(260,147.83,'三室两厅','renting','2026-01-01 09:00:00.000000',51,1,'',5,'0501'),(261,152.75,'一室一厅','occupied','2026-01-01 09:00:00.000000',52,2,'',4,'0101'),(262,159.72,'一室一厅','occupied','2026-01-01 09:00:00.000000',52,2,'',4,'0201'),(263,88.78,'四室两厅','vacant','2026-01-01 09:00:00.000000',52,0,'',0,'0301'),(264,75.18,'一室一厅','occupied','2026-01-01 09:00:00.000000',52,2,'',2,'0401'),(265,160.60,'两室一厅','occupied','2026-01-01 09:00:00.000000',52,2,'',1,'0501'),(266,133.42,'三室两厅','renting','2026-01-01 09:00:00.000000',53,1,'',1,'0101'),(267,88.21,'三室两厅','occupied','2026-01-01 09:00:00.000000',53,2,'',1,'0201'),(268,117.89,'两室一厅','occupied','2026-01-01 09:00:00.000000',53,2,'',3,'0301'),(269,72.27,'四室两厅','renting','2026-01-01 09:00:00.000000',53,2,'',4,'0401'),(270,74.23,'三室两厅','occupied','2026-01-01 09:00:00.000000',53,2,'',2,'0501'),(271,123.48,'一室一厅','occupied','2026-01-01 09:00:00.000000',54,2,'',5,'0101'),(272,131.65,'四室两厅','renting','2026-01-01 09:00:00.000000',54,1,'',4,'0201'),(273,161.33,'一室一厅','vacant','2026-01-01 09:00:00.000000',54,0,'',0,'0301'),(274,115.24,'一室一厅','renting','2026-01-01 09:00:00.000000',54,2,'',4,'0401'),(275,139.38,'三室两厅','occupied','2026-01-01 09:00:00.000000',54,2,'',1,'0501'),(276,79.78,'两室一厅','occupied','2026-01-01 09:00:00.000000',55,1,'',3,'0101'),(277,114.02,'四室两厅','occupied','2026-01-01 09:00:00.000000',55,1,'',1,'0201'),(278,103.11,'三室两厅','occupied','2026-01-01 09:00:00.000000',55,1,'',2,'0301'),(279,85.94,'四室两厅','renting','2026-01-01 09:00:00.000000',55,2,'',4,'0401'),(280,123.62,'三室两厅','occupied','2026-01-01 09:00:00.000000',55,2,'',4,'0501'),(281,155.41,'三室两厅','occupied','2026-01-01 09:00:00.000000',56,2,'',3,'0101'),(282,165.84,'一室一厅','occupied','2026-01-01 09:00:00.000000',56,2,'',5,'0201'),(283,153.58,'四室两厅','occupied','2026-01-01 09:00:00.000000',56,1,'',1,'0301'),(284,85.58,'四室两厅','occupied','2026-01-01 09:00:00.000000',56,1,'',3,'0401'),(285,114.65,'一室一厅','occupied','2026-01-01 09:00:00.000000',56,2,'',3,'0501'),(286,131.08,'一室一厅','occupied','2026-01-01 09:00:00.000000',57,2,'',3,'0101'),(287,144.08,'四室两厅','renting','2026-01-01 09:00:00.000000',57,2,'',3,'0201'),(288,77.15,'一室一厅','occupied','2026-01-01 09:00:00.000000',57,2,'',1,'0301'),(289,120.16,'三室两厅','vacant','2026-01-01 09:00:00.000000',57,0,'',0,'0401'),(290,148.99,'三室两厅','renting','2026-01-01 09:00:00.000000',57,1,'',3,'0501'),(291,69.35,'三室两厅','occupied','2026-01-01 09:00:00.000000',58,1,'',5,'0101'),(292,145.62,'两室一厅','occupied','2026-01-01 09:00:00.000000',58,1,'',5,'0201'),(293,94.59,'四室两厅','occupied','2026-01-01 09:00:00.000000',58,1,'',2,'0301'),(294,164.32,'一室一厅','occupied','2026-01-01 09:00:00.000000',58,2,'',5,'0401'),(295,141.86,'一室一厅','vacant','2026-01-01 09:00:00.000000',58,0,'',0,'0501'),(296,156.39,'两室一厅','repairing','2026-01-01 09:00:00.000000',59,1,'',3,'0101'),(297,69.87,'一室一厅','occupied','2026-01-01 09:00:00.000000',59,1,'',5,'0201'),(298,112.37,'两室一厅','vacant','2026-01-01 09:00:00.000000',59,0,'',0,'0301'),(299,117.28,'四室两厅','repairing','2026-01-01 09:00:00.000000',59,1,'',3,'0401'),(300,71.29,'四室两厅','vacant','2026-01-01 09:00:00.000000',59,0,'',0,'0501'),(301,112.89,'四室两厅','occupied','2026-01-01 09:00:00.000000',60,1,'',4,'0101'),(302,153.36,'两室一厅','renting','2026-01-01 09:00:00.000000',60,2,'',4,'0201'),(303,103.55,'两室一厅','vacant','2026-01-01 09:00:00.000000',60,0,'',0,'0301'),(304,70.84,'三室两厅','occupied','2026-01-01 09:00:00.000000',60,1,'',1,'0401'),(305,68.56,'两室一厅','occupied','2026-01-01 09:00:00.000000',60,1,'',3,'0501'),(306,107.00,'四室两厅','renting','2026-01-01 09:00:00.000000',61,1,'',4,'0101'),(307,77.86,'两室一厅','renting','2026-01-01 09:00:00.000000',61,1,'',5,'0201'),(308,159.41,'两室一厅','vacant','2026-01-01 09:00:00.000000',61,0,'',0,'0301'),(309,109.87,'一室一厅','vacant','2026-01-01 09:00:00.000000',61,0,'',0,'0401'),(310,146.23,'一室一厅','renting','2026-01-01 09:00:00.000000',61,2,'',4,'0501'),(311,154.55,'两室一厅','renting','2026-01-01 09:00:00.000000',62,1,'',5,'0101'),(312,88.38,'两室一厅','renting','2026-01-01 09:00:00.000000',62,1,'',2,'0201'),(313,117.13,'四室两厅','renting','2026-01-01 09:00:00.000000',62,2,'',1,'0301'),(314,80.30,'一室一厅','occupied','2026-01-01 09:00:00.000000',62,1,'',2,'0401'),(315,159.50,'四室两厅','repairing','2026-01-01 09:00:00.000000',62,1,'',4,'0501'),(316,150.37,'四室两厅','occupied','2026-01-01 09:00:00.000000',63,2,'',1,'0101'),(317,107.53,'四室两厅','repairing','2026-01-01 09:00:00.000000',63,2,'',1,'0201'),(318,117.83,'四室两厅','renting','2026-01-01 09:00:00.000000',63,1,'',3,'0301'),(319,87.59,'三室两厅','occupied','2026-01-01 09:00:00.000000',63,1,'',2,'0401'),(320,79.87,'三室两厅','renting','2026-01-01 09:00:00.000000',63,1,'',4,'0501'),(321,90.42,'两室一厅','repairing','2026-01-01 09:00:00.000000',64,2,'',4,'0101'),(322,119.69,'两室一厅','occupied','2026-01-01 09:00:00.000000',64,1,'',5,'0201'),(323,69.48,'两室一厅','occupied','2026-01-01 09:00:00.000000',64,1,'',3,'0301'),(324,131.13,'三室两厅','vacant','2026-01-01 09:00:00.000000',64,0,'',0,'0401'),(325,81.60,'一室一厅','occupied','2026-01-01 09:00:00.000000',64,1,'',4,'0501'),(326,146.42,'四室两厅','occupied','2026-01-01 09:00:00.000000',65,2,'',1,'0101'),(327,74.02,'四室两厅','repairing','2026-01-01 09:00:00.000000',65,1,'',5,'0201'),(328,69.10,'一室一厅','vacant','2026-01-01 09:00:00.000000',65,0,'',0,'0301'),(329,114.26,'两室一厅','occupied','2026-01-01 09:00:00.000000',65,1,'',2,'0401'),(330,142.97,'两室一厅','vacant','2026-01-01 09:00:00.000000',65,0,'',0,'0501'),(331,106.41,'四室两厅','occupied','2026-01-01 09:00:00.000000',66,2,'',2,'0101'),(332,120.60,'四室两厅','renting','2026-01-01 09:00:00.000000',66,1,'',4,'0201'),(333,137.50,'四室两厅','occupied','2026-01-01 09:00:00.000000',66,1,'',1,'0301'),(334,130.87,'三室两厅','occupied','2026-01-01 09:00:00.000000',66,1,'',5,'0401'),(335,108.15,'两室一厅','occupied','2026-01-01 09:00:00.000000',66,1,'',2,'0501'),(336,89.33,'三室两厅','occupied','2026-01-01 09:00:00.000000',67,2,'',5,'0101'),(337,88.46,'四室两厅','occupied','2026-01-01 09:00:00.000000',67,2,'',3,'0201'),(338,155.11,'两室一厅','renting','2026-01-01 09:00:00.000000',67,1,'',1,'0301'),(339,154.91,'一室一厅','occupied','2026-01-01 09:00:00.000000',67,1,'',1,'0401'),(340,111.59,'四室两厅','renting','2026-01-01 09:00:00.000000',67,2,'',1,'0501'),(341,75.26,'两室一厅','occupied','2026-01-01 09:00:00.000000',68,1,'',3,'0101'),(342,91.55,'三室两厅','occupied','2026-01-01 09:00:00.000000',68,2,'',3,'0201'),(343,71.54,'一室一厅','renting','2026-01-01 09:00:00.000000',68,2,'',5,'0301'),(344,145.23,'四室两厅','occupied','2026-01-01 09:00:00.000000',68,1,'',1,'0401'),(345,75.62,'两室一厅','occupied','2026-01-01 09:00:00.000000',68,1,'',2,'0501'),(346,103.08,'一室一厅','occupied','2026-01-01 09:00:00.000000',69,2,'',2,'0101'),(347,104.79,'两室一厅','occupied','2026-01-01 09:00:00.000000',69,1,'',3,'0201'),(348,128.12,'两室一厅','occupied','2026-01-01 09:00:00.000000',69,1,'',5,'0301'),(349,96.89,'四室两厅','occupied','2026-01-01 09:00:00.000000',69,1,'',2,'0401'),(350,141.74,'两室一厅','vacant','2026-01-01 09:00:00.000000',69,0,'',0,'0501'),(351,105.49,'一室一厅','vacant','2026-01-01 09:00:00.000000',70,0,'',0,'0101'),(352,158.44,'两室一厅','vacant','2026-01-01 09:00:00.000000',70,0,'',0,'0201'),(353,162.16,'四室两厅','occupied','2026-01-01 09:00:00.000000',70,2,'',2,'0301'),(354,147.31,'四室两厅','renting','2026-01-01 09:00:00.000000',70,2,'',4,'0401'),(355,72.61,'两室一厅','occupied','2026-01-01 09:00:00.000000',70,2,'',3,'0501'),(356,96.62,'两室一厅','occupied','2026-01-01 09:00:00.000000',71,2,'',3,'0101'),(357,93.60,'一室一厅','renting','2026-01-01 09:00:00.000000',71,2,'',3,'0201'),(358,131.51,'三室两厅','occupied','2026-01-01 09:00:00.000000',71,2,'',3,'0301'),(359,141.20,'三室两厅','occupied','2026-01-01 09:00:00.000000',71,2,'',1,'0401'),(360,151.01,'两室一厅','renting','2026-01-01 09:00:00.000000',71,2,'',1,'0501'),(361,129.32,'三室两厅','occupied','2026-01-01 09:00:00.000000',72,1,'',3,'0101'),(362,70.12,'一室一厅','occupied','2026-01-01 09:00:00.000000',72,2,'',4,'0201'),(363,125.08,'四室两厅','vacant','2026-01-01 09:00:00.000000',72,0,'',0,'0301'),(364,94.50,'四室两厅','occupied','2026-01-01 09:00:00.000000',72,1,'',5,'0401'),(365,160.65,'四室两厅','renting','2026-01-01 09:00:00.000000',72,1,'',4,'0501'),(366,114.46,'四室两厅','vacant','2026-01-01 09:00:00.000000',73,0,'',0,'0101'),(367,96.13,'两室一厅','occupied','2026-01-01 09:00:00.000000',73,2,'',1,'0201'),(368,113.96,'四室两厅','vacant','2026-01-01 09:00:00.000000',73,0,'',0,'0301'),(369,121.94,'四室两厅','renting','2026-01-01 09:00:00.000000',73,1,'',4,'0401'),(370,166.97,'四室两厅','renting','2026-01-01 09:00:00.000000',73,2,'',3,'0501'),(371,118.38,'四室两厅','renting','2026-01-01 09:00:00.000000',74,2,'',1,'0101'),(372,140.67,'两室一厅','occupied','2026-01-01 09:00:00.000000',74,2,'',5,'0201'),(373,72.45,'四室两厅','renting','2026-01-01 09:00:00.000000',74,1,'',5,'0301'),(374,85.09,'三室两厅','occupied','2026-01-01 09:00:00.000000',74,2,'',4,'0401'),(375,92.83,'一室一厅','renting','2026-01-01 09:00:00.000000',74,2,'',1,'0501'),(376,68.67,'一室一厅','renting','2026-01-01 09:00:00.000000',75,2,'',4,'0101'),(377,70.94,'一室一厅','renting','2026-01-01 09:00:00.000000',75,1,'',2,'0201'),(378,153.28,'一室一厅','vacant','2026-01-01 09:00:00.000000',75,0,'',0,'0301'),(379,130.85,'三室两厅','renting','2026-01-01 09:00:00.000000',75,1,'',5,'0401'),(380,99.25,'四室两厅','repairing','2026-01-01 09:00:00.000000',75,1,'',1,'0501'),(381,141.43,'两室一厅','renting','2026-01-01 09:00:00.000000',76,2,'',3,'0101'),(382,74.27,'四室两厅','occupied','2026-01-01 09:00:00.000000',76,2,'',3,'0201'),(383,161.46,'两室一厅','occupied','2026-01-01 09:00:00.000000',76,1,'',2,'0301'),(384,79.30,'两室一厅','occupied','2026-01-01 09:00:00.000000',76,2,'',4,'0401'),(385,76.47,'三室两厅','vacant','2026-01-01 09:00:00.000000',76,0,'',0,'0501'),(386,151.44,'四室两厅','occupied','2026-01-01 09:00:00.000000',77,2,'',3,'0101'),(387,132.23,'两室一厅','occupied','2026-01-01 09:00:00.000000',77,2,'',4,'0201'),(388,132.15,'一室一厅','renting','2026-01-01 09:00:00.000000',77,1,'',5,'0301'),(389,147.76,'四室两厅','occupied','2026-01-01 09:00:00.000000',77,1,'',2,'0401'),(390,138.55,'四室两厅','occupied','2026-01-01 09:00:00.000000',77,1,'',2,'0501'),(391,151.53,'两室一厅','occupied','2026-01-01 09:00:00.000000',78,1,'',1,'0101'),(392,155.82,'三室两厅','occupied','2026-01-01 09:00:00.000000',78,2,'',1,'0201'),(393,134.48,'三室两厅','renting','2026-01-01 09:00:00.000000',78,1,'',5,'0301'),(394,82.94,'两室一厅','occupied','2026-01-01 09:00:00.000000',78,2,'',3,'0401'),(395,101.63,'两室一厅','repairing','2026-01-01 09:00:00.000000',78,2,'',5,'0501'),(396,114.95,'三室两厅','occupied','2026-01-01 09:00:00.000000',79,2,'',2,'0101'),(397,100.63,'三室两厅','occupied','2026-01-01 09:00:00.000000',79,1,'',4,'0201'),(398,99.46,'三室两厅','repairing','2026-01-01 09:00:00.000000',79,1,'',1,'0301'),(399,105.48,'一室一厅','repairing','2026-01-01 09:00:00.000000',79,2,'',4,'0401'),(400,150.81,'三室两厅','occupied','2026-01-01 09:00:00.000000',79,2,'',5,'0501'),(401,100.91,'四室两厅','renting','2026-01-01 09:00:00.000000',80,1,'',1,'0101'),(402,131.15,'三室两厅','occupied','2026-01-01 09:00:00.000000',80,2,'',1,'0201'),(403,122.33,'两室一厅','repairing','2026-01-01 09:00:00.000000',80,1,'',2,'0301'),(404,74.40,'三室两厅','renting','2026-01-01 09:00:00.000000',80,2,'',1,'0401'),(405,144.55,'两室一厅','vacant','2026-01-01 09:00:00.000000',80,0,'',0,'0501'),(406,157.62,'三室两厅','occupied','2026-01-01 09:00:00.000000',81,1,'',5,'0101'),(407,150.88,'一室一厅','renting','2026-01-01 09:00:00.000000',81,2,'',1,'0201'),(408,75.04,'三室两厅','vacant','2026-01-01 09:00:00.000000',81,0,'',0,'0301'),(409,139.22,'四室两厅','renting','2026-01-01 09:00:00.000000',81,2,'',3,'0401'),(410,74.46,'三室两厅','vacant','2026-01-01 09:00:00.000000',81,0,'',0,'0501'),(411,161.73,'两室一厅','occupied','2026-01-01 09:00:00.000000',82,1,'',5,'0101'),(412,143.74,'两室一厅','vacant','2026-01-01 09:00:00.000000',82,0,'',0,'0201'),(413,103.11,'两室一厅','occupied','2026-01-01 09:00:00.000000',82,1,'',5,'0301'),(414,162.75,'三室两厅','renting','2026-01-01 09:00:00.000000',82,1,'',3,'0401'),(415,92.96,'三室两厅','vacant','2026-01-01 09:00:00.000000',82,0,'',0,'0501'),(416,85.89,'四室两厅','occupied','2026-01-01 09:00:00.000000',83,1,'',2,'0101'),(417,132.58,'四室两厅','renting','2026-01-01 09:00:00.000000',83,2,'',1,'0201'),(418,120.45,'三室两厅','renting','2026-01-01 09:00:00.000000',83,2,'',2,'0301'),(419,114.15,'三室两厅','occupied','2026-01-01 09:00:00.000000',83,1,'',3,'0401'),(420,166.44,'三室两厅','occupied','2026-01-01 09:00:00.000000',83,2,'',3,'0501'),(421,120.19,'三室两厅','occupied','2026-01-01 09:00:00.000000',84,2,'',2,'0101'),(422,86.13,'四室两厅','occupied','2026-01-01 09:00:00.000000',84,2,'',1,'0201'),(423,138.52,'一室一厅','occupied','2026-01-01 09:00:00.000000',84,2,'',4,'0301'),(424,89.65,'四室两厅','occupied','2026-01-01 09:00:00.000000',84,2,'',1,'0401'),(425,126.57,'一室一厅','occupied','2026-01-01 09:00:00.000000',84,2,'',4,'0501'),(426,132.65,'四室两厅','occupied','2026-01-01 09:00:00.000000',85,1,'',1,'0101'),(427,129.20,'一室一厅','renting','2026-01-01 09:00:00.000000',85,2,'',2,'0201'),(428,117.19,'两室一厅','occupied','2026-01-01 09:00:00.000000',85,2,'',4,'0301'),(429,135.36,'一室一厅','renting','2026-01-01 09:00:00.000000',85,2,'',5,'0401'),(430,121.76,'四室两厅','occupied','2026-01-01 09:00:00.000000',85,2,'',1,'0501'),(431,150.62,'一室一厅','renting','2026-01-01 09:00:00.000000',86,1,'',3,'0101'),(432,165.97,'两室一厅','renting','2026-01-01 09:00:00.000000',86,2,'',4,'0201'),(433,78.47,'四室两厅','occupied','2026-01-01 09:00:00.000000',86,2,'',3,'0301'),(434,166.78,'一室一厅','vacant','2026-01-01 09:00:00.000000',86,0,'',0,'0401'),(435,140.94,'四室两厅','renting','2026-01-01 09:00:00.000000',86,2,'',4,'0501'),(436,121.15,'四室两厅','renting','2026-01-01 09:00:00.000000',87,1,'',3,'0101'),(437,107.96,'两室一厅','vacant','2026-01-01 09:00:00.000000',87,0,'',0,'0201'),(438,167.35,'三室两厅','renting','2026-01-01 09:00:00.000000',87,1,'',2,'0301'),(439,122.79,'三室两厅','vacant','2026-01-01 09:00:00.000000',87,0,'',0,'0401'),(440,150.19,'两室一厅','vacant','2026-01-01 09:00:00.000000',87,0,'',0,'0501'),(441,135.46,'四室两厅','renting','2026-01-01 09:00:00.000000',88,2,'',5,'0101'),(442,121.46,'四室两厅','renting','2026-01-01 09:00:00.000000',88,2,'',5,'0201'),(443,119.17,'四室两厅','occupied','2026-01-01 09:00:00.000000',88,2,'',1,'0301'),(444,127.39,'四室两厅','occupied','2026-01-01 09:00:00.000000',88,2,'',3,'0401'),(445,101.89,'三室两厅','occupied','2026-01-01 09:00:00.000000',88,2,'',3,'0501'),(446,132.11,'一室一厅','occupied','2026-01-01 09:00:00.000000',89,2,'',4,'0101'),(447,122.07,'一室一厅','occupied','2026-01-01 09:00:00.000000',89,2,'',2,'0201'),(448,107.18,'四室两厅','occupied','2026-01-01 09:00:00.000000',89,2,'',5,'0301'),(449,74.75,'三室两厅','occupied','2026-01-01 09:00:00.000000',89,1,'',4,'0401'),(450,72.21,'一室一厅','occupied','2026-01-01 09:00:00.000000',89,1,'',1,'0501'),(451,112.30,'三室两厅','renting','2026-01-01 09:00:00.000000',90,1,'',2,'0101'),(452,113.63,'一室一厅','vacant','2026-01-01 09:00:00.000000',90,0,'',0,'0201'),(453,115.52,'三室两厅','occupied','2026-01-01 09:00:00.000000',90,2,'',3,'0301'),(454,115.50,'一室一厅','vacant','2026-01-01 09:00:00.000000',90,0,'',0,'0401'),(455,165.63,'两室一厅','renting','2026-01-01 09:00:00.000000',90,1,'',5,'0501'),(456,141.97,'四室两厅','repairing','2026-01-01 09:00:00.000000',91,1,'',2,'0101'),(457,76.90,'一室一厅','occupied','2026-01-01 09:00:00.000000',91,2,'',3,'0201'),(458,166.53,'一室一厅','occupied','2026-01-01 09:00:00.000000',91,2,'',1,'0301'),(459,100.43,'四室两厅','occupied','2026-01-01 09:00:00.000000',91,2,'',2,'0401'),(460,108.46,'一室一厅','renting','2026-01-01 09:00:00.000000',91,2,'',4,'0501'),(461,98.69,'一室一厅','occupied','2026-01-01 09:00:00.000000',92,1,'',2,'0101'),(462,84.53,'四室两厅','renting','2026-01-01 09:00:00.000000',92,2,'',2,'0201'),(463,115.87,'三室两厅','occupied','2026-01-01 09:00:00.000000',92,2,'',3,'0301'),(464,155.45,'一室一厅','renting','2026-01-01 09:00:00.000000',92,2,'',2,'0401'),(465,125.14,'两室一厅','occupied','2026-01-01 09:00:00.000000',92,1,'',5,'0501'),(466,98.91,'三室两厅','renting','2026-01-01 09:00:00.000000',93,1,'',1,'0101'),(467,150.96,'两室一厅','occupied','2026-01-01 09:00:00.000000',93,1,'',5,'0201'),(468,159.90,'三室两厅','vacant','2026-01-01 09:00:00.000000',93,0,'',0,'0301'),(469,137.58,'三室两厅','repairing','2026-01-01 09:00:00.000000',93,2,'',3,'0401'),(470,75.33,'两室一厅','renting','2026-01-01 09:00:00.000000',93,2,'',4,'0501'),(471,153.03,'两室一厅','occupied','2026-01-01 09:00:00.000000',94,1,'',3,'0101'),(472,70.38,'四室两厅','occupied','2026-01-01 09:00:00.000000',94,2,'',2,'0201'),(473,104.89,'四室两厅','vacant','2026-01-01 09:00:00.000000',94,0,'',0,'0301'),(474,85.99,'两室一厅','renting','2026-01-01 09:00:00.000000',94,2,'',5,'0401'),(475,103.85,'四室两厅','renting','2026-01-01 09:00:00.000000',94,1,'',2,'0501'),(476,148.95,'三室两厅','vacant','2026-01-01 09:00:00.000000',95,0,'',0,'0101'),(477,82.62,'三室两厅','renting','2026-01-01 09:00:00.000000',95,2,'',3,'0201'),(478,110.95,'两室一厅','occupied','2026-01-01 09:00:00.000000',95,1,'',5,'0301'),(479,73.10,'一室一厅','repairing','2026-01-01 09:00:00.000000',95,1,'',4,'0401'),(480,99.21,'四室两厅','occupied','2026-01-01 09:00:00.000000',95,2,'',3,'0501'),(481,144.59,'两室一厅','occupied','2026-01-01 09:00:00.000000',96,1,'',3,'0101'),(482,72.82,'三室两厅','renting','2026-01-01 09:00:00.000000',96,1,'',4,'0201'),(483,93.59,'两室一厅','renting','2026-01-01 09:00:00.000000',96,1,'',2,'0301'),(484,118.26,'一室一厅','occupied','2026-01-01 09:00:00.000000',96,1,'',3,'0401'),(485,137.36,'两室一厅','vacant','2026-01-01 09:00:00.000000',96,0,'',0,'0501'),(486,82.29,'三室两厅','occupied','2026-01-01 09:00:00.000000',97,2,'',2,'0101'),(487,99.14,'四室两厅','renting','2026-01-01 09:00:00.000000',97,2,'',3,'0201'),(488,94.88,'三室两厅','occupied','2026-01-01 09:00:00.000000',97,1,'',5,'0301'),(489,158.02,'两室一厅','renting','2026-01-01 09:00:00.000000',97,2,'',5,'0401'),(490,141.58,'一室一厅','renting','2026-01-01 09:00:00.000000',97,1,'',4,'0501'),(491,143.84,'两室一厅','occupied','2026-01-01 09:00:00.000000',98,2,'',1,'0101'),(492,137.04,'四室两厅','occupied','2026-01-01 09:00:00.000000',98,1,'',2,'0201'),(493,104.43,'一室一厅','renting','2026-01-01 09:00:00.000000',98,2,'',5,'0301'),(494,99.59,'三室两厅','occupied','2026-01-01 09:00:00.000000',98,2,'',1,'0401'),(495,141.40,'两室一厅','vacant','2026-01-01 09:00:00.000000',98,0,'',0,'0501'),(496,145.49,'一室一厅','renting','2026-01-01 09:00:00.000000',99,2,'',4,'0101'),(497,82.54,'四室两厅','occupied','2026-01-01 09:00:00.000000',99,1,'',3,'0201'),(498,100.60,'两室一厅','occupied','2026-01-01 09:00:00.000000',99,1,'',4,'0301'),(499,70.66,'一室一厅','vacant','2026-01-01 09:00:00.000000',99,0,'',0,'0401'),(500,121.78,'两室一厅','repairing','2026-01-01 09:00:00.000000',99,2,'',4,'0501'),(501,81.17,'两室一厅','occupied','2026-01-01 09:00:00.000000',100,2,'',3,'0101'),(502,117.36,'一室一厅','repairing','2026-01-01 09:00:00.000000',100,2,'',5,'0201'),(503,94.67,'三室两厅','vacant','2026-01-01 09:00:00.000000',100,0,'',0,'0301'),(504,137.36,'两室一厅','vacant','2026-01-01 09:00:00.000000',100,0,'',0,'0401'),(505,108.53,'三室两厅','occupied','2026-01-01 09:00:00.000000',100,1,'',2,'0501'),(506,163.06,'三室两厅','vacant','2026-01-01 09:00:00.000000',101,0,'',0,'0101'),(507,83.01,'三室两厅','vacant','2026-01-01 09:00:00.000000',101,0,'',0,'0201'),(508,116.42,'四室两厅','occupied','2026-01-01 09:00:00.000000',101,2,'',2,'0301'),(509,70.11,'三室两厅','occupied','2026-01-01 09:00:00.000000',101,1,'',5,'0401'),(510,121.95,'两室一厅','occupied','2026-01-01 09:00:00.000000',101,1,'',5,'0501'),(511,149.88,'四室两厅','occupied','2026-01-01 09:00:00.000000',102,1,'',4,'0101'),(512,71.72,'一室一厅','vacant','2026-01-01 09:00:00.000000',102,0,'',0,'0201'),(513,112.83,'一室一厅','occupied','2026-01-01 09:00:00.000000',102,2,'',1,'0301'),(514,107.48,'三室两厅','occupied','2026-01-01 09:00:00.000000',102,2,'',4,'0401'),(515,158.52,'两室一厅','renting','2026-01-01 09:00:00.000000',102,2,'',5,'0501'),(516,117.92,'四室两厅','occupied','2026-01-01 09:00:00.000000',103,1,'',4,'0101'),(517,138.76,'两室一厅','occupied','2026-01-01 09:00:00.000000',103,1,'',3,'0201'),(518,87.12,'一室一厅','occupied','2026-01-01 09:00:00.000000',103,2,'',4,'0301'),(519,86.06,'三室两厅','occupied','2026-01-01 09:00:00.000000',103,1,'',4,'0401'),(520,94.67,'三室两厅','occupied','2026-01-01 09:00:00.000000',103,1,'',3,'0501'),(521,117.25,'四室两厅','occupied','2026-01-01 09:00:00.000000',104,1,'',2,'0101'),(522,96.32,'四室两厅','occupied','2026-01-01 09:00:00.000000',104,1,'',4,'0201'),(523,136.59,'四室两厅','occupied','2026-01-01 09:00:00.000000',104,2,'',3,'0301'),(524,77.48,'两室一厅','renting','2026-01-01 09:00:00.000000',104,1,'',5,'0401'),(525,89.11,'三室两厅','occupied','2026-01-01 09:00:00.000000',104,1,'',1,'0501'),(526,99.07,'一室一厅','occupied','2026-01-01 09:00:00.000000',105,2,'',5,'0101'),(527,105.25,'四室两厅','occupied','2026-01-01 09:00:00.000000',105,2,'',5,'0201'),(528,70.15,'两室一厅','occupied','2026-01-01 09:00:00.000000',105,2,'',3,'0301'),(529,166.60,'两室一厅','occupied','2026-01-01 09:00:00.000000',105,1,'',4,'0401'),(530,109.98,'四室两厅','occupied','2026-01-01 09:00:00.000000',105,1,'',2,'0501'),(531,136.53,'三室两厅','occupied','2026-01-01 09:00:00.000000',106,2,'',4,'0101'),(532,79.14,'四室两厅','occupied','2026-01-01 09:00:00.000000',106,2,'',2,'0201'),(533,151.61,'一室一厅','vacant','2026-01-01 09:00:00.000000',106,0,'',0,'0301'),(534,81.95,'四室两厅','occupied','2026-01-01 09:00:00.000000',106,1,'',4,'0401'),(535,162.82,'四室两厅','occupied','2026-01-01 09:00:00.000000',106,2,'',2,'0501'),(536,112.67,'四室两厅','occupied','2026-01-01 09:00:00.000000',107,2,'',5,'0101'),(537,75.25,'一室一厅','occupied','2026-01-01 09:00:00.000000',107,2,'',2,'0201'),(538,110.93,'三室两厅','occupied','2026-01-01 09:00:00.000000',107,1,'',5,'0301'),(539,167.32,'两室一厅','vacant','2026-01-01 09:00:00.000000',107,0,'',0,'0401'),(540,149.02,'四室两厅','renting','2026-01-01 09:00:00.000000',107,2,'',5,'0501'),(541,96.94,'三室两厅','occupied','2026-01-01 09:00:00.000000',108,1,'',2,'0101'),(542,103.81,'三室两厅','occupied','2026-01-01 09:00:00.000000',108,1,'',1,'0201'),(543,112.63,'一室一厅','repairing','2026-01-01 09:00:00.000000',108,2,'',5,'0301'),(544,117.70,'三室两厅','occupied','2026-01-01 09:00:00.000000',108,2,'',5,'0401'),(545,162.23,'四室两厅','repairing','2026-01-01 09:00:00.000000',108,2,'',2,'0501'),(546,166.89,'两室一厅','renting','2026-01-01 09:00:00.000000',109,2,'',1,'0101'),(547,102.99,'四室两厅','vacant','2026-01-01 09:00:00.000000',109,0,'',0,'0201'),(548,72.68,'四室两厅','occupied','2026-01-01 09:00:00.000000',109,1,'',5,'0301'),(549,99.40,'四室两厅','occupied','2026-01-01 09:00:00.000000',109,1,'',3,'0401'),(550,72.75,'一室一厅','renting','2026-01-01 09:00:00.000000',109,2,'',4,'0501'),(551,140.47,'四室两厅','occupied','2026-01-01 09:00:00.000000',110,1,'',3,'0101'),(552,137.32,'两室一厅','occupied','2026-01-01 09:00:00.000000',110,2,'',2,'0201'),(553,164.38,'两室一厅','occupied','2026-01-01 09:00:00.000000',110,2,'',5,'0301'),(554,79.48,'四室两厅','occupied','2026-01-01 09:00:00.000000',110,1,'',4,'0401'),(555,97.74,'三室两厅','occupied','2026-01-01 09:00:00.000000',110,1,'',5,'0501'),(556,137.49,'两室一厅','vacant','2026-01-01 09:00:00.000000',111,0,'',0,'0101'),(557,166.22,'两室一厅','occupied','2026-01-01 09:00:00.000000',111,1,'',3,'0201'),(558,143.11,'四室两厅','vacant','2026-01-01 09:00:00.000000',111,0,'',0,'0301'),(559,110.27,'两室一厅','vacant','2026-01-01 09:00:00.000000',111,0,'',0,'0401'),(560,96.68,'一室一厅','occupied','2026-01-01 09:00:00.000000',111,2,'',2,'0501'),(561,108.54,'一室一厅','occupied','2026-01-01 09:00:00.000000',112,2,'',4,'0101'),(562,143.14,'一室一厅','repairing','2026-01-01 09:00:00.000000',112,1,'',1,'0201'),(563,94.16,'两室一厅','vacant','2026-01-01 09:00:00.000000',112,0,'',0,'0301'),(564,159.56,'四室两厅','renting','2026-01-01 09:00:00.000000',112,2,'',4,'0401'),(565,104.63,'三室两厅','vacant','2026-01-01 09:00:00.000000',112,0,'',0,'0501'),(566,72.39,'三室两厅','renting','2026-01-01 09:00:00.000000',113,2,'',4,'0101'),(567,113.15,'一室一厅','occupied','2026-01-01 09:00:00.000000',113,2,'',5,'0201'),(568,71.62,'一室一厅','vacant','2026-01-01 09:00:00.000000',113,0,'',0,'0301'),(569,72.42,'两室一厅','repairing','2026-01-01 09:00:00.000000',113,1,'',1,'0401'),(570,73.98,'四室两厅','occupied','2026-01-01 09:00:00.000000',113,2,'',4,'0501'),(571,76.15,'两室一厅','renting','2026-01-01 09:00:00.000000',114,2,'',4,'0101'),(572,156.05,'一室一厅','renting','2026-01-01 09:00:00.000000',114,2,'',2,'0201'),(573,136.90,'一室一厅','occupied','2026-01-01 09:00:00.000000',114,1,'',2,'0301'),(574,108.11,'三室两厅','occupied','2026-01-01 09:00:00.000000',114,1,'',3,'0401'),(575,155.20,'一室一厅','occupied','2026-01-01 09:00:00.000000',114,2,'',1,'0501'),(576,166.47,'一室一厅','renting','2026-01-01 09:00:00.000000',115,1,'',2,'0101'),(577,137.51,'两室一厅','occupied','2026-01-01 09:00:00.000000',115,2,'',1,'0201'),(578,151.72,'两室一厅','occupied','2026-01-01 09:00:00.000000',115,2,'',5,'0301'),(579,138.60,'四室两厅','occupied','2026-01-01 09:00:00.000000',115,2,'',1,'0401'),(580,135.23,'四室两厅','renting','2026-01-01 09:00:00.000000',115,1,'',3,'0501'),(581,104.40,'三室两厅','occupied','2026-01-01 09:00:00.000000',116,1,'',4,'0101'),(582,137.92,'一室一厅','occupied','2026-01-01 09:00:00.000000',116,1,'',2,'0201'),(583,80.20,'一室一厅','occupied','2026-01-01 09:00:00.000000',116,2,'',2,'0301'),(584,88.71,'两室一厅','renting','2026-01-01 09:00:00.000000',116,2,'',5,'0401'),(585,132.49,'两室一厅','occupied','2026-01-01 09:00:00.000000',116,2,'',2,'0501'),(586,153.51,'三室两厅','vacant','2026-01-01 09:00:00.000000',117,0,'',0,'0101'),(587,78.88,'三室两厅','repairing','2026-01-01 09:00:00.000000',117,1,'',5,'0201'),(588,142.70,'两室一厅','occupied','2026-01-01 09:00:00.000000',117,2,'',3,'0301'),(589,167.11,'两室一厅','renting','2026-01-01 09:00:00.000000',117,1,'',1,'0401'),(590,99.73,'一室一厅','occupied','2026-01-01 09:00:00.000000',117,2,'',2,'0501'),(591,69.41,'四室两厅','renting','2026-01-01 09:00:00.000000',118,1,'',3,'0101'),(592,142.13,'三室两厅','occupied','2026-01-01 09:00:00.000000',118,2,'',1,'0201'),(593,87.37,'两室一厅','occupied','2026-01-01 09:00:00.000000',118,2,'',3,'0301'),(594,166.70,'一室一厅','renting','2026-01-01 09:00:00.000000',118,1,'',1,'0401'),(595,109.07,'三室两厅','occupied','2026-01-01 09:00:00.000000',118,1,'',5,'0501'),(596,94.35,'三室两厅','vacant','2026-01-01 09:00:00.000000',119,0,'',0,'0101'),(597,157.40,'一室一厅','occupied','2026-01-01 09:00:00.000000',119,1,'',4,'0201'),(598,75.32,'四室两厅','occupied','2026-01-01 09:00:00.000000',119,1,'',1,'0301'),(599,123.04,'三室两厅','occupied','2026-01-01 09:00:00.000000',119,2,'',5,'0401'),(600,131.37,'两室一厅','occupied','2026-01-01 09:00:00.000000',119,2,'',1,'0501'),(601,95.44,'两室一厅','vacant','2026-01-01 09:00:00.000000',120,0,'',0,'0101'),(602,142.74,'三室两厅','occupied','2026-01-01 09:00:00.000000',120,2,'',2,'0201'),(603,161.50,'一室一厅','vacant','2026-01-01 09:00:00.000000',120,0,'',0,'0301'),(604,127.16,'四室两厅','occupied','2026-01-01 09:00:00.000000',120,1,'',3,'0401'),(605,122.57,'三室两厅','occupied','2026-01-01 09:00:00.000000',120,1,'',1,'0501'),(606,152.84,'一室一厅','renting','2026-01-01 09:00:00.000000',121,2,'',5,'0101'),(607,165.64,'两室一厅','vacant','2026-01-01 09:00:00.000000',121,0,'',0,'0201'),(608,101.83,'一室一厅','occupied','2026-01-01 09:00:00.000000',121,1,'',5,'0301'),(609,151.76,'一室一厅','renting','2026-01-01 09:00:00.000000',121,2,'',2,'0401'),(610,72.19,'三室两厅','occupied','2026-01-01 09:00:00.000000',121,2,'',5,'0501'),(611,83.48,'四室两厅','renting','2026-01-01 09:00:00.000000',122,2,'',1,'0101'),(612,106.19,'两室一厅','vacant','2026-01-01 09:00:00.000000',122,0,'',0,'0201'),(613,97.92,'三室两厅','occupied','2026-01-01 09:00:00.000000',122,2,'',1,'0301'),(614,91.06,'一室一厅','occupied','2026-01-01 09:00:00.000000',122,2,'',2,'0401'),(615,73.98,'四室两厅','repairing','2026-01-01 09:00:00.000000',122,1,'',5,'0501'),(616,100.35,'一室一厅','occupied','2026-01-01 09:00:00.000000',123,2,'',1,'0101'),(617,139.72,'四室两厅','occupied','2026-01-01 09:00:00.000000',123,2,'',2,'0201'),(618,128.49,'一室一厅','repairing','2026-01-01 09:00:00.000000',123,1,'',1,'0301'),(619,113.24,'两室一厅','renting','2026-01-01 09:00:00.000000',123,1,'',4,'0401'),(620,81.16,'一室一厅','occupied','2026-01-01 09:00:00.000000',123,2,'',5,'0501'),(621,95.77,'两室一厅','vacant','2026-01-01 09:00:00.000000',124,0,'',0,'0101'),(622,133.29,'一室一厅','renting','2026-01-01 09:00:00.000000',124,1,'',2,'0201'),(623,68.50,'三室两厅','occupied','2026-01-01 09:00:00.000000',124,1,'',4,'0301'),(624,141.40,'一室一厅','vacant','2026-01-01 09:00:00.000000',124,0,'',0,'0401'),(625,120.25,'一室一厅','occupied','2026-01-01 09:00:00.000000',124,1,'',4,'0501'),(626,159.03,'两室一厅','renting','2026-01-01 09:00:00.000000',125,1,'',2,'0101'),(627,150.97,'四室两厅','occupied','2026-01-01 09:00:00.000000',125,2,'',3,'0201'),(628,134.55,'四室两厅','occupied','2026-01-01 09:00:00.000000',125,2,'',1,'0301'),(629,124.55,'一室一厅','occupied','2026-01-01 09:00:00.000000',125,1,'',2,'0401'),(630,140.31,'三室两厅','occupied','2026-01-01 09:00:00.000000',125,2,'',2,'0501'),(631,150.02,'一室一厅','occupied','2026-01-01 09:00:00.000000',126,2,'',1,'0101'),(632,71.22,'两室一厅','renting','2026-01-01 09:00:00.000000',126,1,'',1,'0201'),(633,96.96,'两室一厅','occupied','2026-01-01 09:00:00.000000',126,1,'',3,'0301'),(634,129.79,'四室两厅','repairing','2026-01-01 09:00:00.000000',126,2,'',1,'0401'),(635,114.82,'一室一厅','occupied','2026-01-01 09:00:00.000000',126,2,'',3,'0501'),(636,104.01,'一室一厅','occupied','2026-01-01 09:00:00.000000',127,1,'',5,'0101'),(637,101.99,'两室一厅','occupied','2026-01-01 09:00:00.000000',127,1,'',1,'0201'),(638,140.99,'三室两厅','repairing','2026-01-01 09:00:00.000000',127,1,'',4,'0301'),(639,78.02,'三室两厅','occupied','2026-01-01 09:00:00.000000',127,1,'',5,'0401'),(640,162.93,'四室两厅','occupied','2026-01-01 09:00:00.000000',127,1,'',2,'0501'),(641,154.15,'四室两厅','occupied','2026-01-01 09:00:00.000000',128,2,'',3,'0101'),(642,150.76,'两室一厅','occupied','2026-01-01 09:00:00.000000',128,2,'',4,'0201'),(643,78.94,'一室一厅','vacant','2026-01-01 09:00:00.000000',128,0,'',0,'0301'),(644,110.82,'四室两厅','renting','2026-01-01 09:00:00.000000',128,1,'',4,'0401'),(645,105.84,'四室两厅','occupied','2026-01-01 09:00:00.000000',128,2,'',2,'0501'),(646,101.00,'四室两厅','vacant','2026-01-01 09:00:00.000000',129,0,'',0,'0101'),(647,73.46,'四室两厅','occupied','2026-01-01 09:00:00.000000',129,2,'',5,'0201'),(648,103.68,'两室一厅','occupied','2026-01-01 09:00:00.000000',129,2,'',5,'0301'),(649,87.12,'两室一厅','renting','2026-01-01 09:00:00.000000',129,2,'',5,'0401'),(650,96.54,'四室两厅','vacant','2026-01-01 09:00:00.000000',129,0,'',0,'0501'),(651,101.64,'两室一厅','renting','2026-01-01 09:00:00.000000',130,2,'',1,'0101'),(652,145.25,'两室一厅','occupied','2026-01-01 09:00:00.000000',130,2,'',1,'0201'),(653,89.16,'两室一厅','renting','2026-01-01 09:00:00.000000',130,2,'',1,'0301'),(654,78.34,'一室一厅','occupied','2026-01-01 09:00:00.000000',130,2,'',1,'0401'),(655,156.40,'三室两厅','occupied','2026-01-01 09:00:00.000000',130,1,'',5,'0501'),(656,116.89,'三室两厅','occupied','2026-01-01 09:00:00.000000',131,1,'',2,'0101'),(657,160.30,'两室一厅','occupied','2026-01-01 09:00:00.000000',131,1,'',2,'0201'),(658,155.68,'一室一厅','occupied','2026-01-01 09:00:00.000000',131,1,'',1,'0301'),(659,129.48,'一室一厅','vacant','2026-01-01 09:00:00.000000',131,0,'',0,'0401'),(660,112.37,'四室两厅','repairing','2026-01-01 09:00:00.000000',131,1,'',2,'0501'),(661,116.58,'四室两厅','occupied','2026-01-01 09:00:00.000000',132,1,'',1,'0101'),(662,167.60,'三室两厅','vacant','2026-01-01 09:00:00.000000',132,0,'',0,'0201'),(663,140.42,'三室两厅','vacant','2026-01-01 09:00:00.000000',132,0,'',0,'0301'),(664,151.08,'四室两厅','occupied','2026-01-01 09:00:00.000000',132,2,'',5,'0401'),(665,101.89,'一室一厅','occupied','2026-01-01 09:00:00.000000',132,2,'',2,'0501'),(666,103.99,'四室两厅','renting','2026-01-01 09:00:00.000000',133,2,'',5,'0101'),(667,94.69,'两室一厅','vacant','2026-01-01 09:00:00.000000',133,0,'',0,'0201'),(668,131.44,'两室一厅','occupied','2026-01-01 09:00:00.000000',133,1,'',4,'0301'),(669,101.13,'三室两厅','occupied','2026-01-01 09:00:00.000000',133,2,'',3,'0401'),(670,144.79,'三室两厅','renting','2026-01-01 09:00:00.000000',133,1,'',2,'0501'),(671,92.09,'四室两厅','repairing','2026-01-01 09:00:00.000000',134,1,'',4,'0101'),(672,91.40,'一室一厅','occupied','2026-01-01 09:00:00.000000',134,2,'',5,'0201'),(673,73.07,'三室两厅','occupied','2026-01-01 09:00:00.000000',134,2,'',2,'0301'),(674,124.61,'四室两厅','occupied','2026-01-01 09:00:00.000000',134,2,'',2,'0401'),(675,152.20,'一室一厅','occupied','2026-01-01 09:00:00.000000',134,1,'',2,'0501'),(676,161.51,'四室两厅','occupied','2026-01-01 09:00:00.000000',135,1,'',5,'0101'),(677,76.70,'三室两厅','repairing','2026-01-01 09:00:00.000000',135,1,'',1,'0201'),(678,137.20,'一室一厅','renting','2026-01-01 09:00:00.000000',135,2,'',5,'0301'),(679,72.30,'两室一厅','occupied','2026-01-01 09:00:00.000000',135,1,'',3,'0401'),(680,128.07,'两室一厅','vacant','2026-01-01 09:00:00.000000',135,0,'',0,'0501'),(681,157.34,'一室一厅','vacant','2026-01-01 09:00:00.000000',136,0,'',0,'0101'),(682,98.98,'三室两厅','occupied','2026-01-01 09:00:00.000000',136,2,'',3,'0201'),(683,161.26,'四室两厅','repairing','2026-01-01 09:00:00.000000',136,2,'',1,'0301'),(684,162.51,'四室两厅','vacant','2026-01-01 09:00:00.000000',136,0,'',0,'0401'),(685,94.96,'三室两厅','occupied','2026-01-01 09:00:00.000000',136,1,'',1,'0501'),(686,104.00,'三室两厅','occupied','2026-01-01 09:00:00.000000',137,1,'',3,'0101'),(687,90.73,'三室两厅','vacant','2026-01-01 09:00:00.000000',137,0,'',0,'0201'),(688,98.33,'两室一厅','vacant','2026-01-01 09:00:00.000000',137,0,'',0,'0301'),(689,76.49,'三室两厅','vacant','2026-01-01 09:00:00.000000',137,0,'',0,'0401'),(690,69.20,'两室一厅','occupied','2026-01-01 09:00:00.000000',137,2,'',5,'0501'),(691,148.49,'四室两厅','occupied','2026-01-01 09:00:00.000000',138,1,'',3,'0101'),(692,121.32,'一室一厅','repairing','2026-01-01 09:00:00.000000',138,1,'',1,'0201'),(693,81.28,'三室两厅','vacant','2026-01-01 09:00:00.000000',138,0,'',0,'0301'),(694,115.78,'三室两厅','renting','2026-01-01 09:00:00.000000',138,2,'',5,'0401'),(695,118.25,'四室两厅','renting','2026-01-01 09:00:00.000000',138,1,'',2,'0501'),(696,115.44,'三室两厅','occupied','2026-01-01 09:00:00.000000',139,2,'',5,'0101'),(697,165.78,'四室两厅','occupied','2026-01-01 09:00:00.000000',139,2,'',5,'0201'),(698,126.42,'四室两厅','occupied','2026-01-01 09:00:00.000000',139,1,'',1,'0301'),(699,96.11,'四室两厅','occupied','2026-01-01 09:00:00.000000',139,1,'',5,'0401'),(700,126.58,'一室一厅','vacant','2026-01-01 09:00:00.000000',139,0,'',0,'0501'),(701,140.92,'四室两厅','occupied','2026-01-01 09:00:00.000000',140,2,'',5,'0101'),(702,160.50,'一室一厅','repairing','2026-01-01 09:00:00.000000',140,2,'',4,'0201'),(703,124.42,'一室一厅','occupied','2026-01-01 09:00:00.000000',140,2,'',5,'0301'),(704,87.77,'一室一厅','occupied','2026-01-01 09:00:00.000000',140,2,'',2,'0401'),(705,151.59,'四室两厅','occupied','2026-01-01 09:00:00.000000',140,1,'',3,'0501'),(706,108.62,'三室两厅','occupied','2026-01-01 09:00:00.000000',141,2,'',1,'0101'),(707,74.01,'四室两厅','occupied','2026-01-01 09:00:00.000000',141,1,'',3,'0201'),(708,142.23,'一室一厅','repairing','2026-01-01 09:00:00.000000',141,1,'',3,'0301'),(709,104.41,'一室一厅','repairing','2026-01-01 09:00:00.000000',141,2,'',2,'0401'),(710,89.26,'四室两厅','renting','2026-01-01 09:00:00.000000',141,2,'',1,'0501'),(711,129.83,'一室一厅','occupied','2026-01-01 09:00:00.000000',142,1,'',5,'0101'),(712,91.57,'一室一厅','renting','2026-01-01 09:00:00.000000',142,1,'',4,'0201'),(713,126.46,'两室一厅','occupied','2026-01-01 09:00:00.000000',142,2,'',2,'0301'),(714,161.07,'四室两厅','repairing','2026-01-01 09:00:00.000000',142,2,'',5,'0401'),(715,114.89,'两室一厅','occupied','2026-01-01 09:00:00.000000',142,2,'',3,'0501'),(716,140.38,'四室两厅','vacant','2026-01-01 09:00:00.000000',143,0,'',0,'0101'),(717,153.62,'一室一厅','occupied','2026-01-01 09:00:00.000000',143,1,'',5,'0201'),(718,165.61,'四室两厅','occupied','2026-01-01 09:00:00.000000',143,2,'',1,'0301'),(719,90.85,'一室一厅','renting','2026-01-01 09:00:00.000000',143,1,'',2,'0401'),(720,79.58,'一室一厅','renting','2026-01-01 09:00:00.000000',143,2,'',1,'0501'),(721,152.95,'一室一厅','occupied','2026-01-01 09:00:00.000000',144,2,'',4,'0101'),(722,125.53,'三室两厅','occupied','2026-01-01 09:00:00.000000',144,1,'',1,'0201'),(723,127.16,'两室一厅','occupied','2026-01-01 09:00:00.000000',144,2,'',1,'0301'),(724,93.45,'三室两厅','occupied','2026-01-01 09:00:00.000000',144,1,'',1,'0401'),(725,69.88,'四室两厅','occupied','2026-01-01 09:00:00.000000',144,1,'',5,'0501'),(726,135.31,'三室两厅','occupied','2026-01-01 09:00:00.000000',145,1,'',5,'0101'),(727,110.14,'一室一厅','vacant','2026-01-01 09:00:00.000000',145,0,'',0,'0201'),(728,147.32,'两室一厅','occupied','2026-01-01 09:00:00.000000',145,2,'',5,'0301'),(729,110.57,'四室两厅','occupied','2026-01-01 09:00:00.000000',145,1,'',1,'0401'),(730,115.47,'四室两厅','occupied','2026-01-01 09:00:00.000000',145,2,'',3,'0501'),(731,145.41,'两室一厅','vacant','2026-01-01 09:00:00.000000',146,0,'',0,'0101'),(732,129.05,'一室一厅','occupied','2026-01-01 09:00:00.000000',146,2,'',5,'0201'),(733,120.58,'一室一厅','occupied','2026-01-01 09:00:00.000000',146,2,'',2,'0301'),(734,118.05,'三室两厅','renting','2026-01-01 09:00:00.000000',146,2,'',3,'0401'),(735,119.55,'一室一厅','occupied','2026-01-01 09:00:00.000000',146,1,'',5,'0501'),(736,132.85,'两室一厅','renting','2026-01-01 09:00:00.000000',147,1,'',2,'0101'),(737,87.63,'四室两厅','renting','2026-01-01 09:00:00.000000',147,2,'',3,'0201'),(738,100.43,'三室两厅','vacant','2026-01-01 09:00:00.000000',147,0,'',0,'0301'),(739,90.03,'两室一厅','occupied','2026-01-01 09:00:00.000000',147,1,'',3,'0401'),(740,77.44,'三室两厅','repairing','2026-01-01 09:00:00.000000',147,1,'',1,'0501'),(741,132.58,'三室两厅','vacant','2026-01-01 09:00:00.000000',148,0,'',0,'0101'),(742,89.26,'三室两厅','occupied','2026-01-01 09:00:00.000000',148,2,'',3,'0201'),(743,146.36,'两室一厅','occupied','2026-01-01 09:00:00.000000',148,1,'',5,'0301'),(744,88.65,'两室一厅','occupied','2026-01-01 09:00:00.000000',148,1,'',5,'0401'),(745,116.84,'一室一厅','occupied','2026-01-01 09:00:00.000000',148,2,'',1,'0501'),(746,85.48,'三室两厅','occupied','2026-01-01 09:00:00.000000',149,1,'',2,'0101'),(747,126.74,'两室一厅','vacant','2026-01-01 09:00:00.000000',149,0,'',0,'0201'),(748,69.83,'两室一厅','renting','2026-01-01 09:00:00.000000',149,2,'',2,'0301'),(749,126.09,'一室一厅','renting','2026-01-01 09:00:00.000000',149,2,'',5,'0401'),(750,144.36,'一室一厅','occupied','2026-01-01 09:00:00.000000',149,2,'',4,'0501'),(751,146.00,'两室一厅','occupied','2026-01-01 09:00:00.000000',150,2,'',2,'0101'),(752,121.84,'三室两厅','occupied','2026-01-01 09:00:00.000000',150,1,'',5,'0201'),(753,77.93,'两室一厅','occupied','2026-01-01 09:00:00.000000',150,2,'',1,'0301'),(754,161.62,'四室两厅','vacant','2026-01-01 09:00:00.000000',150,0,'',0,'0401'),(755,105.39,'一室一厅','occupied','2026-01-01 09:00:00.000000',150,2,'',4,'0501'),(756,97.59,'四室两厅','occupied','2026-01-01 09:00:00.000000',151,2,'',1,'0101'),(757,151.96,'三室两厅','occupied','2026-01-01 09:00:00.000000',151,2,'',1,'0201'),(758,105.99,'两室一厅','renting','2026-01-01 09:00:00.000000',151,2,'',3,'0301'),(759,109.69,'四室两厅','vacant','2026-01-01 09:00:00.000000',151,0,'',0,'0401'),(760,87.35,'四室两厅','occupied','2026-01-01 09:00:00.000000',151,2,'',1,'0501'),(761,157.18,'一室一厅','occupied','2026-01-01 09:00:00.000000',152,1,'',3,'0101'),(762,132.07,'两室一厅','occupied','2026-01-01 09:00:00.000000',152,1,'',1,'0201'),(763,89.15,'三室两厅','vacant','2026-01-01 09:00:00.000000',152,0,'',0,'0301'),(764,103.20,'四室两厅','occupied','2026-01-01 09:00:00.000000',152,2,'',3,'0401'),(765,77.93,'三室两厅','vacant','2026-01-01 09:00:00.000000',152,0,'',0,'0501'),(766,112.55,'四室两厅','occupied','2026-01-01 09:00:00.000000',153,1,'',5,'0101'),(767,129.17,'三室两厅','occupied','2026-01-01 09:00:00.000000',153,1,'',5,'0201'),(768,93.79,'一室一厅','occupied','2026-01-01 09:00:00.000000',153,1,'',4,'0301'),(769,101.17,'四室两厅','vacant','2026-01-01 09:00:00.000000',153,0,'',0,'0401'),(770,83.35,'一室一厅','renting','2026-01-01 09:00:00.000000',153,1,'',2,'0501'),(771,99.03,'两室一厅','vacant','2026-01-01 09:00:00.000000',154,0,'',0,'0101'),(772,83.54,'四室两厅','occupied','2026-01-01 09:00:00.000000',154,1,'',1,'0201'),(773,166.02,'两室一厅','occupied','2026-01-01 09:00:00.000000',154,1,'',4,'0301'),(774,164.03,'四室两厅','repairing','2026-01-01 09:00:00.000000',154,2,'',5,'0401'),(775,160.41,'一室一厅','occupied','2026-01-01 09:00:00.000000',154,2,'',5,'0501'),(776,115.10,'三室两厅','occupied','2026-01-01 09:00:00.000000',155,1,'',2,'0101'),(777,83.90,'三室两厅','occupied','2026-01-01 09:00:00.000000',155,2,'',5,'0201'),(778,80.37,'两室一厅','occupied','2026-01-01 09:00:00.000000',155,2,'',4,'0301'),(779,118.76,'四室两厅','repairing','2026-01-01 09:00:00.000000',155,2,'',4,'0401'),(780,132.61,'三室两厅','occupied','2026-01-01 09:00:00.000000',155,1,'',3,'0501'),(781,118.62,'两室一厅','vacant','2026-01-01 09:00:00.000000',156,0,'',0,'0101'),(782,142.61,'一室一厅','occupied','2026-01-01 09:00:00.000000',156,1,'',3,'0201'),(783,132.78,'三室两厅','occupied','2026-01-01 09:00:00.000000',156,2,'',2,'0301'),(784,156.66,'两室一厅','occupied','2026-01-01 09:00:00.000000',156,2,'',3,'0401'),(785,88.28,'一室一厅','occupied','2026-01-01 09:00:00.000000',156,2,'',2,'0501'),(786,92.52,'四室两厅','occupied','2026-01-01 09:00:00.000000',157,2,'',1,'0101'),(787,92.25,'一室一厅','renting','2026-01-01 09:00:00.000000',157,2,'',2,'0201'),(788,161.30,'一室一厅','vacant','2026-01-01 09:00:00.000000',157,0,'',0,'0301'),(789,133.16,'一室一厅','occupied','2026-01-01 09:00:00.000000',157,1,'',4,'0401'),(790,153.96,'一室一厅','renting','2026-01-01 09:00:00.000000',157,2,'',4,'0501'),(791,142.61,'三室两厅','renting','2026-01-01 09:00:00.000000',158,2,'',4,'0101'),(792,76.35,'两室一厅','occupied','2026-01-01 09:00:00.000000',158,1,'',4,'0201'),(793,101.65,'一室一厅','occupied','2026-01-01 09:00:00.000000',158,2,'',3,'0301'),(794,120.18,'三室两厅','renting','2026-01-01 09:00:00.000000',158,1,'',1,'0401'),(795,147.33,'两室一厅','occupied','2026-01-01 09:00:00.000000',158,2,'',1,'0501'),(796,131.92,'两室一厅','occupied','2026-01-01 09:00:00.000000',159,2,'',4,'0101'),(797,82.32,'两室一厅','vacant','2026-01-01 09:00:00.000000',159,0,'',0,'0201'),(798,157.24,'三室两厅','renting','2026-01-01 09:00:00.000000',159,2,'',5,'0301'),(799,76.71,'两室一厅','occupied','2026-01-01 09:00:00.000000',159,1,'',5,'0401'),(800,82.97,'两室一厅','occupied','2026-01-01 09:00:00.000000',159,2,'',5,'0501'),(801,135.67,'一室一厅','renting','2026-01-01 09:00:00.000000',160,2,'',3,'0101'),(802,98.23,'两室一厅','occupied','2026-01-01 09:00:00.000000',160,1,'',3,'0201'),(803,85.46,'一室一厅','renting','2026-01-01 09:00:00.000000',160,2,'',2,'0301'),(804,123.65,'三室两厅','renting','2026-01-01 09:00:00.000000',160,2,'',4,'0401'),(805,84.50,'一室一厅','occupied','2026-01-01 09:00:00.000000',160,2,'',5,'0501'),(806,140.05,'一室一厅','vacant','2026-01-01 09:00:00.000000',161,0,'',0,'0101'),(807,164.91,'一室一厅','occupied','2026-01-01 09:00:00.000000',161,2,'',4,'0201'),(808,77.13,'三室两厅','vacant','2026-01-01 09:00:00.000000',161,0,'',0,'0301'),(809,82.52,'两室一厅','occupied','2026-01-01 09:00:00.000000',161,2,'',5,'0401'),(810,87.14,'四室两厅','repairing','2026-01-01 09:00:00.000000',161,2,'',3,'0501'),(811,86.41,'两室一厅','renting','2026-01-01 09:00:00.000000',162,2,'',2,'0101'),(812,112.20,'一室一厅','occupied','2026-01-01 09:00:00.000000',162,1,'',4,'0201'),(813,81.67,'两室一厅','renting','2026-01-01 09:00:00.000000',162,1,'',3,'0301'),(814,122.55,'三室两厅','occupied','2026-01-01 09:00:00.000000',162,2,'',2,'0401'),(815,156.63,'四室两厅','occupied','2026-01-01 09:00:00.000000',162,2,'',3,'0501'),(816,98.92,'四室两厅','renting','2026-01-01 09:00:00.000000',163,2,'',2,'0101'),(817,90.84,'四室两厅','occupied','2026-01-01 09:00:00.000000',163,1,'',4,'0201'),(818,85.08,'两室一厅','occupied','2026-01-01 09:00:00.000000',163,1,'',2,'0301'),(819,129.14,'两室一厅','repairing','2026-01-01 09:00:00.000000',163,1,'',1,'0401'),(820,128.92,'三室两厅','occupied','2026-01-01 09:00:00.000000',163,1,'',3,'0501'),(821,115.99,'一室一厅','occupied','2026-01-01 09:00:00.000000',164,2,'',2,'0101'),(822,150.59,'四室两厅','renting','2026-01-01 09:00:00.000000',164,1,'',4,'0201'),(823,118.03,'两室一厅','occupied','2026-01-01 09:00:00.000000',164,2,'',2,'0301'),(824,141.96,'一室一厅','occupied','2026-01-01 09:00:00.000000',164,1,'',1,'0401'),(825,133.75,'三室两厅','vacant','2026-01-01 09:00:00.000000',164,0,'',0,'0501'),(826,156.76,'两室一厅','occupied','2026-01-01 09:00:00.000000',165,2,'',5,'0101'),(827,158.61,'一室一厅','occupied','2026-01-01 09:00:00.000000',165,1,'',3,'0201'),(828,135.40,'四室两厅','vacant','2026-01-01 09:00:00.000000',165,0,'',0,'0301'),(829,82.46,'一室一厅','vacant','2026-01-01 09:00:00.000000',165,0,'',0,'0401'),(830,109.82,'两室一厅','occupied','2026-01-01 09:00:00.000000',165,1,'',1,'0501'),(831,117.31,'两室一厅','occupied','2026-01-01 09:00:00.000000',166,2,'',3,'0101'),(832,123.43,'一室一厅','vacant','2026-01-01 09:00:00.000000',166,0,'',0,'0201'),(833,87.35,'一室一厅','vacant','2026-01-01 09:00:00.000000',166,0,'',0,'0301'),(834,92.70,'四室两厅','vacant','2026-01-01 09:00:00.000000',166,0,'',0,'0401'),(835,153.69,'两室一厅','vacant','2026-01-01 09:00:00.000000',166,0,'',0,'0501'),(836,81.87,'一室一厅','occupied','2026-01-01 09:00:00.000000',167,1,'',2,'0101'),(837,124.01,'四室两厅','occupied','2026-01-01 09:00:00.000000',167,2,'',4,'0201'),(838,149.32,'四室两厅','renting','2026-01-01 09:00:00.000000',167,1,'',2,'0301'),(839,104.74,'四室两厅','occupied','2026-01-01 09:00:00.000000',167,2,'',5,'0401'),(840,68.02,'一室一厅','occupied','2026-01-01 09:00:00.000000',167,1,'',3,'0501'),(841,88.60,'两室一厅','renting','2026-01-01 09:00:00.000000',168,2,'',5,'0101'),(842,150.20,'四室两厅','renting','2026-01-01 09:00:00.000000',168,2,'',1,'0201'),(843,119.97,'一室一厅','occupied','2026-01-01 09:00:00.000000',168,1,'',3,'0301'),(844,102.40,'两室一厅','occupied','2026-01-01 09:00:00.000000',168,1,'',4,'0401'),(845,104.81,'四室两厅','occupied','2026-01-01 09:00:00.000000',168,2,'',2,'0501'),(846,88.56,'一室一厅','renting','2026-01-01 09:00:00.000000',169,2,'',1,'0101'),(847,81.95,'三室两厅','vacant','2026-01-01 09:00:00.000000',169,0,'',0,'0201'),(848,130.82,'一室一厅','renting','2026-01-01 09:00:00.000000',169,2,'',3,'0301'),(849,77.16,'三室两厅','occupied','2026-01-01 09:00:00.000000',169,2,'',1,'0401'),(850,146.12,'一室一厅','repairing','2026-01-01 09:00:00.000000',169,2,'',1,'0501'),(851,117.91,'一室一厅','vacant','2026-01-01 09:00:00.000000',170,0,'',0,'0101'),(852,140.40,'三室两厅','occupied','2026-01-01 09:00:00.000000',170,1,'',1,'0201'),(853,93.95,'两室一厅','occupied','2026-01-01 09:00:00.000000',170,2,'',3,'0301'),(854,134.25,'三室两厅','occupied','2026-01-01 09:00:00.000000',170,2,'',5,'0401'),(855,79.84,'一室一厅','occupied','2026-01-01 09:00:00.000000',170,1,'',4,'0501'),(856,144.62,'两室一厅','occupied','2026-01-01 09:00:00.000000',171,2,'',3,'0101'),(857,122.39,'三室两厅','renting','2026-01-01 09:00:00.000000',171,2,'',2,'0201'),(858,158.86,'两室一厅','occupied','2026-01-01 09:00:00.000000',171,2,'',1,'0301'),(859,162.19,'两室一厅','occupied','2026-01-01 09:00:00.000000',171,2,'',2,'0401'),(860,94.11,'四室两厅','occupied','2026-01-01 09:00:00.000000',171,2,'',3,'0501'),(861,162.65,'四室两厅','vacant','2026-01-01 09:00:00.000000',172,0,'',0,'0101'),(862,93.34,'三室两厅','renting','2026-01-01 09:00:00.000000',172,2,'',4,'0201'),(863,80.08,'四室两厅','vacant','2026-01-01 09:00:00.000000',172,0,'',0,'0301'),(864,137.53,'四室两厅','occupied','2026-01-01 09:00:00.000000',172,1,'',4,'0401'),(865,120.69,'两室一厅','occupied','2026-01-01 09:00:00.000000',172,1,'',2,'0501'),(866,152.14,'两室一厅','occupied','2026-01-01 09:00:00.000000',173,2,'',1,'0101'),(867,102.87,'两室一厅','occupied','2026-01-01 09:00:00.000000',173,2,'',2,'0201'),(868,118.33,'三室两厅','occupied','2026-01-01 09:00:00.000000',173,1,'',3,'0301'),(869,156.49,'三室两厅','occupied','2026-01-01 09:00:00.000000',173,1,'',2,'0401'),(870,101.18,'两室一厅','renting','2026-01-01 09:00:00.000000',173,1,'',2,'0501'),(871,80.92,'四室两厅','repairing','2026-01-01 09:00:00.000000',174,2,'',4,'0101'),(872,106.20,'三室两厅','occupied','2026-01-01 09:00:00.000000',174,2,'',3,'0201'),(873,113.79,'四室两厅','occupied','2026-01-01 09:00:00.000000',174,2,'',4,'0301'),(874,81.36,'一室一厅','occupied','2026-01-01 09:00:00.000000',174,2,'',1,'0401'),(875,159.13,'两室一厅','renting','2026-01-01 09:00:00.000000',174,1,'',2,'0501'),(876,148.49,'四室两厅','occupied','2026-01-01 09:00:00.000000',175,2,'',1,'0101'),(877,116.15,'四室两厅','occupied','2026-01-01 09:00:00.000000',175,2,'',3,'0201'),(878,100.96,'一室一厅','occupied','2026-01-01 09:00:00.000000',175,1,'',1,'0301'),(879,120.89,'一室一厅','occupied','2026-01-01 09:00:00.000000',175,2,'',4,'0401'),(880,140.52,'一室一厅','vacant','2026-01-01 09:00:00.000000',175,0,'',0,'0501'),(881,131.11,'两室一厅','vacant','2026-01-01 09:00:00.000000',176,0,'',0,'0101'),(882,114.58,'两室一厅','occupied','2026-01-01 09:00:00.000000',176,1,'',3,'0201'),(883,77.67,'一室一厅','vacant','2026-01-01 09:00:00.000000',176,0,'',0,'0301'),(884,105.46,'四室两厅','occupied','2026-01-01 09:00:00.000000',176,2,'',5,'0401'),(885,104.72,'一室一厅','occupied','2026-01-01 09:00:00.000000',176,2,'',1,'0501'),(886,73.19,'两室一厅','occupied','2026-01-01 09:00:00.000000',177,1,'',2,'0101'),(887,151.77,'四室两厅','occupied','2026-01-01 09:00:00.000000',177,1,'',2,'0201'),(888,145.33,'一室一厅','vacant','2026-01-01 09:00:00.000000',177,0,'',0,'0301'),(889,156.42,'一室一厅','occupied','2026-01-01 09:00:00.000000',177,2,'',4,'0401'),(890,119.77,'一室一厅','repairing','2026-01-01 09:00:00.000000',177,2,'',3,'0501'),(891,115.14,'四室两厅','vacant','2026-01-01 09:00:00.000000',178,0,'',0,'0101'),(892,86.09,'三室两厅','vacant','2026-01-01 09:00:00.000000',178,0,'',0,'0201'),(893,152.60,'四室两厅','vacant','2026-01-01 09:00:00.000000',178,0,'',0,'0301'),(894,88.93,'一室一厅','vacant','2026-01-01 09:00:00.000000',178,0,'',0,'0401'),(895,127.52,'三室两厅','renting','2026-01-01 09:00:00.000000',178,1,'',2,'0501'),(896,69.23,'四室两厅','renting','2026-01-01 09:00:00.000000',179,2,'',4,'0101'),(897,104.71,'四室两厅','occupied','2026-01-01 09:00:00.000000',179,2,'',3,'0201'),(898,73.89,'一室一厅','occupied','2026-01-01 09:00:00.000000',179,2,'',5,'0301'),(899,103.01,'一室一厅','occupied','2026-01-01 09:00:00.000000',179,2,'',1,'0401'),(900,167.74,'两室一厅','occupied','2026-01-01 09:00:00.000000',179,2,'',4,'0501'),(901,140.46,'一室一厅','occupied','2026-01-01 09:00:00.000000',180,1,'',3,'0101'),(902,115.16,'四室两厅','occupied','2026-01-01 09:00:00.000000',180,2,'',3,'0201'),(903,85.28,'两室一厅','occupied','2026-01-01 09:00:00.000000',180,1,'',3,'0301'),(904,142.68,'三室两厅','renting','2026-01-01 09:00:00.000000',180,2,'',4,'0401'),(905,101.00,'两室一厅','occupied','2026-01-01 09:00:00.000000',180,2,'',4,'0501'),(906,123.45,'四室两厅','vacant','2026-01-01 09:00:00.000000',181,0,'',0,'0101'),(907,85.07,'四室两厅','vacant','2026-01-01 09:00:00.000000',181,0,'',0,'0201'),(908,109.28,'四室两厅','vacant','2026-01-01 09:00:00.000000',181,0,'',0,'0301'),(909,83.23,'四室两厅','occupied','2026-01-01 09:00:00.000000',181,2,'',2,'0401'),(910,151.05,'三室两厅','repairing','2026-01-01 09:00:00.000000',181,1,'',4,'0501'),(911,89.56,'四室两厅','occupied','2026-01-01 09:00:00.000000',182,1,'',4,'0101'),(912,82.23,'四室两厅','occupied','2026-01-01 09:00:00.000000',182,1,'',2,'0201'),(913,141.21,'一室一厅','vacant','2026-01-01 09:00:00.000000',182,0,'',0,'0301'),(914,87.51,'三室两厅','occupied','2026-01-01 09:00:00.000000',182,2,'',1,'0401'),(915,88.20,'两室一厅','occupied','2026-01-01 09:00:00.000000',182,1,'',5,'0501'),(916,69.56,'一室一厅','vacant','2026-01-01 09:00:00.000000',183,0,'',0,'0101'),(917,137.38,'一室一厅','occupied','2026-01-01 09:00:00.000000',183,2,'',1,'0201'),(918,111.63,'两室一厅','occupied','2026-01-01 09:00:00.000000',183,1,'',5,'0301'),(919,121.45,'两室一厅','occupied','2026-01-01 09:00:00.000000',183,2,'',3,'0401'),(920,80.47,'两室一厅','repairing','2026-01-01 09:00:00.000000',183,1,'',4,'0501'),(921,148.67,'两室一厅','occupied','2026-01-01 09:00:00.000000',184,2,'',2,'0101'),(922,78.68,'三室两厅','occupied','2026-01-01 09:00:00.000000',184,2,'',5,'0201'),(923,162.11,'两室一厅','occupied','2026-01-01 09:00:00.000000',184,2,'',3,'0301'),(924,71.69,'四室两厅','vacant','2026-01-01 09:00:00.000000',184,0,'',0,'0401'),(925,110.15,'一室一厅','occupied','2026-01-01 09:00:00.000000',184,1,'',3,'0501'),(926,110.34,'一室一厅','occupied','2026-01-01 09:00:00.000000',185,2,'',3,'0101'),(927,76.76,'两室一厅','occupied','2026-01-01 09:00:00.000000',185,2,'',4,'0201'),(928,137.11,'一室一厅','vacant','2026-01-01 09:00:00.000000',185,0,'',0,'0301'),(929,146.89,'四室两厅','occupied','2026-01-01 09:00:00.000000',185,1,'',2,'0401'),(930,83.56,'三室两厅','occupied','2026-01-01 09:00:00.000000',185,2,'',4,'0501'),(931,144.11,'三室两厅','occupied','2026-01-01 09:00:00.000000',186,2,'',5,'0101'),(932,81.13,'四室两厅','occupied','2026-01-01 09:00:00.000000',186,1,'',4,'0201'),(933,116.35,'三室两厅','occupied','2026-01-01 09:00:00.000000',186,1,'',5,'0301'),(934,83.26,'两室一厅','occupied','2026-01-01 09:00:00.000000',186,1,'',3,'0401'),(935,93.18,'一室一厅','renting','2026-01-01 09:00:00.000000',186,2,'',1,'0501'),(936,80.29,'三室两厅','vacant','2026-01-01 09:00:00.000000',187,0,'',0,'0101'),(937,141.35,'四室两厅','occupied','2026-01-01 09:00:00.000000',187,2,'',1,'0201'),(938,137.09,'两室一厅','renting','2026-01-01 09:00:00.000000',187,2,'',3,'0301'),(939,76.92,'一室一厅','vacant','2026-01-01 09:00:00.000000',187,0,'',0,'0401'),(940,138.53,'两室一厅','occupied','2026-01-01 09:00:00.000000',187,1,'',2,'0501'),(941,91.25,'一室一厅','occupied','2026-01-01 09:00:00.000000',188,2,'',4,'0101'),(942,114.97,'一室一厅','occupied','2026-01-01 09:00:00.000000',188,2,'',1,'0201'),(943,122.05,'四室两厅','occupied','2026-01-01 09:00:00.000000',188,2,'',5,'0301'),(944,70.20,'一室一厅','occupied','2026-01-01 09:00:00.000000',188,2,'',1,'0401'),(945,133.00,'四室两厅','occupied','2026-01-01 09:00:00.000000',188,1,'',2,'0501'),(946,162.75,'三室两厅','occupied','2026-01-01 09:00:00.000000',189,2,'',2,'0101'),(947,73.98,'一室一厅','vacant','2026-01-01 09:00:00.000000',189,0,'',0,'0201'),(948,107.16,'四室两厅','occupied','2026-01-01 09:00:00.000000',189,2,'',2,'0301'),(949,130.10,'两室一厅','vacant','2026-01-01 09:00:00.000000',189,0,'',0,'0401'),(950,164.73,'三室两厅','occupied','2026-01-01 09:00:00.000000',189,2,'',1,'0501'),(951,83.58,'三室两厅','occupied','2026-01-01 09:00:00.000000',190,2,'',1,'0101'),(952,89.07,'两室一厅','occupied','2026-01-01 09:00:00.000000',190,2,'',1,'0201'),(953,115.39,'两室一厅','repairing','2026-01-01 09:00:00.000000',190,1,'',2,'0301'),(954,142.51,'一室一厅','occupied','2026-01-01 09:00:00.000000',190,1,'',4,'0401'),(955,150.03,'三室两厅','repairing','2026-01-01 09:00:00.000000',190,2,'',4,'0501'),(956,131.83,'一室一厅','occupied','2026-01-01 09:00:00.000000',191,2,'',4,'0101'),(957,162.12,'一室一厅','occupied','2026-01-01 09:00:00.000000',191,1,'',4,'0201'),(958,121.60,'一室一厅','vacant','2026-01-01 09:00:00.000000',191,0,'',0,'0301'),(959,157.60,'三室两厅','occupied','2026-01-01 09:00:00.000000',191,1,'',2,'0401'),(960,142.18,'一室一厅','occupied','2026-01-01 09:00:00.000000',191,2,'',3,'0501'),(961,144.09,'三室两厅','occupied','2026-01-01 09:00:00.000000',192,1,'',5,'0101'),(962,82.25,'四室两厅','occupied','2026-01-01 09:00:00.000000',192,2,'',4,'0201'),(963,106.21,'一室一厅','occupied','2026-01-01 09:00:00.000000',192,1,'',3,'0301'),(964,141.02,'一室一厅','occupied','2026-01-01 09:00:00.000000',192,1,'',4,'0401'),(965,141.10,'四室两厅','occupied','2026-01-01 09:00:00.000000',192,2,'',5,'0501'),(966,121.09,'三室两厅','vacant','2026-01-01 09:00:00.000000',193,0,'',0,'0101'),(967,120.87,'两室一厅','occupied','2026-01-01 09:00:00.000000',193,1,'',3,'0201'),(968,159.06,'三室两厅','occupied','2026-01-01 09:00:00.000000',193,2,'',1,'0301'),(969,154.91,'三室两厅','repairing','2026-01-01 09:00:00.000000',193,1,'',4,'0401'),(970,93.77,'三室两厅','renting','2026-01-01 09:00:00.000000',193,2,'',1,'0501'),(971,138.01,'两室一厅','occupied','2026-01-01 09:00:00.000000',194,2,'',3,'0101'),(972,73.44,'两室一厅','occupied','2026-01-01 09:00:00.000000',194,1,'',2,'0201'),(973,85.64,'四室两厅','occupied','2026-01-01 09:00:00.000000',194,2,'',5,'0301'),(974,161.49,'四室两厅','occupied','2026-01-01 09:00:00.000000',194,2,'',2,'0401'),(975,128.04,'两室一厅','vacant','2026-01-01 09:00:00.000000',194,0,'',0,'0501'),(976,89.34,'一室一厅','occupied','2026-01-01 09:00:00.000000',195,1,'',4,'0101'),(977,151.16,'四室两厅','renting','2026-01-01 09:00:00.000000',195,2,'',3,'0201'),(978,131.51,'一室一厅','occupied','2026-01-01 09:00:00.000000',195,2,'',5,'0301'),(979,166.74,'一室一厅','occupied','2026-01-01 09:00:00.000000',195,2,'',5,'0401'),(980,99.77,'三室两厅','occupied','2026-01-01 09:00:00.000000',195,1,'',4,'0501'),(981,111.71,'四室两厅','occupied','2026-01-01 09:00:00.000000',196,1,'',3,'0101'),(982,95.94,'一室一厅','occupied','2026-01-01 09:00:00.000000',196,1,'',1,'0201'),(983,86.73,'一室一厅','occupied','2026-01-01 09:00:00.000000',196,1,'',1,'0301'),(984,96.37,'两室一厅','occupied','2026-01-01 09:00:00.000000',196,2,'',2,'0401'),(985,135.97,'三室两厅','occupied','2026-01-01 09:00:00.000000',196,1,'',4,'0501'),(986,98.37,'三室两厅','renting','2026-01-01 09:00:00.000000',197,2,'',1,'0101'),(987,88.64,'三室两厅','occupied','2026-01-01 09:00:00.000000',197,1,'',4,'0201'),(988,115.69,'四室两厅','occupied','2026-01-01 09:00:00.000000',197,2,'',5,'0301'),(989,137.21,'两室一厅','occupied','2026-01-01 09:00:00.000000',197,2,'',4,'0401'),(990,127.91,'三室两厅','occupied','2026-01-01 09:00:00.000000',197,1,'',5,'0501'),(991,89.78,'三室两厅','occupied','2026-01-01 09:00:00.000000',198,2,'',1,'0101'),(992,72.51,'两室一厅','occupied','2026-01-01 09:00:00.000000',198,1,'',4,'0201'),(993,79.90,'三室两厅','occupied','2026-01-01 09:00:00.000000',198,2,'',3,'0301'),(994,73.39,'一室一厅','renting','2026-01-01 09:00:00.000000',198,1,'',1,'0401'),(995,149.38,'一室一厅','occupied','2026-01-01 09:00:00.000000',198,1,'',2,'0501'),(996,138.84,'两室一厅','vacant','2026-01-01 09:00:00.000000',199,0,'',0,'0101'),(997,101.90,'三室两厅','renting','2026-01-01 09:00:00.000000',199,1,'',3,'0201'),(998,74.53,'两室一厅','occupied','2026-01-01 09:00:00.000000',199,2,'',4,'0301'),(999,128.13,'两室一厅','occupied','2026-01-01 09:00:00.000000',199,2,'',1,'0401'),(1000,153.35,'四室两厅','vacant','2026-01-01 09:00:00.000000',199,0,'',0,'0501'),(1001,132.62,'三室两厅','occupied','2026-01-01 09:00:00.000000',200,2,'',2,'0101'),(1002,103.40,'三室两厅','occupied','2026-01-01 09:00:00.000000',200,2,'',4,'0201'),(1003,133.40,'三室两厅','repairing','2026-01-01 09:00:00.000000',200,2,'',3,'0301'),(1004,148.02,'两室一厅','occupied','2026-01-01 09:00:00.000000',200,1,'',3,'0401'),(1005,97.39,'三室两厅','occupied','2026-01-01 09:00:00.000000',200,1,'',1,'0501');
/*!40000 ALTER TABLE `house` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_log`
--

DROP TABLE IF EXISTS `login_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_log` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `ip` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_log`
--

LOCK TABLES `login_log` WRITE;
/*!40000 ALTER TABLE `login_log` DISABLE KEYS */;
INSERT INTO `login_log` VALUES (1,'admin','127.0.0.1','2026-06-04 08:28:45.861423'),(2,'admin','127.0.0.1','2026-06-04 10:31:12.234842'),(3,'admin','127.0.0.1','2026-06-05 02:48:14.516181'),(4,'admin','127.0.0.1','2026-06-05 05:04:12.458386'),(5,'admin','127.0.0.1','2026-06-05 07:05:33.668766'),(6,'admin','127.0.0.1','2026-06-05 09:28:40.066528'),(7,'admin','127.0.0.1','2026-06-08 02:57:26.448645'),(8,'admin','127.0.0.1','2026-06-08 03:50:17.813596'),(9,'admin','127.0.0.1','2026-06-08 05:45:05.512940'),(10,'admin','127.0.0.1','2026-06-08 07:47:45.382984'),(11,'admin','127.0.0.1','2026-06-08 09:48:48.004585'),(12,'admin','127.0.0.1','2026-06-09 01:50:17.562710'),(13,'admin','127.0.0.1','2026-06-09 03:54:14.189056'),(14,'admin','127.0.0.1','2026-06-09 05:57:47.030453'),(15,'admin','127.0.0.1','2026-06-09 08:29:45.166568'),(16,'admin','127.0.0.1','2026-06-10 02:59:03.285337');
/*!40000 ALTER TABLE `login_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `icon` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `path` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `component` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `sort` int DEFAULT NULL,
  `hidden` tinyint(1) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `parent_id` bigint DEFAULT NULL,
  `menu_type` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `menu_parent_id_7f4b2723_fk_menu_id` (`parent_id`),
  CONSTRAINT `menu_parent_id_7f4b2723_fk_menu_id` FOREIGN KEY (`parent_id`) REFERENCES `menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu`
--

LOCK TABLES `menu` WRITE;
/*!40000 ALTER TABLE `menu` DISABLE KEYS */;
INSERT INTO `menu` VALUES (1,'用户列表',NULL,'/user/list',NULL,0,0,'2026-05-29 04:29:43.844966',NULL,1),(2,'角色列表',NULL,'/role/list',NULL,0,0,'2026-05-29 04:29:56.721758',NULL,1),(3,'权限列表',NULL,'/permission/list',NULL,0,0,'2026-05-29 04:30:51.148822',NULL,1),(4,'报修列表',NULL,'/repair/list',NULL,0,0,'2026-05-29 04:31:05.957606',NULL,1);
/*!40000 ALTER TABLE `menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notice`
--

DROP TABLE IF EXISTS `notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `content` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notice`
--

LOCK TABLES `notice` WRITE;
/*!40000 ALTER TABLE `notice` DISABLE KEYS */;
INSERT INTO `notice` VALUES (1,'停水通知','明日上午9点停水，请合理安排用水时间','published','2026-06-03 06:42:22.414744');
/*!40000 ALTER TABLE `notice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operation_log`
--

DROP TABLE IF EXISTS `operation_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operation_log` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `module` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `action` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operation_log`
--

LOCK TABLES `operation_log` WRITE;
/*!40000 ALTER TABLE `operation_log` DISABLE KEYS */;
INSERT INTO `operation_log` VALUES (1,'admin2','房屋管理','新增房屋 104','2026-06-03 09:57:16.641698'),(2,'admin2','收费管理','缴费账单 3','2026-06-04 06:12:07.730468'),(3,'admin','业主管理','新增业主：张三','2026-06-04 10:50:12.475787'),(4,'admin2','业主管理','新增业主 张三','2026-06-04 10:50:12.477232'),(5,'admin2','文件上传','上传文件 张三','2026-06-04 10:50:12.478882'),(6,'admin','业主管理','修改业主：张三','2026-06-04 11:36:27.323043'),(7,'admin2','业主管理','修改业主 张三','2026-06-04 11:36:27.326282'),(8,'admin2','车位管理','新增车位 A01-13','2026-06-05 06:25:55.793827'),(9,'','车辆管理','新增车辆：京A12345','2026-06-05 06:28:15.558316'),(10,'','车辆管理','修改车辆：京A12345','2026-06-05 06:37:35.020057'),(11,'','车辆管理','删除车辆：京A12345','2026-06-05 06:40:09.500338'),(12,'','车辆管理','新增车辆：京A12345','2026-06-05 07:06:34.371031'),(13,'admin','车辆管理','修改车辆：京A12345','2026-06-05 07:44:47.610815'),(14,'admin','车辆管理','修改车辆：京A12345','2026-06-05 07:45:33.663338'),(15,'admin','车辆管理','修改车辆：京A12345','2026-06-05 07:48:20.273042'),(16,'admin','车辆管理','修改车辆：京A12345','2026-06-05 07:50:11.444568'),(17,'','访客管理','新增访客','2026-06-05 08:59:12.333802'),(18,'admin','访客管理','新增访客','2026-06-08 06:40:59.173949'),(19,'admin','访客管理','处理访客信息','2026-06-08 08:01:55.284274'),(20,'admin','访客管理','审批访客：李朋友','2026-06-08 08:35:06.283495'),(21,'admin','访客管理','审批访客：张三朋友','2026-06-08 10:06:09.411371'),(22,'admin','报修管理','修改报修','2026-06-09 09:14:19.300732');
/*!40000 ALTER TABLE `operation_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `owner`
--

DROP TABLE IF EXISTS `owner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `owner` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `id_card` varchar(18) COLLATE utf8mb4_general_ci NOT NULL,
  `gender` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `house_id` bigint NOT NULL,
  `remark` longtext COLLATE utf8mb4_general_ci,
  `birthday` date DEFAULT NULL,
  `is_primary` tinyint(1) NOT NULL,
  `relationship` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `id_card_image` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `avatar` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_card` (`id_card`),
  UNIQUE KEY `owner_phone_15cbbf92_uniq` (`phone`),
  KEY `owner_house_id_add4d76a_fk_house_id` (`house_id`),
  CONSTRAINT `owner_house_id_add4d76a_fk_house_id` FOREIGN KEY (`house_id`) REFERENCES `house` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `owner`
--

LOCK TABLES `owner` WRITE;
/*!40000 ALTER TABLE `owner` DISABLE KEYS */;
INSERT INTO `owner` VALUES (2,'李四','10000000011','DEMO-ID-OWNER-02','female','2026-06-01 10:24:21.434288',1,NULL,NULL,0,'spouse',NULL,NULL),(3,'王五','10000000012','DEMO-ID-OWNER-03','male','2026-06-02 05:35:55.670306',1,NULL,NULL,0,'self',NULL,NULL),(4,'张三','10000000010','DEMO-ID-OWNER-04','female','2026-06-04 10:50:12.462238',1,NULL,NULL,1,'parent','/media/upload/截屏2026-05-20 11.45.17.png','');
/*!40000 ALTER TABLE `owner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parking`
--

DROP TABLE IF EXISTS `parking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parking` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `parking_no` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `area` decimal(10,2) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `owner_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `parking_parking_no_ec5b9127_uniq` (`parking_no`),
  KEY `parking_owner_id_613675b7_fk_owner_id` (`owner_id`),
  CONSTRAINT `parking_owner_id_613675b7_fk_owner_id` FOREIGN KEY (`owner_id`) REFERENCES `owner` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parking`
--

LOCK TABLES `parking` WRITE;
/*!40000 ALTER TABLE `parking` DISABLE KEYS */;
INSERT INTO `parking` VALUES (4,'A001',20.00,'used','2026-06-02 11:54:02.062387',3),(5,'A01-13',20.00,'idle','2026-06-05 06:25:55.783154',2);
/*!40000 ALTER TABLE `parking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repair`
--

DROP TABLE IF EXISTS `repair`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `content` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `house_id` bigint NOT NULL,
  `owner_id` bigint NOT NULL,
  `finish_time` datetime(6) DEFAULT NULL,
  `phone` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `repair_house_id_3159e8d6_fk_house_id` (`house_id`),
  KEY `repair_owner_id_c35b2a7b_fk_owner_id` (`owner_id`),
  CONSTRAINT `repair_house_id_3159e8d6_fk_house_id` FOREIGN KEY (`house_id`) REFERENCES `house` (`id`),
  CONSTRAINT `repair_owner_id_c35b2a7b_fk_owner_id` FOREIGN KEY (`owner_id`) REFERENCES `owner` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repair`
--

LOCK TABLES `repair` WRITE;
/*!40000 ALTER TABLE `repair` DISABLE KEYS */;
INSERT INTO `repair` VALUES (1,'空调漏水','客厅空调一直漏水','finished','2026-06-03 05:06:33.424371',1,2,'2026-06-09 09:32:11.500437','');
/*!40000 ALTER TABLE `repair` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repair_repair_user`
--

DROP TABLE IF EXISTS `repair_repair_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair_repair_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `repair_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `repair_repair_user_repair_id_user_id_e714ac49_uniq` (`repair_id`,`user_id`),
  KEY `repair_repair_user_user_id_0adc42ac_fk_sys_user_id` (`user_id`),
  CONSTRAINT `repair_repair_user_repair_id_db88d6a4_fk_repair_id` FOREIGN KEY (`repair_id`) REFERENCES `repair` (`id`),
  CONSTRAINT `repair_repair_user_user_id_0adc42ac_fk_sys_user_id` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repair_repair_user`
--

LOCK TABLES `repair_repair_user` WRITE;
/*!40000 ALTER TABLE `repair_repair_user` DISABLE KEYS */;
INSERT INTO `repair_repair_user` VALUES (1,1,1);
/*!40000 ALTER TABLE `repair_repair_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_permission`
--

DROP TABLE IF EXISTS `sys_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_permission` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `code` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `menu_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sys_permission_menu_id_50793a4b_fk_menu_id` (`menu_id`),
  CONSTRAINT `sys_permission_menu_id_50793a4b_fk_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_permission`
--

LOCK TABLES `sys_permission` WRITE;
/*!40000 ALTER TABLE `sys_permission` DISABLE KEYS */;
INSERT INTO `sys_permission` VALUES (1,'用户列表','user:list','2026-05-28 07:55:34.222091',1),(2,'用户新增','user:create','2026-05-28 10:44:58.373328',NULL),(3,'角色列表','role:create','2026-05-28 10:45:48.510139',2),(4,'权限列表','permission:create','2026-05-28 10:46:10.886751',3),(5,'报修列表','repair:list','2026-05-28 11:12:08.281503',NULL);
/*!40000 ALTER TABLE `sys_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user`
--

DROP TABLE IF EXISTS `sys_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `phone` varchar(11) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `real_name` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nickname` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `id_card` varchar(18) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `avatar` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `status` smallint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `role_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `id_card` (`id_card`),
  KEY `sys_user_role_id_8a2e10d7_fk_users_role_id` (`role_id`),
  CONSTRAINT `sys_user_role_id_8a2e10d7_fk_users_role_id` FOREIGN KEY (`role_id`) REFERENCES `users_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

LOCK TABLES `sys_user` WRITE;
/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES (1,'pbkdf2_sha256$600000$hIGhsNnBQ6EsjeSj55c6JD$2+bjR3Ock7FobuznQl2sFW8Y1auTYaMXfez3NPDaQE4=','2026-05-28 10:59:25.000000',1,'admin','','','',1,1,'2026-05-28 10:50:43.000000',NULL,'管理员',NULL,NULL,NULL,1,'2026-05-28 10:50:43.531654',NULL);
/*!40000 ALTER TABLE `sys_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user_groups`
--

DROP TABLE IF EXISTS `sys_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sys_user_groups_user_id_group_id_9eeca8dc_uniq` (`user_id`,`group_id`),
  KEY `sys_user_groups_group_id_9b8b43fc_fk_auth_group_id` (`group_id`),
  CONSTRAINT `sys_user_groups_group_id_9b8b43fc_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `sys_user_groups_user_id_87e5b1ea_fk_sys_user_id` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user_groups`
--

LOCK TABLES `sys_user_groups` WRITE;
/*!40000 ALTER TABLE `sys_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user_roles`
--

DROP TABLE IF EXISTS `sys_user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user_roles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `role_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sys_user_roles_user_id_role_id_f0e1dc00_uniq` (`user_id`,`role_id`),
  KEY `sys_user_roles_role_id_17e6bf1b_fk_users_role_id` (`role_id`),
  CONSTRAINT `sys_user_roles_role_id_17e6bf1b_fk_users_role_id` FOREIGN KEY (`role_id`) REFERENCES `users_role` (`id`),
  CONSTRAINT `sys_user_roles_user_id_97eefe2f_fk_sys_user_id` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user_roles`
--

LOCK TABLES `sys_user_roles` WRITE;
/*!40000 ALTER TABLE `sys_user_roles` DISABLE KEYS */;
INSERT INTO `sys_user_roles` VALUES (1,1,1);
/*!40000 ALTER TABLE `sys_user_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user_user_permissions`
--

DROP TABLE IF EXISTS `sys_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sys_user_user_permissions_user_id_permission_id_20b74a10_uniq` (`user_id`,`permission_id`),
  KEY `sys_user_user_permis_permission_id_55623e22_fk_auth_perm` (`permission_id`),
  CONSTRAINT `sys_user_user_permis_permission_id_55623e22_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `sys_user_user_permissions_user_id_ad6c918a_fk_sys_user_id` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user_user_permissions`
--

LOCK TABLES `sys_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `sys_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unit`
--

DROP TABLE IF EXISTS `unit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unit` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `code` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `floor_count` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `building_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unit_code_a6d32bd6_uniq` (`code`),
  KEY `unit_building_id_7d8d3ee3_fk_building_id` (`building_id`),
  CONSTRAINT `unit_building_id_7d8d3ee3_fk_building_id` FOREIGN KEY (`building_id`) REFERENCES `building` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=203 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unit`
--

LOCK TABLES `unit` WRITE;
/*!40000 ALTER TABLE `unit` DISABLE KEYS */;
INSERT INTO `unit` VALUES (1,'1单元','UNIT001',18,'2026-05-29 07:12:17.870584',1),(2,'1单元','U001',18,'2026-06-01 09:21:14.792148',1),(3,'1单元','UNT00001',30,'2026-01-01 09:00:00.000000',1),(4,'2单元','UNT00002',30,'2026-01-01 09:00:00.000000',1),(5,'3单元','UNT00003',30,'2026-01-01 09:00:00.000000',1),(6,'4单元','UNT00004',30,'2026-01-01 09:00:00.000000',1),(7,'1单元','UNT00005',30,'2026-01-01 09:00:00.000000',2),(8,'2单元','UNT00006',30,'2026-01-01 09:00:00.000000',2),(9,'3单元','UNT00007',30,'2026-01-01 09:00:00.000000',2),(10,'4单元','UNT00008',30,'2026-01-01 09:00:00.000000',2),(11,'1单元','UNT00009',30,'2026-01-01 09:00:00.000000',3),(12,'2单元','UNT00010',30,'2026-01-01 09:00:00.000000',3),(13,'3单元','UNT00011',30,'2026-01-01 09:00:00.000000',3),(14,'4单元','UNT00012',30,'2026-01-01 09:00:00.000000',3),(15,'1单元','UNT00013',30,'2026-01-01 09:00:00.000000',4),(16,'2单元','UNT00014',30,'2026-01-01 09:00:00.000000',4),(17,'3单元','UNT00015',30,'2026-01-01 09:00:00.000000',4),(18,'4单元','UNT00016',30,'2026-01-01 09:00:00.000000',4),(19,'1单元','UNT00017',30,'2026-01-01 09:00:00.000000',5),(20,'2单元','UNT00018',30,'2026-01-01 09:00:00.000000',5),(21,'3单元','UNT00019',30,'2026-01-01 09:00:00.000000',5),(22,'4单元','UNT00020',30,'2026-01-01 09:00:00.000000',5),(23,'1单元','UNT00021',30,'2026-01-01 09:00:00.000000',6),(24,'2单元','UNT00022',30,'2026-01-01 09:00:00.000000',6),(25,'3单元','UNT00023',30,'2026-01-01 09:00:00.000000',6),(26,'4单元','UNT00024',30,'2026-01-01 09:00:00.000000',6),(27,'1单元','UNT00025',30,'2026-01-01 09:00:00.000000',7),(28,'2单元','UNT00026',30,'2026-01-01 09:00:00.000000',7),(29,'3单元','UNT00027',30,'2026-01-01 09:00:00.000000',7),(30,'4单元','UNT00028',30,'2026-01-01 09:00:00.000000',7),(31,'1单元','UNT00029',30,'2026-01-01 09:00:00.000000',8),(32,'2单元','UNT00030',30,'2026-01-01 09:00:00.000000',8),(33,'3单元','UNT00031',30,'2026-01-01 09:00:00.000000',8),(34,'4单元','UNT00032',30,'2026-01-01 09:00:00.000000',8),(35,'1单元','UNT00033',30,'2026-01-01 09:00:00.000000',9),(36,'2单元','UNT00034',30,'2026-01-01 09:00:00.000000',9),(37,'3单元','UNT00035',30,'2026-01-01 09:00:00.000000',9),(38,'4单元','UNT00036',30,'2026-01-01 09:00:00.000000',9),(39,'1单元','UNT00037',30,'2026-01-01 09:00:00.000000',10),(40,'2单元','UNT00038',30,'2026-01-01 09:00:00.000000',10),(41,'3单元','UNT00039',30,'2026-01-01 09:00:00.000000',10),(42,'4单元','UNT00040',30,'2026-01-01 09:00:00.000000',10),(43,'1单元','UNT00041',30,'2026-01-01 09:00:00.000000',11),(44,'2单元','UNT00042',30,'2026-01-01 09:00:00.000000',11),(45,'3单元','UNT00043',30,'2026-01-01 09:00:00.000000',11),(46,'4单元','UNT00044',30,'2026-01-01 09:00:00.000000',11),(47,'1单元','UNT00045',30,'2026-01-01 09:00:00.000000',12),(48,'2单元','UNT00046',30,'2026-01-01 09:00:00.000000',12),(49,'3单元','UNT00047',30,'2026-01-01 09:00:00.000000',12),(50,'4单元','UNT00048',30,'2026-01-01 09:00:00.000000',12),(51,'1单元','UNT00049',30,'2026-01-01 09:00:00.000000',13),(52,'2单元','UNT00050',30,'2026-01-01 09:00:00.000000',13),(53,'3单元','UNT00051',30,'2026-01-01 09:00:00.000000',13),(54,'4单元','UNT00052',30,'2026-01-01 09:00:00.000000',13),(55,'1单元','UNT00053',30,'2026-01-01 09:00:00.000000',14),(56,'2单元','UNT00054',30,'2026-01-01 09:00:00.000000',14),(57,'3单元','UNT00055',30,'2026-01-01 09:00:00.000000',14),(58,'4单元','UNT00056',30,'2026-01-01 09:00:00.000000',14),(59,'1单元','UNT00057',30,'2026-01-01 09:00:00.000000',15),(60,'2单元','UNT00058',30,'2026-01-01 09:00:00.000000',15),(61,'3单元','UNT00059',30,'2026-01-01 09:00:00.000000',15),(62,'4单元','UNT00060',30,'2026-01-01 09:00:00.000000',15),(63,'1单元','UNT00061',30,'2026-01-01 09:00:00.000000',16),(64,'2单元','UNT00062',30,'2026-01-01 09:00:00.000000',16),(65,'3单元','UNT00063',30,'2026-01-01 09:00:00.000000',16),(66,'4单元','UNT00064',30,'2026-01-01 09:00:00.000000',16),(67,'1单元','UNT00065',30,'2026-01-01 09:00:00.000000',17),(68,'2单元','UNT00066',30,'2026-01-01 09:00:00.000000',17),(69,'3单元','UNT00067',30,'2026-01-01 09:00:00.000000',17),(70,'4单元','UNT00068',30,'2026-01-01 09:00:00.000000',17),(71,'1单元','UNT00069',30,'2026-01-01 09:00:00.000000',18),(72,'2单元','UNT00070',30,'2026-01-01 09:00:00.000000',18),(73,'3单元','UNT00071',30,'2026-01-01 09:00:00.000000',18),(74,'4单元','UNT00072',30,'2026-01-01 09:00:00.000000',18),(75,'1单元','UNT00073',30,'2026-01-01 09:00:00.000000',19),(76,'2单元','UNT00074',30,'2026-01-01 09:00:00.000000',19),(77,'3单元','UNT00075',30,'2026-01-01 09:00:00.000000',19),(78,'4单元','UNT00076',30,'2026-01-01 09:00:00.000000',19),(79,'1单元','UNT00077',30,'2026-01-01 09:00:00.000000',20),(80,'2单元','UNT00078',30,'2026-01-01 09:00:00.000000',20),(81,'3单元','UNT00079',30,'2026-01-01 09:00:00.000000',20),(82,'4单元','UNT00080',30,'2026-01-01 09:00:00.000000',20),(83,'1单元','UNT00081',30,'2026-01-01 09:00:00.000000',21),(84,'2单元','UNT00082',30,'2026-01-01 09:00:00.000000',21),(85,'3单元','UNT00083',30,'2026-01-01 09:00:00.000000',21),(86,'4单元','UNT00084',30,'2026-01-01 09:00:00.000000',21),(87,'1单元','UNT00085',30,'2026-01-01 09:00:00.000000',22),(88,'2单元','UNT00086',30,'2026-01-01 09:00:00.000000',22),(89,'3单元','UNT00087',30,'2026-01-01 09:00:00.000000',22),(90,'4单元','UNT00088',30,'2026-01-01 09:00:00.000000',22),(91,'1单元','UNT00089',30,'2026-01-01 09:00:00.000000',23),(92,'2单元','UNT00090',30,'2026-01-01 09:00:00.000000',23),(93,'3单元','UNT00091',30,'2026-01-01 09:00:00.000000',23),(94,'4单元','UNT00092',30,'2026-01-01 09:00:00.000000',23),(95,'1单元','UNT00093',30,'2026-01-01 09:00:00.000000',24),(96,'2单元','UNT00094',30,'2026-01-01 09:00:00.000000',24),(97,'3单元','UNT00095',30,'2026-01-01 09:00:00.000000',24),(98,'4单元','UNT00096',30,'2026-01-01 09:00:00.000000',24),(99,'1单元','UNT00097',30,'2026-01-01 09:00:00.000000',25),(100,'2单元','UNT00098',30,'2026-01-01 09:00:00.000000',25),(101,'3单元','UNT00099',30,'2026-01-01 09:00:00.000000',25),(102,'4单元','UNT00100',30,'2026-01-01 09:00:00.000000',25),(103,'1单元','UNT00101',30,'2026-01-01 09:00:00.000000',26),(104,'2单元','UNT00102',30,'2026-01-01 09:00:00.000000',26),(105,'3单元','UNT00103',30,'2026-01-01 09:00:00.000000',26),(106,'4单元','UNT00104',30,'2026-01-01 09:00:00.000000',26),(107,'1单元','UNT00105',30,'2026-01-01 09:00:00.000000',27),(108,'2单元','UNT00106',30,'2026-01-01 09:00:00.000000',27),(109,'3单元','UNT00107',30,'2026-01-01 09:00:00.000000',27),(110,'4单元','UNT00108',30,'2026-01-01 09:00:00.000000',27),(111,'1单元','UNT00109',30,'2026-01-01 09:00:00.000000',28),(112,'2单元','UNT00110',30,'2026-01-01 09:00:00.000000',28),(113,'3单元','UNT00111',30,'2026-01-01 09:00:00.000000',28),(114,'4单元','UNT00112',30,'2026-01-01 09:00:00.000000',28),(115,'1单元','UNT00113',30,'2026-01-01 09:00:00.000000',29),(116,'2单元','UNT00114',30,'2026-01-01 09:00:00.000000',29),(117,'3单元','UNT00115',30,'2026-01-01 09:00:00.000000',29),(118,'4单元','UNT00116',30,'2026-01-01 09:00:00.000000',29),(119,'1单元','UNT00117',30,'2026-01-01 09:00:00.000000',30),(120,'2单元','UNT00118',30,'2026-01-01 09:00:00.000000',30),(121,'3单元','UNT00119',30,'2026-01-01 09:00:00.000000',30),(122,'4单元','UNT00120',30,'2026-01-01 09:00:00.000000',30),(123,'1单元','UNT00121',30,'2026-01-01 09:00:00.000000',31),(124,'2单元','UNT00122',30,'2026-01-01 09:00:00.000000',31),(125,'3单元','UNT00123',30,'2026-01-01 09:00:00.000000',31),(126,'4单元','UNT00124',30,'2026-01-01 09:00:00.000000',31),(127,'1单元','UNT00125',30,'2026-01-01 09:00:00.000000',32),(128,'2单元','UNT00126',30,'2026-01-01 09:00:00.000000',32),(129,'3单元','UNT00127',30,'2026-01-01 09:00:00.000000',32),(130,'4单元','UNT00128',30,'2026-01-01 09:00:00.000000',32),(131,'1单元','UNT00129',30,'2026-01-01 09:00:00.000000',33),(132,'2单元','UNT00130',30,'2026-01-01 09:00:00.000000',33),(133,'3单元','UNT00131',30,'2026-01-01 09:00:00.000000',33),(134,'4单元','UNT00132',30,'2026-01-01 09:00:00.000000',33),(135,'1单元','UNT00133',30,'2026-01-01 09:00:00.000000',34),(136,'2单元','UNT00134',30,'2026-01-01 09:00:00.000000',34),(137,'3单元','UNT00135',30,'2026-01-01 09:00:00.000000',34),(138,'4单元','UNT00136',30,'2026-01-01 09:00:00.000000',34),(139,'1单元','UNT00137',30,'2026-01-01 09:00:00.000000',35),(140,'2单元','UNT00138',30,'2026-01-01 09:00:00.000000',35),(141,'3单元','UNT00139',30,'2026-01-01 09:00:00.000000',35),(142,'4单元','UNT00140',30,'2026-01-01 09:00:00.000000',35),(143,'1单元','UNT00141',30,'2026-01-01 09:00:00.000000',36),(144,'2单元','UNT00142',30,'2026-01-01 09:00:00.000000',36),(145,'3单元','UNT00143',30,'2026-01-01 09:00:00.000000',36),(146,'4单元','UNT00144',30,'2026-01-01 09:00:00.000000',36),(147,'1单元','UNT00145',30,'2026-01-01 09:00:00.000000',37),(148,'2单元','UNT00146',30,'2026-01-01 09:00:00.000000',37),(149,'3单元','UNT00147',30,'2026-01-01 09:00:00.000000',37),(150,'4单元','UNT00148',30,'2026-01-01 09:00:00.000000',37),(151,'1单元','UNT00149',30,'2026-01-01 09:00:00.000000',38),(152,'2单元','UNT00150',30,'2026-01-01 09:00:00.000000',38),(153,'3单元','UNT00151',30,'2026-01-01 09:00:00.000000',38),(154,'4单元','UNT00152',30,'2026-01-01 09:00:00.000000',38),(155,'1单元','UNT00153',30,'2026-01-01 09:00:00.000000',39),(156,'2单元','UNT00154',30,'2026-01-01 09:00:00.000000',39),(157,'3单元','UNT00155',30,'2026-01-01 09:00:00.000000',39),(158,'4单元','UNT00156',30,'2026-01-01 09:00:00.000000',39),(159,'1单元','UNT00157',30,'2026-01-01 09:00:00.000000',40),(160,'2单元','UNT00158',30,'2026-01-01 09:00:00.000000',40),(161,'3单元','UNT00159',30,'2026-01-01 09:00:00.000000',40),(162,'4单元','UNT00160',30,'2026-01-01 09:00:00.000000',40),(163,'1单元','UNT00161',30,'2026-01-01 09:00:00.000000',41),(164,'2单元','UNT00162',30,'2026-01-01 09:00:00.000000',41),(165,'3单元','UNT00163',30,'2026-01-01 09:00:00.000000',41),(166,'4单元','UNT00164',30,'2026-01-01 09:00:00.000000',41),(167,'1单元','UNT00165',30,'2026-01-01 09:00:00.000000',42),(168,'2单元','UNT00166',30,'2026-01-01 09:00:00.000000',42),(169,'3单元','UNT00167',30,'2026-01-01 09:00:00.000000',42),(170,'4单元','UNT00168',30,'2026-01-01 09:00:00.000000',42),(171,'1单元','UNT00169',30,'2026-01-01 09:00:00.000000',43),(172,'2单元','UNT00170',30,'2026-01-01 09:00:00.000000',43),(173,'3单元','UNT00171',30,'2026-01-01 09:00:00.000000',43),(174,'4单元','UNT00172',30,'2026-01-01 09:00:00.000000',43),(175,'1单元','UNT00173',30,'2026-01-01 09:00:00.000000',44),(176,'2单元','UNT00174',30,'2026-01-01 09:00:00.000000',44),(177,'3单元','UNT00175',30,'2026-01-01 09:00:00.000000',44),(178,'4单元','UNT00176',30,'2026-01-01 09:00:00.000000',44),(179,'1单元','UNT00177',30,'2026-01-01 09:00:00.000000',45),(180,'2单元','UNT00178',30,'2026-01-01 09:00:00.000000',45),(181,'3单元','UNT00179',30,'2026-01-01 09:00:00.000000',45),(182,'4单元','UNT00180',30,'2026-01-01 09:00:00.000000',45),(183,'1单元','UNT00181',30,'2026-01-01 09:00:00.000000',46),(184,'2单元','UNT00182',30,'2026-01-01 09:00:00.000000',46),(185,'3单元','UNT00183',30,'2026-01-01 09:00:00.000000',46),(186,'4单元','UNT00184',30,'2026-01-01 09:00:00.000000',46),(187,'1单元','UNT00185',30,'2026-01-01 09:00:00.000000',47),(188,'2单元','UNT00186',30,'2026-01-01 09:00:00.000000',47),(189,'3单元','UNT00187',30,'2026-01-01 09:00:00.000000',47),(190,'4单元','UNT00188',30,'2026-01-01 09:00:00.000000',47),(191,'1单元','UNT00189',30,'2026-01-01 09:00:00.000000',48),(192,'2单元','UNT00190',30,'2026-01-01 09:00:00.000000',48),(193,'3单元','UNT00191',30,'2026-01-01 09:00:00.000000',48),(194,'4单元','UNT00192',30,'2026-01-01 09:00:00.000000',48),(195,'1单元','UNT00193',30,'2026-01-01 09:00:00.000000',49),(196,'2单元','UNT00194',30,'2026-01-01 09:00:00.000000',49),(197,'3单元','UNT00195',30,'2026-01-01 09:00:00.000000',49),(198,'4单元','UNT00196',30,'2026-01-01 09:00:00.000000',49),(199,'1单元','UNT00197',30,'2026-01-01 09:00:00.000000',50),(200,'2单元','UNT00198',30,'2026-01-01 09:00:00.000000',50),(201,'3单元','UNT00199',30,'2026-01-01 09:00:00.000000',50),(202,'4单元','UNT00200',30,'2026-01-01 09:00:00.000000',50);
/*!40000 ALTER TABLE `unit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_role`
--

DROP TABLE IF EXISTS `users_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `code` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_role`
--

LOCK TABLES `users_role` WRITE;
/*!40000 ALTER TABLE `users_role` DISABLE KEYS */;
INSERT INTO `users_role` VALUES (1,'管理员','admin','2026-05-28 11:08:42.423708'),(2,'维修员','repair','2026-05-28 11:12:32.057952');
/*!40000 ALTER TABLE `users_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_role_permissions`
--

DROP TABLE IF EXISTS `users_role_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_role_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role_id` bigint NOT NULL,
  `permission_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_role_permissions_role_id_permission_id_a9833844_uniq` (`role_id`,`permission_id`),
  KEY `users_role_permissio_permission_id_5313a8eb_fk_sys_permi` (`permission_id`),
  CONSTRAINT `users_role_permissio_permission_id_5313a8eb_fk_sys_permi` FOREIGN KEY (`permission_id`) REFERENCES `sys_permission` (`id`),
  CONSTRAINT `users_role_permissions_role_id_b99e9f6e_fk_users_role_id` FOREIGN KEY (`role_id`) REFERENCES `users_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_role_permissions`
--

LOCK TABLES `users_role_permissions` WRITE;
/*!40000 ALTER TABLE `users_role_permissions` DISABLE KEYS */;
INSERT INTO `users_role_permissions` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,2,5);
/*!40000 ALTER TABLE `users_role_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visitor`
--

DROP TABLE IF EXISTS `visitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `visitor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `id_card` varchar(18) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `reason` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `visit_time` datetime(6) NOT NULL,
  `leave_time` datetime(6) DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `owner_id` bigint NOT NULL,
  `approve_remark` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `approve_time` datetime(6) DEFAULT NULL,
  `approve_user_id` bigint DEFAULT NULL,
  `enter_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `visitor_owner_id_6bd14ef9_fk_owner_id` (`owner_id`),
  KEY `visitor_approve_user_id_63fed1f1_fk_sys_user_id` (`approve_user_id`),
  CONSTRAINT `visitor_approve_user_id_63fed1f1_fk_sys_user_id` FOREIGN KEY (`approve_user_id`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `visitor_owner_id_6bd14ef9_fk_owner_id` FOREIGN KEY (`owner_id`) REFERENCES `owner` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visitor`
--

LOCK TABLES `visitor` WRITE;
/*!40000 ALTER TABLE `visitor` DISABLE KEYS */;
INSERT INTO `visitor` VALUES (1,'张三朋友','10000000010',NULL,'拜访','2026-06-05 18:00:00.000000','2026-06-09 03:12:50.475813','left','2026-06-05 08:59:12.325507',4,'','2026-06-08 10:06:09.389391',1,'2026-06-09 03:12:39.385409'),(2,'李朋友','10000000021','DEMO-ID-VISITOR-02','送文件，送快递','2026-06-08 14:21:17.000000','2026-06-09 03:10:48.669745','left','2026-06-08 06:40:59.149002',2,'允许进入','2026-06-08 08:35:06.269149',NULL,NULL);
/*!40000 ALTER TABLE `visitor` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-10 13:59:18
