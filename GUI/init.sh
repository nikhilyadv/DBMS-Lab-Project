#!/bin/bash

value=`cat /home/sourabh/Documents/Github/DBMS-Lab-Project/Schema.sql`
mysql -u root -proot <<MY_QUERY
$value
MY_QUERY
