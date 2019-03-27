-------------Marked "absolete" are those procedures, etc. which are not used----------

DROP DATABASE AmaKart;
CREATE DATABASE AmaKart;
USE AmaKart;

/*  Here: customer_id -> R is the only relevant dependency and hence it is in BCNF */
create table customer (
  customer_id VARCHAR (20) primary key not null,
  name VARCHAR (20) not null,
  address VARCHAR (60) not null,
  phone_number DECIMAL (10) UNSIGNED not null,
  email_id VARCHAR (20) not null
);

/*   Here: payment_id -> R is the only relevant dependency and hence it is in BCNF  */
create table payment (
  payment_id int AUTO_INCREMENT primary key not null,
  credit_card_number VARCHAR (20) not null,
  date_ timestamp,
  billing_address varchar(60) not null
);

/* Here: order_id -> R is the only relevant dependency and hence it is in BCNF  */
/* Initially payment id can be null and then later once the customer does the payment, trigger will add the payment id */
create table order_ (
  order_id int AUTO_INCREMENT primary key not null,
  customer_id VARCHAR (20),
  shipping_address varchar(60) not null,
  payment_id int,
  foreign key (customer_id) references customer (customer_id) on delete set null,
  foreign key (payment_id) references payment (payment_id) on delete set null
);

/* Here: seller_id -> R is the only relevant dependency and hence it is in BCNF */
/* Rating will be updated with the help of triggers. */
create table seller (
  seller_id varchar (20) primary key not null,
  name varchar (20) not null,
  address varchar (60) not null,
  phone_number decimal (10) UNSIGNED NOT NULL,
  email_id VARCHAR (20) not null,
  rating float
);

/*  Here: shipper_id -> R is the only relevant dependency and hence it is in BCNF  */
create table shipper (
  shipper_id varchar (20) primary key not null,
  name varchar (20) not null,
  head_quarters varchar (60) not null,
  phone_number decimal (10) UNSIGNED not null,
  email_id VARCHAR (20) not null
);

/*  Here: index_ -> R is the only relevant dependency and hence it is in BCNF  */
create table track (
  index_ INT AUTO_INCREMENT primary key not null,
  shipper_id varchar (20),
  tracking_id varchar (20),
  date_ DATE,
  foreign key (shipper_id) references shipper (shipper_id) on delete set null
);

/*  Here: (product_id, seller_id) -> R is the only relevant dependency and hence it is in BCNF  */
/* Rating will be updated with the help of triggers. */
create table product (
  product_id varchar (20) not null,
  product_name varchar (20) not null,
  product_image varchar(300),
  seller_id varchar (20) not null,
  price float not NULL,
  total_stock int,
  pickup_address varchar (60) not null,
  description varchar (60),
  rating float,
  foreign key (seller_id) references seller (seller_id) on delete cascade,
  primary key (product_id, seller_id)
);

