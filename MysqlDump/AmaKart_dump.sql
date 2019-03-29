-- MySQL dump 10.17  Distrib 10.3.13-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: AmaKart
-- ------------------------------------------------------
-- Server version	10.3.13-MariaDB-1:10.3.13+maria~bionic-log

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
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Users` (
  `username` varchar(20) NOT NULL,
  `passcode` varchar(20) NOT NULL,
  `roles` varchar(20) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES ('BlueDart','hi','shipper'),('FEDEx','hi','shipper'),('Harry','hi','seller'),('John','hi','customer'),('Nikhil','hi','customer'),('Sourabh','hi','seller');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cart` (
  `customer_id` varchar(20) NOT NULL,
  `product_id` varchar(20) NOT NULL,
  `seller_id` varchar(20) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`customer_id`,`product_id`,`seller_id`),
  KEY `product_id` (`product_id`,`seller_id`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE CASCADE,
  CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`, `seller_id`) REFERENCES `product` (`product_id`, `seller_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES ('John','2','Sourabh',10),('Nikhil','1','Sourabh',2);
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER validCartinsert BEFORE INSERT on cart
FOR EACH ROW BEGIN
    IF (NEW.quantity > all(SELECT total_stock FROM product WHERE product.product_id = NEW.product_id AND product.seller_id = NEW.seller_id)) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Not possible';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER validCartupdate BEFORE UPDATE on cart
FOR EACH ROW BEGIN
    IF (NEW.quantity > all(SELECT total_stock FROM product WHERE product.product_id = NEW.product_id AND product.seller_id = NEW.seller_id)) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Not possible';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
  `customer_id` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(60) NOT NULL,
  `phone_number` decimal(10,0) unsigned NOT NULL,
  `email_id` varchar(20) NOT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES ('John','John Snow','ROOM-111',8281112706,'121601013@'),('Nikhil','Nikhil Kumar','ROOM-119',8281112705,'111601013@');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `customerProfile`
--

DROP TABLE IF EXISTS `customerProfile`;
/*!50001 DROP VIEW IF EXISTS `customerProfile`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `customerProfile` (
  `customer_id` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `address` tinyint NOT NULL,
  `phone_number` tinyint NOT NULL,
  `email_id` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `listOrders`
--

DROP TABLE IF EXISTS `listOrders`;
/*!50001 DROP VIEW IF EXISTS `listOrders`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `listOrders` (
  `order_id` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `orderPrice`
--

DROP TABLE IF EXISTS `orderPrice`;
/*!50001 DROP VIEW IF EXISTS `orderPrice`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `orderPrice` (
  `order_id` tinyint NOT NULL,
  `total_price` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `order_`
--

DROP TABLE IF EXISTS `order_`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_` (
  `order_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` varchar(20) DEFAULT NULL,
  `shipping_address` varchar(60) NOT NULL,
  `payment_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`order_id`),
  KEY `customer_id` (`customer_id`),
  KEY `payment_id` (`payment_id`),
  CONSTRAINT `order__ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE SET NULL,
  CONSTRAINT `order__ibfk_2` FOREIGN KEY (`payment_id`) REFERENCES `payment` (`payment_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_`
--

LOCK TABLES `order_` WRITE;
/*!40000 ALTER TABLE `order_` DISABLE KEYS */;
INSERT INTO `order_` VALUES (1,'Nikhil','RM-119',1),(2,'Nikhil','RM123',2),(3,'John','RM123',3);
/*!40000 ALTER TABLE `order_` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `packageStatus`
--

DROP TABLE IF EXISTS `packageStatus`;
/*!50001 DROP VIEW IF EXISTS `packageStatus`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `packageStatus` (
  `order_id` tinyint NOT NULL,
  `product_id` tinyint NOT NULL,
  `ship_index` tinyint NOT NULL,
  `tracking_id` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `credit_card_number` varchar(20) NOT NULL,
  `date_` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `billing_address` varchar(60) NOT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (1,'4362536563578','2018-12-31 18:30:00','CompLabFF'),(2,'1234567890','2019-03-29 18:34:24','RM123'),(3,'1234567890','2019-03-29 18:45:35','RM123');
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `previousOrders`
--

DROP TABLE IF EXISTS `previousOrders`;
/*!50001 DROP VIEW IF EXISTS `previousOrders`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `previousOrders` (
  `order_id` tinyint NOT NULL,
  `shipping_address` tinyint NOT NULL,
  `date_` tinyint NOT NULL,
  `total_price` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `product_id` varchar(20) NOT NULL,
  `product_name` varchar(20) NOT NULL,
  `product_image` varchar(300) DEFAULT NULL,
  `seller_id` varchar(20) NOT NULL,
  `price` float NOT NULL,
  `total_stock` int(11) DEFAULT NULL,
  `pickup_address` varchar(60) NOT NULL,
  `description` varchar(60) DEFAULT NULL,
  `rating` float DEFAULT NULL,
  PRIMARY KEY (`product_id`,`seller_id`),
  KEY `seller_id` (`seller_id`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`seller_id`) REFERENCES `seller` (`seller_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES ('1','Rasgulla','https://i.ndtvimg.com/i/2017-10/rasgulla-recipe_620x330_51508133855.jpg?downsize=650:400&output-quality=70&output-format=webp','Harry',10,15,'RM3oo','Best',NULL),('1','Rasgulla','https://i.ndtvimg.com/i/2017-10/rasgulla-recipe_620x330_51508133855.jpg?downsize=650:400&output-quality=70&output-format=webp','Sourabh',10,88,'RM3xx','Rasgulla from Aggarwal Sweets',NULL),('2','Gulab Jamun','http://www.manjulaskitchen.com/blog/wp-content/uploads/gulab_jamun1.jpg','Sourabh',100,90,'RM3xx','Gulab Jamun from Aggarwal Sweets',NULL),('3','Addidas Shoes','https://assets.adidas.com/images/w_600,f_auto,q_auto/0ffa27e83b4f44b4821ba8b20082b44b_9366/SolarBoost_Shoes_Black_CQ3168_01_standard.jpg','Harry',10000,8,'Bangalore','Original product',NULL),('4','Samsung S10','https://images.anandtech.com/doci/14121/samsung-s10_678x452_575px.jpg','Harry',80000,999,'Hyderabad','On screen fingerprint scanner ...',5);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_order`
--

DROP TABLE IF EXISTS `product_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_order` (
  `product_id` varchar(20) NOT NULL,
  `order_id` int(11) NOT NULL,
  `seller_id` varchar(20) NOT NULL,
  `product_rating` int(11) DEFAULT NULL CHECK (`product_rating` in (NULL,1,2,3,4,5)),
  `seller_rating` int(11) DEFAULT NULL CHECK (`seller_rating` in (NULL,1,2,3,4,5)),
  `ship_index` int(11) DEFAULT NULL,
  `product_review` varchar(60) DEFAULT NULL,
  `seller_review` varchar(60) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `selling_price` float DEFAULT NULL,
  PRIMARY KEY (`product_id`,`order_id`,`seller_id`),
  KEY `order_id` (`order_id`),
  KEY `seller_id` (`seller_id`),
  KEY `ship_index` (`ship_index`),
  CONSTRAINT `product_order_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON DELETE CASCADE,
  CONSTRAINT `product_order_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `order_` (`order_id`) ON DELETE CASCADE,
  CONSTRAINT `product_order_ibfk_3` FOREIGN KEY (`seller_id`) REFERENCES `seller` (`seller_id`) ON DELETE CASCADE,
  CONSTRAINT `product_order_ibfk_4` FOREIGN KEY (`ship_index`) REFERENCES `track` (`index_`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_order`
--

LOCK TABLES `product_order` WRITE;
/*!40000 ALTER TABLE `product_order` DISABLE KEYS */;
INSERT INTO `product_order` VALUES ('1',1,'Sourabh',5,4,1,NULL,NULL,10,10),('1',2,'Sourabh',NULL,NULL,2,NULL,NULL,2,10),('2',3,'Sourabh',NULL,NULL,4,NULL,NULL,10,100),('3',3,'Harry',NULL,NULL,5,NULL,NULL,2,10000),('4',2,'Harry',5,4,3,'Very Nice Product','Seller is bit lazy.',1,80000);
/*!40000 ALTER TABLE `product_order` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER setPrice BEFORE INSERT on product_order
FOR EACH ROW BEGIN
  SET NEW.selling_price = (SELECT price FROM product WHERE product_id = NEW.product_id and seller_id = NEW.seller_id);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER stockCheckandaddTrack BEFORE INSERT on product_order
FOR EACH ROW BEGIN
  UPDATE product set total_stock = total_stock - NEW.quantity WHERE product_id = NEW.product_id and seller_id = NEW.seller_id;
  INSERT INTO track () Values ();
  SET NEW.ship_index = (SELECT MAX(index_) FROM track);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER updateRatingProduct AFTER UPDATE on product_order
FOR EACH ROW BEGIN
  UPDATE product SET rating = (SELECT (AVG(product_rating)) FROM product_order WHERE product_id = NEW.product_id) WHERE product_id = NEW.product_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER updateRatingSeller AFTER UPDATE on product_order
FOR EACH ROW BEGIN
  UPDATE seller SET rating = (SELECT (AVG(seller_rating)) FROM product_order WHERE seller_id = NEW.seller_id) WHERE seller_id = NEW.seller_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `seller`
--

DROP TABLE IF EXISTS `seller`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `seller` (
  `seller_id` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(60) NOT NULL,
  `phone_number` decimal(10,0) unsigned NOT NULL,
  `email_id` varchar(20) NOT NULL,
  `rating` float DEFAULT NULL,
  PRIMARY KEY (`seller_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seller`
--

LOCK TABLES `seller` WRITE;
/*!40000 ALTER TABLE `seller` DISABLE KEYS */;
INSERT INTO `seller` VALUES ('Harry','Harry Potter','ROOM-311',8281112701,'121601025@',4),('Sourabh','Sourabh Agg','ROOM-211',8281112700,'111601025@',NULL);
/*!40000 ALTER TABLE `seller` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `sellerOrders`
--

DROP TABLE IF EXISTS `sellerOrders`;
/*!50001 DROP VIEW IF EXISTS `sellerOrders`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `sellerOrders` (
  `seller_id` tinyint NOT NULL,
  `product_id` tinyint NOT NULL,
  `quantity` tinyint NOT NULL,
  `selling_price` tinyint NOT NULL,
  `date_` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `sellerProducts`
--

DROP TABLE IF EXISTS `sellerProducts`;
/*!50001 DROP VIEW IF EXISTS `sellerProducts`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `sellerProducts` (
  `product_id` tinyint NOT NULL,
  `product_name` tinyint NOT NULL,
  `price` tinyint NOT NULL,
  `total_stock` tinyint NOT NULL,
  `pickup_address` tinyint NOT NULL,
  `description` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `sellerProfile`
--

DROP TABLE IF EXISTS `sellerProfile`;
/*!50001 DROP VIEW IF EXISTS `sellerProfile`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `sellerProfile` (
  `seller_id` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `address` tinyint NOT NULL,
  `phone_number` tinyint NOT NULL,
  `email_id` tinyint NOT NULL,
  `rating` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `shipper`
--

DROP TABLE IF EXISTS `shipper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipper` (
  `shipper_id` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `head_quarters` varchar(60) NOT NULL,
  `phone_number` decimal(10,0) unsigned NOT NULL,
  `email_id` varchar(20) NOT NULL,
  PRIMARY KEY (`shipper_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shipper`
--

LOCK TABLES `shipper` WRITE;
/*!40000 ALTER TABLE `shipper` DISABLE KEYS */;
INSERT INTO `shipper` VALUES ('BlueDart','BlueDart','Bangalore',1800123344,'121601020@'),('FEDEx','FEDEx','Delhi',1800123343,'111601020@');
/*!40000 ALTER TABLE `shipper` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `shipperProfile`
--

DROP TABLE IF EXISTS `shipperProfile`;
/*!50001 DROP VIEW IF EXISTS `shipperProfile`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `shipperProfile` (
  `shipper_id` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `head_quarters` tinyint NOT NULL,
  `phone_number` tinyint NOT NULL,
  `email_id` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `shipperTrack`
--

DROP TABLE IF EXISTS `shipperTrack`;
/*!50001 DROP VIEW IF EXISTS `shipperTrack`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `shipperTrack` (
  `index_` tinyint NOT NULL,
  `source` tinyint NOT NULL,
  `destination` tinyint NOT NULL,
  `tracking_id` tinyint NOT NULL,
  `date_` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `showCart`
--

DROP TABLE IF EXISTS `showCart`;
/*!50001 DROP VIEW IF EXISTS `showCart`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `showCart` (
  `customer_id` tinyint NOT NULL,
  `product_id` tinyint NOT NULL,
  `seller_id` tinyint NOT NULL,
  `quantity` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `track`
--

DROP TABLE IF EXISTS `track`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `track` (
  `index_` int(11) NOT NULL AUTO_INCREMENT,
  `shipper_id` varchar(20) DEFAULT NULL,
  `tracking_id` varchar(20) DEFAULT NULL,
  `date_` date DEFAULT NULL,
  PRIMARY KEY (`index_`),
  KEY `shipper_id` (`shipper_id`),
  CONSTRAINT `track_ibfk_1` FOREIGN KEY (`shipper_id`) REFERENCES `shipper` (`shipper_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `track`
--

LOCK TABLES `track` WRITE;
/*!40000 ALTER TABLE `track` DISABLE KEYS */;
INSERT INTO `track` VALUES (1,'FEDEx','EPIN290348AD7','2019-03-29'),(2,NULL,NULL,NULL),(3,'BlueDart','12354','2019-03-30'),(4,NULL,NULL,NULL),(5,NULL,NULL,NULL);
/*!40000 ALTER TABLE `track` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `trackID`
--

DROP TABLE IF EXISTS `trackID`;
/*!50001 DROP VIEW IF EXISTS `trackID`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `trackID` (
  `order_id` tinyint NOT NULL,
  `product_id` tinyint NOT NULL,
  `ship_index` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `customerProfile`
--

/*!50001 DROP TABLE IF EXISTS `customerProfile`*/;
/*!50001 DROP VIEW IF EXISTS `customerProfile`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `customerProfile` AS (select `customer`.`customer_id` AS `customer_id`,`customer`.`name` AS `name`,`customer`.`address` AS `address`,`customer`.`phone_number` AS `phone_number`,`customer`.`email_id` AS `email_id` from `customer` where concat(`customer`.`customer_id`,'@localhost') in (select user())) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `listOrders`
--

/*!50001 DROP TABLE IF EXISTS `listOrders`*/;
/*!50001 DROP VIEW IF EXISTS `listOrders`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `listOrders` AS (select `order_`.`order_id` AS `order_id` from `order_` where concat(`order_`.`customer_id`,'@localhost') in (select user())) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `orderPrice`
--

/*!50001 DROP TABLE IF EXISTS `orderPrice`*/;
/*!50001 DROP VIEW IF EXISTS `orderPrice`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `orderPrice` AS (select `product_order`.`order_id` AS `order_id`,sum(`product_order`.`selling_price` * `product_order`.`quantity`) AS `total_price` from `product_order` group by `product_order`.`order_id`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `packageStatus`
--

/*!50001 DROP TABLE IF EXISTS `packageStatus`*/;
/*!50001 DROP VIEW IF EXISTS `packageStatus`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `packageStatus` AS (select `T1`.`order_id` AS `order_id`,`T1`.`product_id` AS `product_id`,`T1`.`ship_index` AS `ship_index`,`T2`.`tracking_id` AS `tracking_id` from (`trackID` `T1` join `track` `T2` on(`T1`.`ship_index` = `T2`.`index_`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `previousOrders`
--

/*!50001 DROP TABLE IF EXISTS `previousOrders`*/;
/*!50001 DROP VIEW IF EXISTS `previousOrders`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `previousOrders` AS (select `T1`.`order_id` AS `order_id`,`T1`.`shipping_address` AS `shipping_address`,`T2`.`date_` AS `date_`,`T3`.`total_price` AS `total_price` from ((`order_` `T1` join `payment` `T2` on(`T1`.`payment_id` = `T2`.`payment_id`)) join `orderPrice` `T3` on(`T1`.`order_id` = `T3`.`order_id`)) where concat(`T1`.`customer_id`,'@localhost') in (select user())) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `sellerOrders`
--

/*!50001 DROP TABLE IF EXISTS `sellerOrders`*/;
/*!50001 DROP VIEW IF EXISTS `sellerOrders`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `sellerOrders` AS (select `T1`.`seller_id` AS `seller_id`,`T1`.`product_id` AS `product_id`,`T1`.`quantity` AS `quantity`,`T1`.`selling_price` AS `selling_price`,`T2`.`date_` AS `date_` from (`product_order` `T1` join `payment` `T2`) where concat(`T1`.`seller_id`,'@localhost') in (select user())) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `sellerProducts`
--

/*!50001 DROP TABLE IF EXISTS `sellerProducts`*/;
/*!50001 DROP VIEW IF EXISTS `sellerProducts`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `sellerProducts` AS (select `product`.`product_id` AS `product_id`,`product`.`product_name` AS `product_name`,`product`.`price` AS `price`,`product`.`total_stock` AS `total_stock`,`product`.`pickup_address` AS `pickup_address`,`product`.`description` AS `description` from `product` where concat(`product`.`seller_id`,'@localhost') in (select user())) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `sellerProfile`
--

/*!50001 DROP TABLE IF EXISTS `sellerProfile`*/;
/*!50001 DROP VIEW IF EXISTS `sellerProfile`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `sellerProfile` AS (select `seller`.`seller_id` AS `seller_id`,`seller`.`name` AS `name`,`seller`.`address` AS `address`,`seller`.`phone_number` AS `phone_number`,`seller`.`email_id` AS `email_id`,`seller`.`rating` AS `rating` from `seller` where concat(`seller`.`seller_id`,'@localhost') in (select user())) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `shipperProfile`
--

/*!50001 DROP TABLE IF EXISTS `shipperProfile`*/;
/*!50001 DROP VIEW IF EXISTS `shipperProfile`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `shipperProfile` AS (select `shipper`.`shipper_id` AS `shipper_id`,`shipper`.`name` AS `name`,`shipper`.`head_quarters` AS `head_quarters`,`shipper`.`phone_number` AS `phone_number`,`shipper`.`email_id` AS `email_id` from `shipper` where concat(`shipper`.`shipper_id`,'@localhost') in (select user())) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `shipperTrack`
--

/*!50001 DROP TABLE IF EXISTS `shipperTrack`*/;
/*!50001 DROP VIEW IF EXISTS `shipperTrack`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `shipperTrack` AS (select `track`.`index_` AS `index_`,`product`.`pickup_address` AS `source`,`order_`.`shipping_address` AS `destination`,`track`.`tracking_id` AS `tracking_id`,`track`.`date_` AS `date_` from (((`track` join `product_order` on(`track`.`index_` = `product_order`.`ship_index`)) join `order_` on(`product_order`.`order_id` = `order_`.`order_id`)) join `product` on(`product_order`.`product_id` = `product`.`product_id` and `product_order`.`seller_id` = `product`.`seller_id`)) where concat(`track`.`shipper_id`,'@localhost') = (select user())) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `showCart`
--

/*!50001 DROP TABLE IF EXISTS `showCart`*/;
/*!50001 DROP VIEW IF EXISTS `showCart`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `showCart` AS (select `cart`.`customer_id` AS `customer_id`,`cart`.`product_id` AS `product_id`,`cart`.`seller_id` AS `seller_id`,`cart`.`quantity` AS `quantity` from `cart` where concat(`cart`.`customer_id`,'@localhost') in (select user())) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `trackID`
--

/*!50001 DROP TABLE IF EXISTS `trackID`*/;
/*!50001 DROP VIEW IF EXISTS `trackID`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `trackID` AS (select `product_order`.`order_id` AS `order_id`,`product_order`.`product_id` AS `product_id`,`product_order`.`ship_index` AS `ship_index` from `product_order` where `product_order`.`order_id` in (select `listOrders`.`order_id` from `listOrders`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-03-30  0:19:08
