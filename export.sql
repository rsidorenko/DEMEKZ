-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: furniture
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `birth_date` date NOT NULL,
  `passport` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bank_details` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `family` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `health` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `material_types`
--

DROP TABLE IF EXISTS `material_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `material_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `loss_percent` decimal(5,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `material_types`
--

LOCK TABLES `material_types` WRITE;
/*!40000 ALTER TABLE `material_types` DISABLE KEYS */;
INSERT INTO `material_types` VALUES (1,'Дерево',0.01),(2,'Древесная плита',0.00),(3,'Текстиль',0.00),(4,'Стекло',0.00),(5,'Металл',0.00),(6,'Пластик',0.00);
/*!40000 ALTER TABLE `material_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materials`
--

DROP TABLE IF EXISTS `materials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` int NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `supplier_id` int DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `unit_price` decimal(10,2) NOT NULL,
  `stock_quantity` decimal(10,2) NOT NULL,
  `min_quantity` decimal(10,2) NOT NULL,
  `package_quantity` decimal(10,2) NOT NULL,
  `unit` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `type` (`type`),
  KEY `supplier_id` (`supplier_id`),
  CONSTRAINT `materials_ibfk_1` FOREIGN KEY (`type`) REFERENCES `material_types` (`id`),
  CONSTRAINT `materials_ibfk_2` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materials`
--

