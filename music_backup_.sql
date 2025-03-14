-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: music_website
-- ------------------------------------------------------
-- Server version	8.0.41

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

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add 鎿嶄綔鏃ュ織',7,'add_adminlog'),(26,'Can change 鎿嶄綔鏃ュ織',7,'change_adminlog'),(27,'Can delete 鎿嶄綔鏃ュ織',7,'delete_adminlog'),(28,'Can view 鎿嶄綔鏃ュ織',7,'view_adminlog'),(29,'Can add 闊充箰浣滃搧',8,'add_music'),(30,'Can change 闊充箰浣滃搧',8,'change_music'),(31,'Can delete 闊充箰浣滃搧',8,'delete_music'),(32,'Can view 闊充箰浣滃搧',8,'view_music'),(33,'Can add 鐢ㄦ埛璇勮',9,'add_comment'),(34,'Can change 鐢ㄦ埛璇勮',9,'change_comment'),(35,'Can delete 鐢ㄦ埛璇勮',9,'delete_comment'),(36,'Can view 鐢ㄦ埛璇勮',9,'view_comment'),(37,'Can add 鐢ㄦ埛璧勬枡',10,'add_profile'),(38,'Can change 鐢ㄦ埛璧勬枡',10,'change_profile'),(39,'Can delete 鐢ㄦ埛璧勬枡',10,'delete_profile'),(40,'Can view 鐢ㄦ埛璧勬枡',10,'view_profile');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$870000$28Tq5lSkLp77b1ecCXiTl1$OfSnSPZUz9IqPwLVCfTAPs2ObOShWM5vLaN0LqQswF0=','2025-02-28 09:40:29.054091',1,'shengjieping','','','shengjieping@zerozero.cn',1,1,'2025-02-28 09:39:35.272749');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
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
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
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
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'music','adminlog'),(9,'music','comment'),(8,'music','music'),(10,'music','profile'),(6,'sessions','session');
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
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-02-28 09:34:51.803114'),(2,'auth','0001_initial','2025-02-28 09:34:52.346769'),(3,'admin','0001_initial','2025-02-28 09:34:52.530447'),(4,'admin','0002_logentry_remove_auto_add','2025-02-28 09:34:52.537499'),(5,'admin','0003_logentry_add_action_flag_choices','2025-02-28 09:34:52.542497'),(6,'contenttypes','0002_remove_content_type_name','2025-02-28 09:34:52.643121'),(7,'auth','0002_alter_permission_name_max_length','2025-02-28 09:34:52.706484'),(8,'auth','0003_alter_user_email_max_length','2025-02-28 09:34:52.738819'),(9,'auth','0004_alter_user_username_opts','2025-02-28 09:34:52.745823'),(10,'auth','0005_alter_user_last_login_null','2025-02-28 09:34:52.803965'),(11,'auth','0006_require_contenttypes_0002','2025-02-28 09:34:52.807269'),(12,'auth','0007_alter_validators_add_error_messages','2025-02-28 09:34:52.812962'),(13,'auth','0008_alter_user_username_max_length','2025-02-28 09:34:52.866052'),(14,'auth','0009_alter_user_last_name_max_length','2025-02-28 09:34:52.924119'),(15,'auth','0010_alter_group_name_max_length','2025-02-28 09:34:52.940994'),(16,'auth','0011_update_proxy_permissions','2025-02-28 09:34:52.949507'),(17,'auth','0012_alter_user_first_name_max_length','2025-02-28 09:34:53.008397'),(18,'music','0001_initial','2025-02-28 09:34:53.389581'),(19,'sessions','0001_initial','2025-02-28 09:34:53.429517');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2h1zhgle4i8v7aqoml1gqnl31ok0mrrl','.eJxVjEsOwiAUAO_C2pDy57l07xnIe0ClaiAp7cp4dyXpQrczk3mxgPtWwt7zGpbEzkyw0y8jjI9ch0h3rLfGY6vbuhAfCT9s59eW8vNytH-Dgr2MbSZP87efwCfpVUouAkwUZ4IIkixEZVFnqYUwwiiwGslY4wCN89qy9wcB1je3:1tnwr7:d20Ut9Z-RiEs4TiY0kKALUjR7wa5kVryLqBbwUuF23I','2025-03-14 09:40:29.057093');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `music_adminlog`
--

