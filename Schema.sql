DROP DATABASE AmaKart;
CREATE DATABASE AmaKart;
USE AmaKart;

/*  Here: customer_id -> R is the only non trivial dependency and hence it is in BCNF */
create table customer (
  customer_id VARCHAR (20) primary key not null,
  name VARCHAR (20) not null,
  address VARCHAR (60) not null,
  phone_number DECIMAL (10) UNSIGNED not null,
  email_id VARCHAR (20) not null
);

/*   Here: payment_id -> R is the only non trivial dependency and hence it is in BCNF  */
create table payment (
  payment_id VARCHAR (20) primary key not null,
  credit_card_number VARCHAR (20) not null,
  date_ timestamp,
  billing_address varchar(60) not null
);

/* Here: order_id -> R is the only non trivial dependency and hence it is in BCNF  */
/* Initially payment id can be null and then later once the customer does the payment, trigger will add the payment id */
create table order_ (
  order_id VARCHAR (20) primary key not null,
  customer_id VARCHAR (20),
  shipping_address varchar(60) not null,
  payment_id VARCHAR (20),
  foreign key (customer_id) references customer (customer_id) on delete set null,
  foreign key (payment_id) references payment (payment_id) on delete set null
);

/* Here: seller_id -> R is the only non trivial dependency and hence it is in BCNF */
/* Rating will be updated with the help of triggers. */
create table seller (
  seller_id varchar (20) primary key not null,
  name varchar (20) not null,
  address varchar (60) not null,
  phone_number decimal (10) UNSIGNED NOT NULL,
  email_id VARCHAR (20) not null,
  rating float
);

/*  Here: shipper_id -> R is the only non trivial dependency and hence it is in BCNF  */
create table shipper (
  shipper_id varchar (20) primary key not null,
  name varchar (20) not null,
  head_quarters varchar (60) not null,
  phone_number decimal (10) UNSIGNED not null,
  email_id VARCHAR (20) not null
);

/*  Here: index_ -> R is the only non trivial dependency and hence it is in BCNF  */
create table track (
  index_ INT AUTO_INCREMENT primary key not null,
  shipper_id varchar (20),
  tracking_id varchar (20),
  foreign key (shipper_id) references shipper (shipper_id) on delete set null
);

/*  Here: (product_id, seller_id) -> R is the only non trivial dependency and hence it is in BCNF  */
/* Rating will be updated with the help of triggers. */
create table product (
  product_id varchar (20) not null,
  product_name varchar (20) not null,
  seller_id varchar (20) not null,
  price float not NULL,
  total_stock int,
  pickup_address varchar (60) not null,
  description varchar (60),
  rating float,
  foreign key (seller_id) references seller (seller_id) on delete cascade,
  primary key (product_id, seller_id)
);

/*  Here: (product_id, order_id, seller_id) -> R is the only non trivial dependency and hence it is in BCNF  */
create table product_order (
  product_id varchar(20) not null,
  order_id varchar (20) not null,
  seller_id varchar (20),
  product_rating int check (product_rating in (NULL, 1, 2, 3, 4, 5)),
  seller_rating int check (seller_rating in (NULL, 1, 2, 3, 4, 5)),
  ship_index int,
  product_review varchar (60),
  seller_review varchar (60),
  quantity int,
  selling_price float,
  primary key (product_id, order_id, seller_id),
  foreign key (product_id) references product (product_id) on delete cascade,
  foreign key (order_id) references order_ (order_id) on delete cascade,
  foreign key (seller_id) references seller (seller_id) on delete cascade,
  foreign key (ship_index) references track (index_) on delete set null
);


-- We also have an auxiliary table for keeping track of users with their old passwords as mysql.user encrypts the passwords and there is no way to get it back also this table is required for validation when the user tries to log in the system.
-- Clearly this table is in BCNF.

create table Users (
  username VARCHAR (20) primary key not null,
  passcode VARCHAR (20) not null,
  roles VARCHAR (20) not null
);

-- #########################################
-- ###########CUSTOMER VIEWS################
-- #########################################

-- This view will allow customer to view its details.

CREATE VIEW customer_add AS (SELECT * 
                             FROM customer 
                             WHERE CONCAT(customer_id, "@localhost") IN (SELECT user()));

-- This view will allow customer to see the total cost of his/her various orders

CREATE VIEW orderPrice AS (SELECT order_id, sum(selling_price * quantity) as total_price
                           FROM (product_order)
                           GROUP BY order_id); 

-- This view will tell the customer details corresponding to his/her all order_id mentioning complete order details (order_id, shipping_address, date_, total_price) except the products in that order. 

CREATE VIEW previousOrders AS (SELECT T1.order_id, T1.shipping_address, T2.date_, T3.total_price
                               FROM (order_ as T1) NATURAL JOIN (payment as T2) NATURAL JOIN (orderPrice as T3)
                               WHERE CONCAT(T1.customer_id, "@localhost") IN (SELECT user()));