/*  Here: (product_id, order_id, seller_id) -> R is the only relevant dependency and hence it is in BCNF  */
create table product_order (
  product_id varchar(20) not null,
  order_id int not null,
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


/*  Here: (customer_id, product_id, seller_id) -> R is the only relevant dependency and hence it is in BCNF  */
create table cart (
  customer_id varchar(20),
  product_id varchar(20),
  seller_id varchar(20),
  quantity int,
  primary key (customer_id,product_id,seller_id),
  foreign key (customer_id) references customer(customer_id) on delete cascade,
  foreign key (product_id,seller_id) references product(product_id,seller_id) on delete cascade
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
CREATE VIEW customerProfile AS (SELECT * 
                             FROM customer 
                             WHERE CONCAT(customer_id, "@localhost") IN (SELECT user()));

-- This view will allow customer to see the total cost of his/her various orders
CREATE VIEW orderPrice AS (SELECT order_id, sum(selling_price * quantity) as total_price
                           FROM (product_order)
                           GROUP BY order_id); 

-- This view will allow customer to see and add products to his cart
CREATE VIEW showCart AS (SELECT * FROM cart
                          WHERE CONCAT(customer_id, "@localhost") IN (SELECT user()));

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


-- This view will allow seller to view its details.
CREATE VIEW sellerProfile AS (SELECT * 
                             FROM seller 
                             WHERE CONCAT(seller_id, "@localhost") IN (SELECT user()));


-- Following views are absolete as we have implemented the procedure for it.
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


-- This view will allow shipper to view its details.
CREATE VIEW shipperProfile AS (SELECT * 
                             FROM shipper 
                             WHERE CONCAT(shipper_id, "@localhost") IN (SELECT user()));

-- This view will allow shipper details (pickup_address, shipping_address, tracking_id)
CREATE VIEW shipperTrack AS (SELECT index_, pickup_address AS source, shipping_address AS destination, tracking_id, date_
                              FROM (track JOIN product_order ON index_ = ship_index) NATURAL JOIN order_ NATURAL JOIN product 
                              WHERE CONCAT(shipper_id, "@localhost") = (SELECT user()));

-- #########################################
-- ###########CUSTOMER PROCEDURES###########
-- #########################################

-- Absolete
-- Procedure for customer to see his or her past purchases within a specific time duration
DELIMITER //
CREATE PROCEDURE seePurchasesBetweenDuration(IN startTime TIMESTAMP, IN endTime TIMESTAMP)
BEGIN
    select * from payment natural join order_ natural join product_order where CONCAT(order_.customer_id, "@localhost") IN (SELECT user()) AND payment.date_ BETWEEN startTime AND endTime;
END;
//
DELIMITER ;

-- Procedure for customer to see his or her cart
DELIMITER //
CREATE PROCEDURE getProductsFromCart ()
BEGIN
    select * from showCart natural join product;
END;
//
DELIMITER ;

-- Procedure for customer to checkout his cart
DELIMITER //
CREATE PROCEDURE purchaseEverythingInCart(IN oid varchar(20)) 
BEGIN
    DECLARE n int default 0;
    DECLARE i int default 0;
    DECLARE pid varchar(20);
    DECLARE sid varchar(20);
    DECLARE q int;
    DECLARE price FLOAT;
    select count(*) from showCart into n;
    SET i = 0;
    WHILE i < n DO 
      select product_id from showCart limit i,1 into pid; 
      select seller_id from showCart limit i,1 into sid; 
      select quantity from showCart limit i,1 into q; 
      IF (q > all (SELECT total_stock from product where product_id = pid and seller_id = sid)) THEN
          SELECT total_stock from product where product_id = pid and seller_id = sid into q;
      END IF;
      select price from product where product_id = pid and seller_id = sid into price;
      INSERT INTO product_order(product_id,order_id,seller_id,quantity,selling_price) VALUES (pid,oid,sid,q,price);
      SET i = i + 1;
    END WHILE;
    SET i = 0;
    WHILE i < n DO
      DELETE from showCart where product_id = pid and seller_id = sid;
      SET i = i + 1;
    END WHILE;
END;
//
DELIMITER ;

-- Procedure for customer to remove a product in cart 
DELIMITER //
CREATE PROCEDURE removeProductCart(IN pid varchar(20), IN sid varchar(20))
BEGIN
    delete from showCart where product_id = pid and seller_id = sid;
END;
//
DELIMITER ;

-- Procedure for customer to update a product in cart 
DELIMITER //
CREATE PROCEDURE updateProductCart(IN pid varchar(20), IN sid varchar(20), IN N INT)
BEGIN
    UPDATE showCart set quantity = N where product_id = pid and seller_id = sid;
END;
//
DELIMITER ;

-- Procedure for customer to makeorder
DELIMITER //
CREATE PROCEDURE makeorder(IN cnum varchar(20), IN badd varchar(20), IN cid varchar(20), IN sadd varchar(20))
BEGIN
    DECLARE curr_time TIMESTAMP;
    DECLARE payid INT;
    DECLARE oid INT;
    set curr_time = NOW();
    INSERT INTO payment(credit_card_number,date_,billing_address) values (cnum,curr_time,badd);
    SELECT payment_id from payment where credit_card_number = cnum and date_ = curr_time and billing_address = badd order by payment_id desc into payid;
    INSERT INTO order_ (customer_id,payment_id,shipping_address) VALUES (cid,payid,sadd);
    SELECT order_id from order_ where customer_id = cid and payment_id = payid and shipping_address = sadd order by order_id desc into oid;
    call purchaseEverythingInCart(oid);
END;
//
DELIMITER ;

-- Procedure to add product to cart.
DELIMITER //
CREATE PROCEDURE addProductToCart(IN cid varchar(20),IN pid varchar(20),IN sid varchar(20),IN q int)
BEGIN
    IF ((SELECT count(*) from showCart where product_id = pid and seller_id = sid) = 1) THEN
      UPDATE showCart set quantity = q where product_id = pid and seller_id = sid; 
    ELSE
      INSERT INTO showCart VALUES (cid,pid,sid,q);
    END IF;
END;
//
DELIMITER ;

-- Procedure to see latest N Purchases
DELIMITER //
CREATE PROCEDURE seeLatestNPurchases(IN N INT)
BEGIN
    select * from payment natural join order_ natural join product_order natural join product join track on (product_order.ship_index = track.index_) where CONCAT(order_.customer_id, "@localhost") IN (SELECT user()) ORDER BY payment.date_ DESC LIMIT N;
END;
//
DELIMITER ;

-- Procedure to see Purchases between dates
DELIMITER //
CREATE PROCEDURE seePurchasesByDate(IN startTime TIMESTAMP, IN endTime TIMESTAMP)
BEGIN
    select * from payment natural join order_ natural join product_order natural join product join track on (product_order.ship_index = track.index_) where CONCAT(order_.customer_id, "@localhost") IN (SELECT user()) and payment.date_ BETWEEN startTime AND endTime;
END;
//
DELIMITER ;

-- Procedure to see products within price range
DELIMITER //
CREATE PROCEDURE queryProductsTim(IN productName varchar(20), IN lowRange FLOAT, IN highRange FLOAT)
BEGIN
    select * from product where product_name like CONCAT('%', productName, '%') AND price BETWEEN lowRange AND highRange ORDER BY price ASC;
END;
//
DELIMITER ;

-- Procedure to see reviews of a product
DELIMITER //
CREATE PROCEDURE ProductReviews(IN pid varchar(20), IN sid varchar(20))
BEGIN
    SELECT name, product_rating, product_review, seller_rating, seller_review FROM (product_order natural join order_ natural join customer natural join payment) WHERE product_id = pid AND seller_id = sid;
END;
//
DELIMITER ;

-- Procedure to add review for a product
DELIMITER //
CREATE PROCEDURE addReviewProduct(IN pid varchar(20), IN oid varchar(20), IN sid varchar(20), IN rev varchar(60))
BEGIN
    UPDATE product_order SET product_review = rev WHERE product_id = pid and order_id = oid and seller_id = sid;
END;
//
DELIMITER ;

-- Procedure to add review for a seller 
DELIMITER //
CREATE PROCEDURE addReviewSeller(IN pid varchar(20), IN oid varchar(20), IN sid varchar(20), IN rev varchar(60))
BEGIN
    UPDATE product_order SET seller_review = rev WHERE product_id = pid and order_id = oid and seller_id = sid;
END;
//
DELIMITER ;

-- Procedure to see products sorted by rating
DELIMITER //
CREATE PROCEDURE queryProductsRat(IN productName varchar(20))
BEGIN
    select * from product where product_name like CONCAT('%', productName, '%') ORDER BY rating DESC;
END;
//
DELIMITER ;

-- Procedure to add rating for product
DELIMITER //
CREATE PROCEDURE addRatingProduct(IN pid varchar(20), IN oid varchar(20), IN sid varchar(20), IN rating INT)
BEGIN
    IF (rating IN (1,2,3,4,5)) THEN
      UPDATE product_order SET product_rating =  rating WHERE product_id = pid and order_id = oid and seller_id = sid;
    END IF;
END;
//
DELIMITER ;

-- Procedure to add rating for seller
DELIMITER //
CREATE PROCEDURE addRatingSeller(IN pid varchar(20), IN oid varchar(20), IN sid varchar(20), IN rating INT)
BEGIN
    IF (rating IN (1,2,3,4,5)) THEN
      UPDATE product_order SET seller_rating = rating WHERE product_id = pid and order_id = oid and seller_id = sid;
    END IF;
END;
//
DELIMITER ;


-- Procedure to update customer info
DELIMITER //
CREATE PROCEDURE custUpdateInfo(IN customer_id varchar(20), IN passwordd VARCHAR(20), IN named varchar(20), IN addressd VARCHAR(60), IN phone_number DECIMAL(10) UNSIGNED, IN email_id VARCHAR(20))
BEGIN
    IF (CHAR_LENGTH(passwordd) > 0) THEN
      UPDATE Users SET Users.passcode = passwordd WHERE Users.username = customer_id;
    END IF;
    IF (CHAR_LENGTH(named) > 0) THEN
      UPDATE customer SET customer.name = named WHERE customer.customer_id = customer_id;
    END IF;
    IF (CHAR_LENGTH(addressd) > 0) THEN
      UPDATE customer SET customer.address = addressd WHERE customer.customer_id = customer_id;
    END IF;
    IF (phone_number <> 0) THEN
      UPDATE customer SET customer.phone_number = phone_number WHERE customer.customer_id = customer_id;
    END IF;
    IF (CHAR_LENGTH(email_id) > 0) THEN
      UPDATE customer SET customer.email_id = email_id WHERE customer.customer_id = customer_id;
    END IF;
END;
//
DELIMITER ;

-- #########################################
-- ###########SELLER PROCEDURES#############
-- #########################################


-- Procedure for seller to see sold but not shipped products

DELIMITER //
CREATE PROCEDURE soldButNotShipped(IN seller_id varchar(20))
BEGIN
  select product_order.* from product_order join track on product_order.ship_index = track.index_ where shipper_id is NULL;
  -- select * from product_order where product_order.seller_id = seller_id and ship_index is NULL;
END;
//
DELIMITER ;

-- Procedure for seller to ship a sold product
DELIMITER //
CREATE PROCEDURE shipSoldProduct(IN gproduct_id varchar(20), IN gorder_id varchar(20), IN gseller_id varchar(20), IN gshipper_id varchar(20), IN gtracking_id varchar(20), IN gdate DATE)
BEGIN
  set @c = (select ship_index from product_order where seller_id = gseller_id and product_id = gproduct_id and order_id = gorder_id); 
  update track set shipper_id = gshipper_id, tracking_id = gtracking_id, date_ = (select NOW()) where index_ = @c;
END;
//
DELIMITER ;



-- Procedure for seller to see his rating
DELIMITER //
CREATE PROCEDURE getRating(IN seller_id varchar(20))
BEGIN
  select COALESCE(rating, 0) from seller where seller.seller_id = seller_id;
END;
//
DELIMITER ;


-- Procedure for seller to check whether there is already a product with given seller_id and product_id
DELIMITER //
CREATE PROCEDURE sellerCheckExistProd(IN product_id varchar(20), IN seller_id varchar(20))
BEGIN
  select * from product where product.product_id = product_id and product.seller_id = seller_id;
END;
//
DELIMITER ;

-- Procedure for seller to add new product
DELIMITER //
CREATE PROCEDURE addProduct(IN product_id varchar(20), IN seller_id varchar(20), IN product_name varchar(20), IN product_image varchar(300), IN price float, IN total_stock int, IN pickup_address varchar(60), IN description varchar(60))
BEGIN
  insert into product(product_id, product_name, product_image, seller_id, price, total_stock, pickup_address, description) values (product_id, product_name, product_image, seller_id, price, total_stock, pickup_address, description);
END;
//
DELIMITER ;


-- Procedure for seller to update his specific product details.
DELIMITER //
CREATE PROCEDURE updateProductInfo(IN product_id varchar(20), IN seller_id varchar(20), IN product_name varchar(20), IN product_image varchar(300), IN price float, IN total_stock int, IN pickup_address varchar(60), IN description varchar(60))
BEGIN
  IF (CHAR_LENGTH(product_name) > 0) THEN
    UPDATE product SET product.product_name = product_name where product.product_id = product_id and product.seller_id = seller_id;
  END IF;
  IF (CHAR_LENGTH(product_image) > 0) THEN
    UPDATE product SET product.product_image = product_image where product.product_id = product_id and product.seller_id = seller_id;
  END IF;
  IF (price > 0.1) THEN
    UPDATE product SET product.price = price where product.product_id = product_id and product.seller_id = seller_id;
  END IF;
  IF (CHAR_LENGTH(pickup_address) > 0) THEN
    UPDATE product SET product.pickup_address = pickup_address where product.product_id = product_id and product.seller_id = seller_id;
  END IF;
  IF (CHAR_LENGTH(description) > 0) THEN
    UPDATE product SET product.description = description where product.product_id = product_id and product.seller_id = seller_id;
  END IF;
END;
//
DELIMITER ;


-- Procedure to update seller's info
DELIMITER //
CREATE PROCEDURE sellerUpdateInfo(IN seller_id varchar(20), IN passwordd VARCHAR(20), IN named varchar(20), IN addressd VARCHAR(60), IN phone_number DECIMAL(10) UNSIGNED, IN email_id VARCHAR(20))
BEGIN
    IF (CHAR_LENGTH(passwordd) > 0) THEN
      UPDATE Users SET Users.passcode = passwordd WHERE Users.username = seller_id;
    END IF;
    IF (CHAR_LENGTH(named) > 0) THEN
      UPDATE seller SET seller.name = named WHERE seller.seller_id = seller_id;
    END IF;
    IF (CHAR_LENGTH(addressd) > 0) THEN
      UPDATE seller SET seller.address = addressd WHERE seller.seller_id = seller_id;
    END IF;
    IF (phone_number <> 0) THEN
      UPDATE seller SET seller.phone_number = phone_number WHERE seller.seller_id = seller_id;
    END IF;
    IF (CHAR_LENGTH(email_id) > 0) THEN
      UPDATE seller SET seller.email_id = email_id WHERE seller.seller_id = seller_id;
    END IF;
END;
//
DELIMITER ;

-- Procedure for seller to see his or her past sold products within a specific time duration
DELIMITER //
CREATE PROCEDURE seeSellingsBetweenDuration(IN startTime TIMESTAMP, IN endTime TIMESTAMP)
BEGIN
    select product_order.* from payment natural join order_ natural join product_order where CONCAT(product_order.seller_id, "@localhost") IN (SELECT user()) AND payment.date_ BETWEEN startTime AND endTime;
END;
//
DELIMITER ;

-- Procedure to see latest N Sellings
DELIMITER //
CREATE PROCEDURE seeLatestNSellings(IN N INT)
BEGIN
    select product_order.* from payment natural join order_ natural join product_order where CONCAT(product_order.seller_id, "@localhost") IN (SELECT user()) ORDER BY payment.date_ DESC LIMIT N;
END;
//
DELIMITER ;

-- Procedure to see similary products with increasing price
DELIMITER //
CREATE PROCEDURE selQuerySimProducts(IN productName varchar(20))
BEGIN
    select * from product where product_name like CONCAT('%', productName, '%') AND CONCAT(seller_id, "@localhost") IN (SELECT user()) ORDER BY price ASC;
END;
//
DELIMITER ;

-- Procedure to see similar products sorted by rating
DELIMITER //
CREATE PROCEDURE selQueryProductsRat(IN productName varchar(20))
BEGIN
    select * from product where product_name like CONCAT('%', productName, '%') AND CONCAT(seller_id, "@localhost") IN (SELECT user()) ORDER BY rating DESC;
END;
//
DELIMITER ;

-- #########################################
-- ###########SHIPPER PROCEDURES############
-- #########################################



-- Procedure to update shipper's info
DELIMITER //
CREATE PROCEDURE shipperUpdateInfo(IN shipper_id varchar(20), IN passwordd VARCHAR(20), IN named varchar(20), IN addressd VARCHAR(60), IN phone_number DECIMAL(10) UNSIGNED, IN email_id VARCHAR(20))
BEGIN
    IF (CHAR_LENGTH(passwordd) > 0) THEN
      UPDATE Users SET Users.passcode = passwordd WHERE Users.username = shipper_id;
    END IF;
    IF (CHAR_LENGTH(named) > 0) THEN
      UPDATE shipper SET shipper.name = named WHERE shipper.shipper_id = shipper_id;
    END IF;
    IF (CHAR_LENGTH(addressd) > 0) THEN
      UPDATE shipper SET shipper.head_quarters = addressd WHERE shipper.shipper_id = shipper_id;
    END IF;
    IF (phone_number <> 0) THEN
      UPDATE shipper SET shipper.phone_number = phone_number WHERE shipper.shipper_id = shipper_id;
    END IF;
    IF (CHAR_LENGTH(email_id) > 0) THEN
      UPDATE shipper SET shipper.email_id = email_id WHERE shipper.shipper_id = shipper_id;
    END IF;
END;
//
DELIMITER ;

-- Procedure for shipper to see his or her past shipments within a specific time duration
DELIMITER //
CREATE PROCEDURE seeShipmentsBetweenDuration(IN startTime DATE, IN endTime DATE)
BEGIN
    select * from track where CONCAT(shipper_id, "@localhost") IN (SELECT user()) AND date_ BETWEEN startTime AND endTime;
END;
//
DELIMITER ;

-- Procedure to see latest N Shipments
DELIMITER //
CREATE PROCEDURE seeLatestNShipments(IN N INT)
BEGIN
    select * from track where CONCAT(shipper_id, "@localhost") IN (SELECT user()) ORDER BY date_ DESC LIMIT N;
END;
//
DELIMITER ;

-- #########################################
-- ################FUNCTIONS################
-- #########################################

-- Function to return the total earning of a seller between supplied dates
DELIMITER //
CREATE FUNCTION sellerStatsBetweenDate(startTime TIMESTAMP, endTime TIMESTAMP)
RETURNS FLOAT DETERMINISTIC  
BEGIN
    DECLARE temp FLOAT;
    SELECT SUM(quantity*selling_price) INTO temp FROM product_order natural join order_ natural join payment WHERE date_ BETWEEN startTime and endTime;
    RETURN temp;
END;
//
DELIMITER ;

-- Make sure that any view on which a role gets access on should have the filter "SELECT user()"
GRANT ALL PRIVILEGES ON AmaKart.customerProfile TO customer;
GRANT ALL PRIVILEGES ON AmaKart.showCart TO customer;
GRANT SELECT ON AmaKart.previousOrders TO customer;
GRANT SELECT ON AmaKart.listOrders TO customer;
GRANT SELECT ON AmaKart.packageStatus TO customer;

-- I am not sure about these two please check
-- GRANT INSERT ON AmaKart.order_ TO customer;
-- GRANT INSERT ON AmaKart.payment TO customer;

GRANT SELECT ON AmaKart.sellerProfile TO seller;
GRANT SELECT ON AmaKart.sellerProducts TO seller;
GRANT SELECT ON AmaKart.sellerOrders TO seller;
GRANT SELECT ON AmaKart.shipper to seller;

GRANT SELECT ON AmaKart.shipperProfile TO shipper;
GRANT SELECT ON AmaKart.shipperTrack TO shipper;

-- Procedures/Functions Grant
GRANT EXECUTE ON PROCEDURE AmaKart.seePurchasesBetweenDuration TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.getProductsfromCart TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.seeLatestNPurchases TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.queryProductsTim TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.queryProductsRat TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.makeorder TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.purchaseEverythingInCart TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.addProductToCart TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.custUpdateInfo TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.ProductReviews TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.addReviewProduct TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.addReviewSeller TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.addRatingProduct TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.addRatingSeller TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.seePurchasesByDate TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.updateProductCart TO customer;
GRANT EXECUTE ON PROCEDURE AmaKart.removeProductCart TO customer;


GRANT EXECUTE ON PROCEDURE AmaKart.soldButNotShipped TO seller;
GRANT EXECUTE ON PROCEDURE AmaKart.shipSoldProduct TO seller;
GRANT EXECUTE ON PROCEDURE AmaKart.getRating TO seller;
GRANT EXECUTE ON PROCEDURE AmaKart.sellerCheckExistProd TO seller;
GRANT EXECUTE ON PROCEDURE AmaKart.addProduct TO seller;
GRANT EXECUTE ON PROCEDURE AmaKart.sellerUpdateInfo TO seller;
GRANT EXECUTE ON PROCEDURE AmaKart.selQuerySimProducts TO seller;
GRANT EXECUTE ON PROCEDURE AmaKart.selQueryProductsRat TO seller;
GRANT EXECUTE ON PROCEDURE AmaKart.seeSellingsBetweenDuration TO seller;
GRANT EXECUTE ON PROCEDURE AmaKart.seeLatestNSellings TO seller;
GRANT EXECUTE ON PROCEDURE AmaKart.updateProductInfo TO seller;

GRANT EXECUTE ON PROCEDURE AmaKart.shipperUpdateInfo TO shipper;
GRANT EXECUTE ON PROCEDURE AmaKart.seeShipmentsBetweenDuration TO shipper;
GRANT EXECUTE ON PROCEDURE AmaKart.seeLatestNShipments TO shipper;


GRANT EXECUTE ON FUNCTION AmaKart.sellerStatsBetweenDate TO seller;

--#######################################
--#########TRIGGERS BEGIN################
--#######################################
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
  UPDATE product SET rating = (SELECT (AVG(product_rating)) FROM product_order WHERE product_id = NEW.product_id) WHERE product_id = NEW.product_id;
END//
DELIMITER ;


-- When a customer passes a rating for seller we have to update it in our seller table
DELIMITER //
CREATE TRIGGER updateRatingSeller AFTER UPDATE on product_order
FOR EACH ROW BEGIN
  UPDATE seller SET rating = (SELECT (AVG(seller_rating)) FROM product_order WHERE seller_id = NEW.seller_id) WHERE seller_id = NEW.seller_id;
END//
DELIMITER ;

-- When a product is sold, reduce the amount of the product avaliable and add an entry to our track table for the same
DELIMITER //
CREATE TRIGGER stockCheckandaddTrack BEFORE INSERT on product_order
FOR EACH ROW BEGIN
  UPDATE product set total_stock = total_stock - NEW.quantity WHERE product_id = NEW.product_id and seller_id = NEW.seller_id;
  INSERT INTO track () Values ();
  SET NEW.ship_index = (SELECT MAX(index_) FROM track);
END//
DELIMITER ;

-- To check whether the product added in cart are valid or not
DELIMITER //
CREATE TRIGGER validCartinsert BEFORE INSERT on cart
FOR EACH ROW BEGIN
    IF (NEW.quantity > all(SELECT total_stock FROM product WHERE product.product_id = NEW.product_id AND product.seller_id = NEW.seller_id)) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Not possible';
    END IF;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER validCartupdate BEFORE UPDATE on cart
FOR EACH ROW BEGIN
    IF (NEW.quantity > all(SELECT total_stock FROM product WHERE product.product_id = NEW.product_id AND product.seller_id = NEW.seller_id)) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Not possible';
    END IF;
END//
DELIMITER ;

-- -- When a product is shipped update its shipping date_
-- DELIMITER //
-- CREATE TRIGGER trackupdateshipdate AFTER INSERT on track 
-- FOR EACH ROW BEGIN
--   UPDATE track SET date_ = (select NOW()) WHERE index_ = NEW.index_;
-- END//
-- DELIMITER ;

--#######################################
--#########TRIGGERS END##################
--#######################################

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

INSERT INTO product Values ("1","Rasgulla", 'https://i.ndtvimg.com/i/2017-10/rasgulla-recipe_620x330_51508133855.jpg?downsize=650:400&output-quality=70&output-format=webp', "Sourabh",10,100.0,"RM3xx","Rasgulla from Aggarwal Sweets", NULL);
INSERT INTO product Values ("2","Gulab Jamun", 'http://www.manjulaskitchen.com/blog/wp-content/uploads/gulab_jamun1.jpg', "Sourabh",100,100.0,"RM3xx","Gulab Jamun from Aggarwal Sweets", NULL);

INSERT INTO payment Values ("1","4362536563578",'2019-01-01',"CompLabFF");

INSERT INTO order_ Values ("1","Nikhil","RM-119","1");

-- INSERT INTO track(shipper_id) Values ("FEDEx");

INSERT INTO product_order(product_id, order_id, seller_id, product_rating, seller_rating, ship_index, product_review, seller_review, quantity, selling_price) Values ("1","1","Sourabh",5,4,1,NULL,NULL,10, 10);

UPDATE track set shipper_id = "FEDEx", date_ = (select NOW()), tracking_id = "EPIN290348AD7" where index_ = 1;

INSERT INTO cart Values ("Nikhil","1","Sourabh","2");
