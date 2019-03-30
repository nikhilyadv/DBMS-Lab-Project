#!/bin/bash

value=`cat createUser.sql`

mysql -u root -proot <<MY_QUERY
drop database AmaKart;
create database AmaKart;
use AmaKart;
source AmaKart_dump.sql
$value
MY_QUERY