-- This view will allow customer to just see his various order_id. 

CREATE VIEW listOrders AS (SELECT order_id
                            FROM order_ 
                            WHERE CONCAT(customer_id, "@localhost") IN (SELECT user()));

-- This view will give entry to the track table for each (product_id, order_id) pair

CREATE VIEW trackID AS (SELECT order_id, product_id, ship_index
                        FROM product_order
                        WHERE order_id IN (SELECT * FROM listOrders));

-- This view will augment the previous view with tracking_id as well.

CREATE VIEW packageStatus AS (SELECT T1.order_id, T1.product_id, T1.ship_index, T2.tracking_id
                              FROM (trackID as T1) JOIN (track as T2) ON (T1.ship_index = T2.index_));


-- #########################################
-- ###########SELLER VIEWS##################
-- #########################################

-- This view will allow seller to see his/her various products.

CREATE VIEW sellerProducts AS (SELECT product_id, product_name, price, total_stock, pickup_address, description 
                                  FROM product
                                  WHERE CONCAT(seller_id, "@localhost") in (SELECT user()));

-- This view allow seller to see various orders which he or she have sold (seller_id, product_id, quantity, selling_price, date_) 

CREATE VIEW sellerOrders AS (SELECT T1.seller_id, T1.product_id, T1.quantity, T1.selling_price, T2.date_
                                FROM (product_order as T1) natural join (payment as T2)
                                WHERE CONCAT(T1.seller_id, "@localhost") in (SELECT user()));

-- #########################################
-- ###########SHIPPER VIEWS#################
-- #########################################

-- This view will allow shipper details (pickup_address, shipping_address, tracking_id)

CREATE VIEW shipperTrack AS (SELECT index_, pickup_address AS source, shipping_address AS destination, tracking_id
                              FROM (track JOIN product_order ON index_ = ship_index) NATURAL JOIN order_ NATURAL JOIN product 
                              WHERE CONCAT(shipper_id, "@localhost") = (SELECT user()));

-- #########################################
-- ###########CUSTOMER PROCEDURES###########
-- #########################################

-- Procedure for customer to see his or her past purchases within a specific time duration

DELIMITER //
CREATE PROCEDURE seePurchasesBetweenDuration(IN startTime TIMESTAMP, IN endTime TIMESTAMP)
BEGIN
    select * from payment natural join order_ natural join product_order where CONCAT(order_.customer_id, "@localhost") IN (SELECT user()) AND payment.date_ BETWEEN startTime AND endTime;
END;
//
DELIMITER ;

-- Procedure to see latest N Purchases

DELIMITER //
CREATE PROCEDURE seeLatestNPurchases(IN N INT)
BEGIN
    select * from payment natural join order_ natural join product_order where CONCAT(order_.customer_id, "@localhost") IN (SELECT user()) ORDER BY payment.date_ DESC LIMIT N;
END;
//
DELIMITER ;

-- Procedure to see products within price range

DELIMITER //
CREATE PROCEDURE queryProducts(IN lowRange FLOAT, IN highRange FLOAT)
BEGIN
    select * from product where price BETWEEN lowRange AND highRange ORDER BY price ASC;
END;
//
DELIMITER ;

-- Procedure to see reviews of a product withing a duration
DELIMITER //
CREATE PROCEDURE recentProductReviewsBetweenDuration(IN pid varchar(20), IN sid varchar(20), IN startTime TIMESTAMP, IN endTime TIMESTAMP)
BEGIN
    SELECT name, product_review FROM (product_order natural join order_ natural join customer natural join payment) WHERE product_id = pid AND seller_id = sid AND (payment.date_ BETWEEN startTime AND endTime);
END;
//
DELIMITER ;

-- Procedure to add review for a product
DELIMITER //
CREATE PROCEDURE addReviewProduct(IN pid varchar(20), IN oid varchar(20), IN rev varchar(60))
BEGIN
    UPDATE product_order SET product_review = rev WHERE product_id = pid and order_id = oid;
END;
//
DELIMITER ;

-- Procedure to add review for a seller 
DELIMITER //
CREATE PROCEDURE addReviewSeller(IN pid varchar(20), IN oid varchar(20), IN rev varchar(60))
BEGIN
    UPDATE product_order SET seller_review = rev WHERE product_id = pid and order_id = oid;
END;
//
DELIMITER ;

-- Procedure to add rating for product
DELIMITER //
CREATE PROCEDURE addRatingProduct(IN pid varchar(20), IN oid varchar(20), IN rating INT)
BEGIN
    IF (rating IN (1,2,3,4,5)) THEN
      UPDATE product_order SET product_rating =  rating WHERE product_id = pid and order_id = oid;
    END IF;
END;
//
DELIMITER ;