LOCK TABLES `materials` WRITE;
/*!40000 ALTER TABLE `materials` DISABLE KEYS */;
INSERT INTO `materials` VALUES (1,1,'Цельный массив дерева Дуб 1000х600 мм',NULL,NULL,7450.00,1500.00,500.00,7.20,'м²'),(2,1,'Клееный массив дерева Дуб 1000х600 мм',NULL,NULL,4520.00,300.00,500.00,7.20,'м²'),(3,1,'Шпон облицовочный Дуб натуральный 2750х480 мм',NULL,NULL,2500.00,2000.00,1500.00,19.80,'м²'),(4,2,'Фанера 2200х1000 мм',NULL,NULL,2245.00,450.00,1000.00,52.80,'м²'),(5,2,'ДСП 2750х1830 мм',NULL,NULL,529.60,1010.00,1200.00,181.08,'м²'),(6,2,'МДФ 2070х1400 мм',NULL,NULL,417.24,1550.00,1000.00,87.00,'м²'),(7,2,'ДВП 2440х2050 мм',NULL,NULL,187.00,1310.00,1000.00,190.00,'м²'),(8,2,'ХДФ 2800x2070 мм',NULL,NULL,370.96,1400.00,1200.00,90.00,'м²'),(9,3,'Экокожа 140 см',NULL,NULL,1600.00,1200.00,1500.00,100.00,'пог.м'),(10,3,'Велюр 140 см',NULL,NULL,1300.00,1300.00,1500.00,100.00,'пог.м'),(11,3,'Шенилл 140 см',NULL,NULL,620.00,950.00,1500.00,100.00,'пог.м'),(12,3,'Рогожка 140 см',NULL,NULL,720.00,960.00,1500.00,100.00,'пог.м'),(13,4,'Закаленное стекло 2600х1800 мм',NULL,NULL,1148.00,1000.00,500.00,196.56,'м²'),(14,5,'Металлокаркас для стула',NULL,NULL,1100.00,300.00,250.00,5.00,'шт'),(15,5,'Металлокаркас каркас из профиля с траверсами для стола',NULL,NULL,6700.00,100.00,100.00,1.00,'шт'),(16,6,'Колесо для мебели поворотное',NULL,NULL,10.59,1500.00,1000.00,500.00,'шт'),(17,5,'Газ-лифт',NULL,NULL,730.00,500.00,250.00,5.00,'шт'),(18,5,'Металлическая крестовина для офисных кресел',NULL,NULL,2700.00,500.00,250.00,5.00,'шт'),(19,6,'Пластиковый комплект для стула',NULL,NULL,900.00,300.00,250.00,100.00,'шт'),(20,6,'Кромка ПВХ',NULL,NULL,35.80,1500.00,1000.00,100.00,'м');
/*!40000 ALTER TABLE `materials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partners`
--

DROP TABLE IF EXISTS `partners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `partners` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` enum('Розничный магазин','Оптовый магазин','Интернет-магазин') COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `inn` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `director` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rating` decimal(2,1) NOT NULL,
  `sales_volume` bigint NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `partners_chk_1` CHECK (((`rating` >= 0) and (`rating` <= 5)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partners`
--

LOCK TABLES `partners` WRITE;
/*!40000 ALTER TABLE `partners` DISABLE KEYS */;
/*!40000 ALTER TABLE `partners` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_materials`
--

DROP TABLE IF EXISTS `product_materials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_materials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `material_id` int NOT NULL,
  `quantity_needed` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `material_id` (`material_id`),
  CONSTRAINT `product_materials_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `product_materials_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `materials` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_materials`
--

LOCK TABLES `product_materials` WRITE;
/*!40000 ALTER TABLE `product_materials` DISABLE KEYS */;
INSERT INTO `product_materials` VALUES (1,1,4,0.85),(2,1,9,1.50),(3,1,11,1.50),(4,1,12,1.50),(5,1,14,1.00),(6,1,16,5.00),(7,1,17,1.00),(8,1,18,1.00),(9,1,19,1.00),(10,2,4,1.25),(11,2,10,3.04),(12,2,11,1.50),(13,2,12,2.50),(14,2,14,1.00),(15,2,16,5.00),(16,2,17,1.00),(17,2,18,1.00),(18,2,19,1.00),(19,3,4,1.85),(20,3,10,4.22),(21,3,9,1.50),(22,3,14,1.00),(23,3,16,5.00),(24,3,17,1.00),(25,3,18,1.00),(26,3,19,1.00),(27,4,5,3.33),(28,4,20,6.00),(29,5,1,2.90),(30,5,3,1.70),(31,5,6,2.70),(32,5,8,1.80),(33,6,1,1.70),(34,6,3,1.60),(35,6,8,1.80),(36,7,5,2.00),(37,7,7,0.80),(38,7,20,7.00),(39,8,6,5.95),(40,8,15,1.00),(41,9,5,4.30),(42,9,20,8.60),(43,10,6,7.65),(44,10,8,1.05),(45,10,15,1.00),(46,11,5,6.40),(47,11,20,6.20),(48,12,4,2.55),(49,12,5,5.20),(50,12,7,3.59),(51,12,20,9.40),(52,13,2,3.50),(53,13,3,1.50),(54,13,8,2.10),(55,13,13,0.80),(56,14,2,7.70),(57,14,3,6.50),(58,14,5,4.50),(59,14,6,5.70),(60,14,8,2.30),(61,14,10,1.74),(62,15,5,4.20),(63,15,7,2.21),(64,15,16,4.00),(65,15,20,6.50),(66,16,1,0.40),(67,16,16,4.00),(68,17,3,0.70),(69,17,5,7.65),(70,17,7,0.80),(71,17,20,6.30),(72,18,3,3.20),(73,18,4,3.50),(74,18,7,1.60),(75,18,13,1.60),(76,19,3,1.30),(77,19,5,8.20),(78,19,8,1.30),(79,20,2,1.80),(80,20,3,3.50),(81,20,8,1.65),(82,20,13,1.60);
/*!40000 ALTER TABLE `product_materials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_types`
--

DROP TABLE IF EXISTS `product_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type_coefficient` decimal(5,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type_name` (`type_name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_types`
--

LOCK TABLES `product_types` WRITE;
/*!40000 ALTER TABLE `product_types` DISABLE KEYS */;
INSERT INTO `product_types` VALUES (1,'Кресла',1.95),(2,'Полки',2.50),(3,'Стеллажи',4.35),(4,'Столы',5.50),(5,'Тумбы',7.60),(6,'Шкафы',6.72);
/*!40000 ALTER TABLE `product_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` int NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `article` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `price` decimal(10,2) NOT NULL,
  `size_length` decimal(10,2) NOT NULL,
  `size_width` decimal(10,2) NOT NULL,
  `size_height` decimal(10,2) NOT NULL,
  `weight` decimal(10,2) NOT NULL,
  `manufacture_time` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `article` (`article`),
  KEY `type` (`type`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`type`) REFERENCES `product_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,1,'Кресло детское цвет Белый и Розовый','3028272',NULL,15324.99,600.00,600.00,800.00,15.50,NULL),(2,1,'Кресло офисное цвет Черный','3018556',NULL,21443.99,650.00,650.00,1100.00,25.00,NULL),(3,1,'Кресло эргономичное цвет Темно-коричневый','3549922',NULL,24760.00,700.00,700.00,1200.00,30.00,NULL),(4,2,'Полка настольная','7028048',NULL,2670.89,400.00,300.00,200.00,5.00,NULL),(5,3,'Стеллаж для документов цвет Дуб светлый','5759324',NULL,24899.00,854.00,445.00,2105.00,45.00,NULL),(6,3,'Стеллаж цвет Белый с ящиками','5259474',NULL,16150.00,854.00,445.00,2105.00,50.00,NULL),(7,3,'Стеллаж цвет Орех','5118827',NULL,2860.00,400.00,370.00,2000.00,35.00,NULL),(8,3,'Узкий пенал стеллаж 5 полок цвет Орех','5559898',NULL,8348.00,364.00,326.00,2000.00,30.00,NULL),(9,4,'Стол для ноутбука на металлокаркасе','1029784',NULL,14690.00,800.00,600.00,123.00,20.00,NULL),(10,4,'Стол компьютерный','1028248',NULL,4105.89,700.00,600.00,500.00,25.00,NULL),(11,4,'Стол компьютерный на металлокаркасе','1130981',NULL,13899.00,1400.00,600.00,750.00,35.00,NULL),(12,4,'Стол письменный','1188827',NULL,5148.00,1100.00,750.00,600.00,30.00,NULL),(13,4,'Стол письменный с тумбочкой 4 ящика','1029272',NULL,15325.00,1100.00,750.00,600.00,40.00,NULL),(14,4,'Стол руководителя письменный цвет Венге','1016662',NULL,43500.90,1600.00,800.00,764.00,45.00,NULL),(15,4,'Стол руководителя письменный цвет Орех темный','1658953',NULL,132500.00,2300.00,1000.00,750.00,60.00,NULL),(16,5,'Тумба выкатная 3 ящика','6033136',NULL,3750.00,400.00,400.00,600.00,25.00,NULL),(17,5,'Тумба офисная для оргтехники','6115947',NULL,2450.00,500.00,400.00,700.00,30.00,NULL),(18,6,'Шкаф для книг','4159043',NULL,23390.99,800.00,420.00,2000.00,50.00,NULL),(19,6,'Шкаф для одежды цвет Венге','4758375',NULL,12035.00,602.00,420.00,2000.00,45.00,NULL),(20,6,'Шкаф-витрина 2 ящика','4588376',NULL,31991.00,800.00,420.00,2000.00,55.00,NULL);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `inn` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `supplier_type` enum('Розничный магазин','Оптовый магазин','Интернет-магазин') COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-17  2:07:35
