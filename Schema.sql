/* Notation: A dependency A -> B is called relevant dependency if all other dependencies are of the form A -> C where C is a subset of B */

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
  payment_id VARCHAR (20) primary key not null,
  credit_card_number VARCHAR (20) not null,
  date_ timestamp,
  billing_address varchar(60) not null
);

/* Here: order_id -> R is the only relevant dependency and hence it is in BCNF  */
/* Initially payment id can be null and then later once the customer does the payment, trigger will add the payment id */
create table order_ (
  order_id VARCHAR (20) primary key not null,
  customer_id VARCHAR (20),
  shipping_address varchar(60) not null,
  payment_id VARCHAR (20),
  foreign key (customer_id) references customer (customer_id) on delete set null,
  foreign key (payment_id) references payment (payment_id) on delete set null
);

/* Here: supplier_id -> R is the only relevant dependency and hence it is in BCNF */
/* Rating will be updated with the help of triggers. */
create table supplier (
  supplier_id varchar (20) primary key not null,
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
  foreign key (shipper_id) references shipper (shipper_id) on delete set null
);

/*  Here: (product_id, supplier_id) -> R is the only relevant dependency and hence it is in BCNF  */
/* Rating will be updated with the help of triggers. */
create table product (
  product_id varchar (20) not null,
  product_name varchar (20) not null,
  supplier_id varchar (20) not null,
  price float not NULL,
  total_stock int,
  pickup_address varchar (60) not null,
  description varchar (60),
  rating float,
  foreign key (supplier_id) references supplier (supplier_id) on delete cascade,
  primary key (product_id, supplier_id)
);

/*  Here: (product_id, order_id, supplier_id) -> R is the only relevant dependency and hence it is in BCNF  */
create table product_order (
  product_id varchar(20) not null,
  order_id varchar (20) not null,
  supplier_id varchar (20),
  product_rating int check (product_rating in (1, 2, 3, 4, 5)),
  supplier_rating int check (supplier_rating in (1, 2, 3, 4, 5)),
  ship_index int,
  product_review varchar (60),
  supplier_review varchar (60),
  quantity int,
  selling_price float,
  primary key (product_id, order_id),
  foreign key (product_id) references product (product_id) on delete cascade,
  foreign key (order_id) references order_ (order_id) on delete cascade,
  foreign key (supplier_id) references supplier (supplier_id) on delete set null,
  foreign key (ship_index) references track (index_) on delete set null
);


CREATE VIEW orderPrice AS (select order_id, sum(selling_price * quantity) as total_price
                           FROM (product_order)
                           GROUP BY order_id); 

CREATE VIEW previousOrders AS (SELECT T1.order_id, T1.shipping_address, T2.date_, T3.total_price
                               FROM (order_ as T1) NATURAL JOIN (payment as T2) NATURAL JOIN (orderPrice as T3)
                               WHERE T1.customer_id IN (SELECT user()));

CREATE VIEW listOrders AS (SELECT order_id
                            FROM order_ 
                            WHERE customer_id IN (SELECT user()));

CREATE VIEW trackID AS (SELECT order_id, product_id, ship_index
                        FROM product_order
                        WHERE order_id IN (SELECT * FROM listOrders));

CREATE VIEW packageStatus AS (SELECT T1.order_id, T1.product_id, T1.ship_index, T2.tracking_id
                              FROM (trackID as T1) JOIN (track as T2) ON (T1.ship_index = T2.index_));

CREATE VIEW supplierProducts AS (SELECT product_id, product_name, price, total_stock, pickup_address, description 
                                  FROM product
                                  WHERE supplier_id = (SELECT user()));

CREATE VIEW supplierOrders AS (SELECT T1.supplier_id, T1.product_id, T1.quantity, T1.selling_price, T2.date_
                                FROM (product_order as T1) natural join (payment as T2)
                                WHERE T1.supplier_id = (SELECT user()));

CREATE VIEW shipperTrack AS (SELECT index_, pickup_address AS source, shipping_address AS destination, tracking_id
                              FROM (track JOIN product_order ON index_ = ship_index) NATURAL JOIN order_ NATURAL JOIN product WHERE shipper_id = (SELECT user()));

DROP ROLE dbadmin;
DROP ROLE customer;
DROP ROLE supplier;
DROP ROLE shipper;

CREATE ROLE dbadmin;
CREATE ROLE customer;
CREATE ROLE supplier;
CREATE ROLE shipper;

GRANT ALL PRIVILEGES ON AmaKart.* TO dbadmin;

DELIMITER //
CREATE TRIGGER setPrice BEFORE INSERT on product_order
FOR EACH ROW BEGIN
  SET NEW.selling_price = (SELECT price FROM product WHERE product_id = NEW.product_id and supplier_id = NEW.supplier_id);
END//
DELIMITER ;

INSERT INTO customer Values ("Nikhil@localhost","Nikhil Kumar","ROOM-119",8281112705,"111601013@");
INSERT INTO supplier Values ("Sourabh@localhost","Sourabh Agg","ROOM-211",8281112700,"111601025@");
INSERT INTO shipper Values ("FEDEx@localhost","FEDEx","Delhi",1800123343,"111601020@");

INSERT INTO product Values ("1","Rasgulla","Sourabh@localhost",10,100.0,"RM3xx","Rasgulla from Aggarwal Sweets");

INSERT INTO payment Values ("1","4362536563578",NULL,"CompLabFF");

INSERT INTO order_ Values ("1","Nikhil@localhost","RM-119","1");

INSERT INTO track(shipper_id) Values ("FEDEx@localhost");

INSERT INTO product_order(product_id, order_id, supplier_id, product_rating, supplier_rating, ship_index, product_review, supplier_review, quantity) Values ("1","1","Sourabh@localhost",5,4,1,NULL,NULL,10);
