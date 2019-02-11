create table Users (
  username VARCHAR (20) primary key not null,
  passcode VARCHAR (20) not null,
  role VARCHAR (20) not null
);

create table customer (
  customer_id VARCHAR (20) primary key not null,
  name VARCHAR (20) not null,
  address VARCHAR (60) not null,
  phone_number DECIMAL (10) UNSIGNED not null,
  email_id VARCHAR (20) not null,
  foreign key (customer_id) references Users(username) on delete cascade
);

create table payment (
  payment_id VARCHAR (20) primary key not null,
  credit_card_number VARCHAR (20) not null,
  date_ timestamp,
  billing_address varchar(60) not null
);

create table order_ (
  order_id VARCHAR (20) primary key not null,
  customer_id VARCHAR (20),
  shipping_address varchar(60) not null,
  payment_id VARCHAR (20),
  foreign key (customer_id) references customer (customer_id) on delete set null,
  foreign key (payment_id) references payment (payment_id) on delete set null
);

create table supplier (
  supplier_id varchar (20) primary key not null,
  name varchar (20) not null,
  address varchar (60) not null,
  phone_number decimal (10) UNSIGNED NOT NULL,
  email_id VARCHAR (20) not null,
  foreign key (supplier_id) references Users(username) on delete cascade
);

create table shipper (
  shipper_id varchar (20) primary key not null,
  name varchar (20) not null,
  head_quarters varchar (60) not null,
  phone_number decimal (10) UNSIGNED not null,
  email_id VARCHAR (20) not null,
  foreign key (shipper_id) references Users(username) on delete cascade
);

create table track (
  index_ INT AUTO_INCREMENT primary key not null,
  shipper_id varchar (20),
  tracking_id varchar (20),
  foreign key (shipper_id) references shipper (shipper_id) on delete set null
);

create table product (
  product_id varchar (20) not null,
  supplier_id varchar (20) not null,
  price float not NULL,
  total_stock int,
  description varchar (60),
  foreign key (supplier_id) references supplier (supplier_id) on delete cascade,
  primary key (product_id, supplier_id)
);

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
  primary key (product_id, order_id),
  foreign key (product_id) references product (product_id) on delete cascade,
  foreign key (order_id) references order_ (order_id) on delete cascade,
  foreign key (supplier_id) references supplier (supplier_id) on delete set null,
  foreign key (ship_index) references track (index_) on delete set null
);

INSERT INTO Users Values ("Nikhil", "lol", "CUS");
INSERT INTO Users Values ("Sourabh", "foo", "SUP");
INSERT INTO Users Values ("FEDEx", "goo", "SHI");

INSERT INTO customer Values ("Nikhil","Nikhil Kumar","ROOM-119",8281112705,"111601013@");
INSERT INTO supplier Values ("Sourabh","Sourabh Agg","ROOM-211",8281112700,"111601025@");
INSERT INTO shipper Values ("FEDEx","FEDEx","Delhi",1800123343,"111601020@");

INSERT INTO product Values ("1","Sourabh",10,100.0,"Rasgulla from Aggarwal Sweets");

INSERT INTO payment Values ("1","4362536563578",NULL,"CompLabFF");

INSERT INTO order_ Values ("1","Nikhil","RM-119","1");

INSERT INTO track(shipper_id) Values ("FEDEx");

INSERT INTO product_order Values ("1","1","Sourabh",5,4,1,NULL,NULL,10);

