create table customer (
  customer_id VARCHAR (20) primary key not null,
  name VARCHAR (20) not null,
  address VARCHAR (60) not null,
  phone_number DECIMAL (10) UNSIGNED not null,
  email_id VARCHAR (20) not null
);

create table payment (
  payment_id int AUTO_INCREMENT primary key not null,
  credit_card_number VARCHAR (20) not null,
  date_ timestamp,
  billing_address varchar(60) not null
);

create table order_ (
  order_id int AUTO_INCREMENT primary key not null,
  customer_id VARCHAR (20),
  shipping_address varchar(60) not null,
  payment_id int,
  foreign key (customer_id) references customer (customer_id) on delete set null,
  foreign key (payment_id) references payment (payment_id) on delete set null
);

create table seller (
  seller_id varchar (20) primary key not null,
  name varchar (20) not null,
  address varchar (60) not null,
  phone_number decimal (10) UNSIGNED NOT NULL,
  email_id VARCHAR (20) not null,
  rating float
);

create table shipper (
  shipper_id varchar (20) primary key not null,
  name varchar (20) not null,
  head_quarters varchar (60) not null,
  phone_number decimal (10) UNSIGNED not null,
  email_id VARCHAR (20) not null
);

create table track (
  index_ INT AUTO_INCREMENT primary key not null,
  shipper_id varchar (20),
  tracking_id varchar (20),
  date_ DATE,
  foreign key (shipper_id) references shipper (shipper_id) on delete set null
);

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

create table cart (
  customer_id varchar(20),
  product_id varchar(20),
  seller_id varchar(20),
  quantity int,
  primary key (customer_id,product_id,seller_id),
  foreign key (customer_id) references customer(customer_id) on delete cascade,
  foreign key (product_id,seller_id) references product(product_id,seller_id) on delete cascade
);