DROP TABLE IF EXISTS `music_adminlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `music_adminlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `action` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `target` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `music_adminlog_user_id_1d3379c2_fk_auth_user_id` (`user_id`),
  CONSTRAINT `music_adminlog_user_id_1d3379c2_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `music_adminlog`
--

LOCK TABLES `music_adminlog` WRITE;
/*!40000 ALTER TABLE `music_adminlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `music_adminlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `music_comment`
--

DROP TABLE IF EXISTS `music_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `music_comment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `music_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `music_comment_user_id_0d3cd408_fk_auth_user_id` (`user_id`),
  KEY `music_comment_music_id_0d592a3b_fk_music_music_id` (`music_id`),
  CONSTRAINT `music_comment_music_id_0d592a3b_fk_music_music_id` FOREIGN KEY (`music_id`) REFERENCES `music_music` (`id`),
  CONSTRAINT `music_comment_user_id_0d3cd408_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `music_comment`
--

LOCK TABLES `music_comment` WRITE;
/*!40000 ALTER TABLE `music_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `music_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `music_music`
--

DROP TABLE IF EXISTS `music_music`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `music_music` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `artist` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `album` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `release_date` date NOT NULL,
  `audio_file` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cover_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lyrics` longtext COLLATE utf8mb4_unicode_ci,
  `play_count` int unsigned NOT NULL,
  `likes` int unsigned NOT NULL,
  `is_original` tinyint(1) NOT NULL,
  `category` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `download_count` int unsigned NOT NULL,
  `uploaded_by_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `music_music_uploaded_by_id_090b23d1_fk_auth_user_id` (`uploaded_by_id`),
  CONSTRAINT `music_music_uploaded_by_id_090b23d1_fk_auth_user_id` FOREIGN KEY (`uploaded_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `music_music_chk_1` CHECK ((`play_count` >= 0)),
  CONSTRAINT `music_music_chk_2` CHECK ((`likes` >= 0)),
  CONSTRAINT `music_music_chk_3` CHECK ((`download_count` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `music_music`
--

LOCK TABLES `music_music` WRITE;
/*!40000 ALTER TABLE `music_music` DISABLE KEYS */;
INSERT INTO `music_music` VALUES (1,'涓滈鐮?,'鍛ㄦ澃L','涓滈鐮?,'2003-07-31','music/4bd10a95-0f39-4bdd-9e4f-9635852b7662.mp3','covers/2025/02/28/4fd20265-aba7-490f-8484-7b9e682fc02a.jpg','[00:01.00]姝屾洸鍚?涓滈鐮?Album Version)\r\n[00:02.00]姝屾墜鍚?鍛ㄦ澃浼r\n[00:03.00]浣滆瘝锛氭柟鏂囧北\r\n[00:04.00]浣滄洸锛氬懆鏉颁鸡\r\n[00:14.06]涓€鐩忕鎰佸鐏极绔嬪湪绐楀彛\r\n[00:20.50]鎴戝湪闂ㄥ悗鍋囪浣犱汉杩樻病璧癨r\n[00:26.98]鏃у湴濡傞噸娓告湀鍦嗘洿瀵傚癁\r\n[00:33.67]澶滃崐娓呴啋鐨勭儧鐏笉蹇嶈嫑璐ｆ垜\r\n[00:40.15]涓€澹舵紓娉婃氮杩瑰ぉ娑毦鍏ュ枆\r\n[00:46.90]浣犺蛋涔嬪悗閰掓殩鍥炲繂鎬濆康鐦r\n[00:53.33]姘村悜涓滄祦鏃堕棿鎬庝箞鍋穃r\n[01:00.00]鑺卞紑灏变竴娆℃垚鐔熸垜鍗撮敊杩嘰r\n[01:09.75]璋佸湪鐢ㄧ惖鐞跺脊濂忎竴鏇蹭笢椋庣牬\r\n[01:16.28]宀佹湀鍦ㄥ涓婂墺钀界湅瑙佸皬鏃跺€橽r\n[01:22.94]鐘硅寰楅偅骞存垜浠兘杩樺緢骞村辜\r\n[01:29.60]鑰屽浠婄惔澹板菇骞絓r\n[01:32.28]鎴戠殑绛夊€欎綘娌″惉杩嘰r\n[01:35.98]璋佸湪鐢ㄧ惖鐞跺脊濂忎竴鏇蹭笢椋庣牬\r\n[01:42.61]鏋彾灏嗘晠浜嬫煋鑹茬粨灞€鎴戠湅閫廫r\n[01:49.15]绡辩瑔澶栫殑鍙ら亾鎴戠壍鐫€浣犺蛋杩嘰r\n[01:55.89]鑽掔儫婕崏鐨勫勾澶碶r\n[01:58.94]灏辫繛鍒嗘墜閮藉緢娌夐粯\r\n[02:28.53]涓€澹舵紓娉婃氮杩瑰ぉ娑毦鍏ュ枆\r\n[02:35.22]浣犺蛋涔嬪悗閰掓殩鍥炲繂鎬濆康鐦r\n[02:41.73]姘村悜涓滄祦鏃堕棿鎬庝箞鍋穃r\n[02:48.45]鑺卞紑灏变竴娆℃垚鐔熸垜鍗撮敊杩嘰r\n[02:58.25]璋佸湪鐢ㄧ惖鐞跺脊濂忎竴鏇蹭笢椋庣牬\r\n[03:04.79]宀佹湀鍦ㄥ涓婂墺钀界湅瑙佸皬鏃跺€橽r\n[03:11.47]鐘硅寰楅偅骞存垜浠兘杩樺緢骞村辜\r\n[03:17.86]鑰屽浠婄惔澹板菇骞絓r\n[03:20.66]鎴戠殑绛夊€欎綘娌″惉杩嘰r\n[03:24.50]璋佸湪鐢ㄧ惖鐞跺脊濂忎竴鏇蹭笢椋庣牬\r\n[03:31.13]鏋彾灏嗘晠浜嬫煋鑹茬粨灞€鎴戠湅閫廫r\n[03:37.67]绡辩瑔澶栫殑鍙ら亾鎴戠壍鐫€浣犺蛋杩嘰r\n[03:44.29]鑽掔儫婕崏鐨勫勾澶碶r\n[03:47.53]灏辫繛鍒嗘墜閮絓r\n[03:50.82]璋佸湪鐢ㄧ惖鐞跺脊濂忎竴鏇蹭笢椋庣牬\r\n[03:57.41]宀佹湀鍦ㄥ涓婂墺钀界湅瑙佸皬鏃跺€橽r\n[04:04.04]鐘硅寰楅偅骞存垜浠兘杩樺緢骞村辜\r\n[04:10.43]鑰屽浠婄惔澹板菇骞絓r\n[04:13.28]鎴戠殑绛夊€欎綘娌″惉杩嘰r\n[04:17.08]璋佸湪鐢ㄧ惖鐞跺脊濂忎竴鏇蹭笢椋庣牬\r\n[04:23.71]鏋彾灏嗘晠浜嬫煋鑹茬粨灞€鎴戠湅閫廫r\n[04:30.41]绡辩瑔澶栫殑鍙ら亾鎴戠壍鐫€浣犺蛋杩嘰r\n[04:36.78]鑽掔儫婕崏鐨勫勾澶碶r\n[04:40.09]灏辫繛鍒嗘墜閮藉緢娌夐粯',7,0,0,'pop',0,1);
/*!40000 ALTER TABLE `music_music` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `music_profile`
--

DROP TABLE IF EXISTS `music_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `music_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bio` longtext COLLATE utf8mb4_unicode_ci,
  `avatar` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `location` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `music_profile_user_id_812c29e6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `music_profile`
--

LOCK TABLES `music_profile` WRITE;
/*!40000 ALTER TABLE `music_profile` DISABLE KEYS */;
INSERT INTO `music_profile` VALUES (1,NULL,'avatars/default.png',NULL,1);
/*!40000 ALTER TABLE `music_profile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-28 18:16:09
