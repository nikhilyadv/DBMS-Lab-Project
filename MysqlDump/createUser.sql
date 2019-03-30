DROP USER Nikhil;
DROP USER John;
DROP USER Sourabh;
DROP USER Harry;
DROP USER FEDEx;
DROP USER BlueDart;

CREATE USER Nikhil IDENTIFIED BY "hi";
CREATE USER John IDENTIFIED BY "hi";
CREATE USER Sourabh IDENTIFIED BY "hi";
CREATE USER Harry IDENTIFIED BY "hi";
CREATE USER FEDEx IDENTIFIED BY "hi";
CREATE USER BlueDart IDENTIFIED BY "hi";

GRANT customer to Nikhil;
GRANT customer to John;
GRANT seller to Sourabh;
GRANT seller to Harry;
GRANT shipper to FEDEx;
GRANT shipper to BlueDart;