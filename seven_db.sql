-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: seven_db
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `seven_products`
--

DROP TABLE IF EXISTS `seven_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seven_products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `이미지URL` varchar(500) DEFAULT NULL,
  `상품명` varchar(255) NOT NULL,
  `가격` varchar(100) DEFAULT NULL,
  `행사유형` varchar(100) DEFAULT NULL,
  `행사분류` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seven_products`
--

LOCK TABLES `seven_products` WRITE;
/*!40000 ALTER TABLE `seven_products` DISABLE KEYS */;
INSERT INTO `seven_products` VALUES (1,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','삼립)잼있는미니딸기쿠키(1입)','300','2+1',NULL),(2,'https://www.7-eleven.co.kr/upload/product/8410031/990973.1.jpg','농심)츄파춥스300','300','2+1',NULL),(3,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','삼립)잼있는미니사과쿠키(1입)','300','2+1',NULL),(4,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','미성)피니과일모양껌20g','700','2+1',NULL),(5,'https://www.7-eleven.co.kr/upload/product/8804973/131578.1.jpg','마즈)스니커즈픽앤믹스20g','700','2+1','과자'),(6,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','삼양)스틱불닭소스16g','700','1+1',NULL),(7,'https://www.7-eleven.co.kr/upload/product/8803186/200163.1.jpg','한국)몽베스트생수330ml','800','2+1','음료'),(8,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','농심)백두산백산수330펫','900','2+1',NULL),(9,'https://www.7-eleven.co.kr/upload/product/8990800/000053.1.jpg','농심)멘토스과일','900','1+1',NULL),(10,'https://www.7-eleven.co.kr/upload/product/8990800/000992.1.jpg','농심)멘토스포도','900','1+1',NULL),(11,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','딥스)춘식이해양심층수300ml','900','1+1',NULL),(12,'https://www.7-eleven.co.kr/upload/product/6921211/104292.1.jpg','농심)멘토스레인보우','900','1+1','과자'),(13,'https://www.7-eleven.co.kr/upload/product/6921211/115076.1.jpg','농심)멘토스콜라향','900','1+1','과자'),(14,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','농심)멘토스사워파인애플37.5g','900','1+1',NULL),(15,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','해태)연양갱땅콩맛55g','900','2+1',NULL),(16,'https://www.7-eleven.co.kr/upload/product/8801117/536411.1.jpg','오리온)초코파이2입','900','2+1',NULL),(17,'https://www.7-eleven.co.kr/upload/product/8809169/718205.1.jpg','풀무원)풀무원샘물','950','2+1','음료'),(18,'https://www.7-eleven.co.kr/upload/product/8801019/307096.1.jpg','해태)딸기웨하스50g','1000','2+1','과자'),(19,'https://www.7-eleven.co.kr/upload/product/8801043/022781.1.jpg','농심)백산수500ml','1000','2+1','음료'),(20,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','나무)롤팝젤리15g(후르츠믹스)','1000','2+1',NULL),(21,'https://www.7-eleven.co.kr/upload/product/8801117/070007.1.jpg','오리온)제주용암수530ml','1000','2+1','음료'),(22,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','매일)킨더트롱키18g(1입)','1000','2+1',NULL),(23,'https://www.7-eleven.co.kr/upload/product/8801111/905299.1.jpg','크라운)키커바1000(30g)','1000','2+1','과자'),(24,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','집기용)가디플러스네임펜_H','1000','2+1',NULL),(25,'https://www.7-eleven.co.kr/upload/product/8801111/930055.1.jpg','크라운)키커바 녹차1000','1000','2+1','과자'),(26,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','집기용)가디플러스보드마카_H','1000','2+1',NULL),(27,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','동원)더바삭한김5g','1000','2+1',NULL),(28,'https://www.7-eleven.co.kr/upload/product/7622201/750879.1.jpg','MZ)호올스오렌지27.9g','1000','2+1',NULL),(29,'https://www.7-eleven.co.kr/upload/product/8801019/307089.1.jpg','해태)크림웨하스50g','1000','2+1',NULL),(30,'https://www.7-eleven.co.kr/upload/product/7622201/750848.1.jpg','MZ)호올스멘토립토스27.9g','1000','2+1',NULL),(31,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','미성)XXL마시멜로우43g','1000','2+1',NULL),(32,'https://www.7-eleven.co.kr/upload/product/7622201/750824.1.jpg','MZ)호올스라임27.9g','1000','2+1',NULL),(33,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','크라운)마이쮸리치44g','1000','2+1',NULL),(34,'https://www.7-eleven.co.kr/upload/product/7622201/750794.1.jpg','MZ)호올스아이스블루27.9g','1000','2+1',NULL),(35,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','동원)동원샘물500ml','1000','1+1',NULL),(36,'https://www.7-eleven.co.kr/upload/product/7622201/750770.1.jpg','MZ)호올스허니레몬27.9g','1000','2+1',NULL),(37,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','남양)과수원사과팩190ml','1000','1+1',NULL),(38,'https://www.7-eleven.co.kr/upload/product/7622201/750718.1.jpg','MZ)호올스블루베리27.9g','1000','2+1',NULL),(39,'https://www.7-eleven.co.kr/front/img/product/product_list_01.jpg','PB)착한콘칩65g','1000','1+1',NULL),(40,'https://www.7-eleven.co.kr/upload/product/7622201/750749.1.jpg','MZ)호올스자몽27.9g','1000','2+1',NULL);
/*!40000 ALTER TABLE `seven_products` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-06 11:54:03
