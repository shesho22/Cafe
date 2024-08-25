-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: juegos_db
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `consola`
--

DROP TABLE IF EXISTS `consola`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consola` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `marca` varchar(50) DEFAULT NULL,
  `detalles` text,
  `estado` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consola`
--

LOCK TABLES `consola` WRITE;
/*!40000 ALTER TABLE `consola` DISABLE KEYS */;
INSERT INTO `consola` VALUES (1,'ps4','sony','ni idea ','libre');
/*!40000 ALTER TABLE `consola` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imagen`
--

DROP TABLE IF EXISTS `imagen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imagen` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ruta` varchar(255) NOT NULL,
  `id_juego_mesa` int DEFAULT NULL,
  `id_juego_consola` int DEFAULT NULL,
  `id_consola` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_juego_mesa` (`id_juego_mesa`),
  KEY `id_juego_consola` (`id_juego_consola`),
  KEY `id_consola` (`id_consola`),
  CONSTRAINT `imagen_ibfk_1` FOREIGN KEY (`id_juego_mesa`) REFERENCES `juego_de_mesa` (`id`),
  CONSTRAINT `imagen_ibfk_2` FOREIGN KEY (`id_juego_consola`) REFERENCES `juego_de_consola` (`id`),
  CONSTRAINT `imagen_ibfk_3` FOREIGN KEY (`id_consola`) REFERENCES `consola` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imagen`
--

LOCK TABLES `imagen` WRITE;
/*!40000 ALTER TABLE `imagen` DISABLE KEYS */;
INSERT INTO `imagen` VALUES (1,'uploads/jeng.jpeg',1,NULL,NULL),(2,'uploads/jen.jpeg',1,NULL,NULL),(3,'uploads/ps4.jpeg',NULL,NULL,1),(4,'uploads/ajedrez.jpeg',2,NULL,NULL);
/*!40000 ALTER TABLE `imagen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `juego_de_consola`
--

DROP TABLE IF EXISTS `juego_de_consola`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `juego_de_consola` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `detalles` text,
  `estado` varchar(50) DEFAULT NULL,
  `id_consola` int DEFAULT NULL,
  `genero` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_consola` (`id_consola`),
  CONSTRAINT `juego_de_consola_ibfk_1` FOREIGN KEY (`id_consola`) REFERENCES `consola` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `juego_de_consola`
--

LOCK TABLES `juego_de_consola` WRITE;
/*!40000 ALTER TABLE `juego_de_consola` DISABLE KEYS */;
/*!40000 ALTER TABLE `juego_de_consola` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `juego_de_mesa`
--

DROP TABLE IF EXISTS `juego_de_mesa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `juego_de_mesa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `genero` varchar(50) DEFAULT NULL,
  `instrucciones` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `juego_de_mesa`
--

LOCK TABLES `juego_de_mesa` WRITE;
/*!40000 ALTER TABLE `juego_de_mesa` DISABLE KEYS */;
INSERT INTO `juego_de_mesa` VALUES (1,'Jenga ','no se ','familiar ','sacar palos '),(2,'aje','yhgluiokjhb','familiar ','yutfgj');
/*!40000 ALTER TABLE `juego_de_mesa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Pues yo ','scrypt:32768:8:1$fqnIbbOImFGnF6YF$9cfb522ed9041ac48d36559644850771164c25efa81828e9b92c7d9e1f4d21516335217b541b2bc36c276240f0e0d305049c9e942eac1afd2ad93c0cd25183d9'),(2,'Pues yo1','scrypt:32768:8:1$QSBph8cEvrG0yIzw$4be75969890bc7f1280ec0f47e872b5fd3a4b80badec21c0fa458546fb27434876e066e59cfe7396ffb280839ef61db8606c5dbe748f34668997d3f6e0ba2607'),(3,'dsfgfhtjgj','scrypt:32768:8:1$MzLpF5UZXt7bQkGL$a8ea61a813bccbd9bd26779447f4dab344be97ddf4399f79e3d3b4a236d7d8c879e0b2bcfa0358b655e92ecc58b0f7e99bf73b3547126ad5d35f94a52a019a08');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-25  0:28:46
