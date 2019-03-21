#!/bin/bash

value=`cat ../Schema.sql`
mysql -u root -proot <<MY_QUERY
$value
MY_QUERY