-- Procedure to add rating for seller
DELIMITER //
CREATE PROCEDURE addRatingSeller(IN pid varchar(20), IN oid varchar(20), IN rating INT)
BEGIN
    IF (rating IN (1,2,3,4,5)) THEN
      UPDATE product_order SET seller_rating = rating WHERE product_id = pid and order_id = oid;
    END IF;
END;
//
DELIMITER ;

DROP ROLE dbadmin;
DROP ROLE customer;
DROP ROLE seller;
DROP ROLE shipper;

CREATE ROLE dbadmin;
CREATE ROLE customer;
CREATE ROLE seller;
CREATE ROLE shipper;

GRANT ALL PRIVILEGES ON AmaKart.* TO dbadmin;

-- Make sure that any view on which a role gets access on should have the filter "SELECT user()"
GRANT ALL PRIVILEGES ON AmaKart.customer_add TO customer;
GRANT SELECT ON AmaKart.previousOrders TO customer;
GRANT SELECT ON AmaKart.listOrders TO customer;
GRANT SELECT ON AmaKart.packageStatus TO customer;

-- I am not sure about these two please check
-- GRANT INSERT ON AmaKart.order_ TO customer;
-- GRANT INSERT ON AmaKart.payment TO customer;

GRANT SELECT ON AmaKart.sellerProducts TO seller;
GRANT SELECT ON AmaKart.sellerOrders TO seller;

GRANT SELECT ON AmaKart.shipperTrack TO shipper;

-- Procedures/Functions Grant
GRANT EXECUTE ON PROCEDURE AmaKart.seePurchasesBetweenDuration TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.seeLatestNPurchases TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.queryProducts TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.recentProductReviewsBetweenDuration TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.addReviewProduct TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.addReviewSeller TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.addRatingProduct TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.addRatingSeller TO customer;

-- When a product is sold, we want to mention its selling_price as later the seller can update the price

DELIMITER //
CREATE TRIGGER setPrice BEFORE INSERT on product_order
FOR EACH ROW BEGIN
  SET NEW.selling_price = (SELECT price FROM product WHERE product_id = NEW.product_id and seller_id = NEW.seller_id);
END//
DELIMITER ;

-- When a customer passes a rating for product we have to update it in our product table

DELIMITER //
CREATE TRIGGER updateRatingProduct AFTER UPDATE on product_order
FOR EACH ROW BEGIN
  IF NEW.product_rating != NULL THEN
    UPDATE product SET rating = (SELECT AVG(product_rating) FROM product_order WHERE product_id = NEW.product_id) WHERE product_id = NEW.product_id;
  END IF;
END//
DELIMITER ;


-- When a customer passes a rating for seller we have to update it in our seller table

DELIMITER //
CREATE TRIGGER updateRatingSeller AFTER UPDATE on product_order
FOR EACH ROW BEGIN
  IF NEW.seller_rating != NULL THEN
    UPDATE seller SET rating = (SELECT AVG(seller_rating) FROM product_order WHERE seller_id = NEW.seller_id) WHERE seller_id = NEW.seller_id;
  END IF;
END//
DELIMITER ;

-- When a product is sold, we need to add an entry to our track table for the same

DELIMITER //
CREATE TRIGGER addTrack BEFORE INSERT on product_order
FOR EACH ROW BEGIN
  INSERT INTO track () Values ();
  SET NEW.ship_index = (SELECT MAX (index_) FROM track);
END//
DELIMITER ;

-- Inserting data and creating dummy users without password
DROP USER Nikhil;
DROP USER Sourabh;
DROP USER FEDEx;

CREATE USER Nikhil IDENTIFIED BY "hi";
CREATE USER Sourabh IDENTIFIED BY "hi";
CREATE USER FEDEx IDENTIFIED BY "hi";


GRANT customer to Nikhil;
GRANT seller to Sourabh;
GRANT shipper to FEDEx;

INSERT INTO Users VALUES ("Nikhil", "hi", "customer");
INSERT INTO Users VALUES ("Sourabh", "hi", "seller");
INSERT INTO Users VALUES ("FEDEx", "hi", "shipper");

INSERT INTO customer Values ("Nikhil","Nikhil Kumar","ROOM-119",8281112705,"111601013@");
INSERT INTO seller Values ("Sourabh","Sourabh Agg","ROOM-211",8281112700,"111601025@",NULL);
INSERT INTO shipper Values ("FEDEx","FEDEx","Delhi",1800123343,"111601020@");

INSERT INTO product Values ("1","Rasgulla","Sourabh",10,100.0,"RM3xx","Rasgulla from Aggarwal Sweets",NULL);

INSERT INTO payment Values ("1","4362536563578",'2019-01-01',"CompLabFF");

INSERT INTO order_ Values ("1","Nikhil","RM-119","1");

INSERT INTO track(shipper_id) Values ("FEDEx");

INSERT INTO product_order(product_id, order_id, seller_id, product_rating, seller_rating, ship_index, product_review, seller_review, quantity) Values ("1","1","Sourabh",5,4,1,NULL,NULL,10);
