CREATE SCHEMA IF NOT EXISTS project;
USE project;
SET SQL_SAFE_UPDATES = 0;
SET GLOBAL sql_mode = (SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));

SELECT * FROM Copies;
SELECT * FROM Borrows;
-- drop order
DROP TABLE IF EXISTS Borrows;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Copies;
DROP TABLE IF EXISTS Librarian;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Branches;
DROP TABLE IF EXISTS Users;

-- users
CREATE TABLE IF NOT EXISTS Users
(
  UserMail VARCHAR(45) NOT NULL,
  User_First_Name VARCHAR(30),
  User_Surname VARCHAR(30),
  City VARCHAR(30),
  Street VARCHAR(30),
  Apartment_Number VARCHAR(30),
  User_Phone_Number INT,
  Date_Of_Birth DATE NOT NULL,
  User_Password VARCHAR(30) NOT NULL,
  PRIMARY KEY (UserMail)
);
INSERT INTO Users VALUES('nadavilany@gmail.com','Nadav','Ilany','Kokhav Yair','Egoz','43','0542558955','1997-09-14',12345678);
INSERT INTO Users VALUES('orsalem@gmail.com','Or','Salem','Yavne','shona hadasha','1','0541111111','1997-09-15',12345678);
INSERT INTO Users VALUES('yuvalbarhalevy@gmail.com','yuval','halevy','tel aviv','dizingof','2','0541111111','1997-09-16',12345678);
INSERT INTO Users VALUES('annazack@gmail.com','anna','zack','shimshon','mi zot','6','0541111121','1997-09-12',12345678);
INSERT INTO Users VALUES('eyalgolan@gmail.com','eyal','golan','everywhere','pantera','8','0541111131','2001-03-12',12345678);

-- branches
CREATE TABLE IF NOT EXISTS Branches
(
  Branch_Name VARCHAR(30) NOT NULL,
  Phone_Number INT NOT NULL,
  Branch_Address VARCHAR(30) NOT NULL,
  PRIMARY KEY (Branch_Address)
);
INSERT INTO Branches VALUES('petah tikvas library',0541111111,'yesod hamaala 2 petah tikva');
INSERT INTO Branches VALUES('tau medoyakim',0541111111,'tel aviv 201');

-- Books
CREATE TABLE IF NOT EXISTS Books
(
  BookID INT NOT NULL,
  BookName VARCHAR(30) NOT NULL,
  AuthorName VARCHAR(30) NOT NULL,
  Year_of_Publication INT NOT NULL,
  Publsher VARCHAR(30),
  BookImage VARCHAR(100),
  PRIMARY KEY (BookID)
);
INSERT INTO Books VALUES(001,'Harry Potter 1','JK Rowling',1999,'Group 6','https://m.media-amazon.com/images/I/71WKvIYkKHL._AC_UY327_FMwebp_QL65_.jpg');
INSERT INTO Books VALUES(002,'Harry Potter 2','JK Rowling',2001,'Group 6','https://m.media-amazon.com/images/I/91u+AfDBxlL._AC_UY327_FMwebp_QL65_.jpg');
INSERT INTO Books VALUES(003,'Harry Potter 3','JK Rowling',2003,'Group 6','https://m.media-amazon.com/images/I/81pLQchf27L._AC_UY327_FMwebp_QL65_.jpg');
INSERT INTO Books VALUES(004,'Harry Potter 4','JK Rowling',2003,'Group 6','https://m.media-amazon.com/images/I/81-VF3jm7NL._AC_UY327_FMwebp_QL65_.jpg');
INSERT INTO Books VALUES(005,'The Alchemist','Paulo Cohelo',1990,'Group 6','https://m.media-amazon.com/images/I/51kcX5PpaZL._AC_UY327_FMwebp_QL65_.jpg');
INSERT INTO Books VALUES(006,'A Game of Thrones',' George R.R. Martin',1996,'Group 6','https://m.media-amazon.com/images/I/51rDpMtBm5L.jpg');
INSERT INTO Books VALUES(007,'A Clash of Kings',' George R.R. Martin',1999,'Group 6','https://m.media-amazon.com/images/I/61lu4iDmAEL.jpg');
INSERT INTO Books VALUES(008,'A Storm of Swords',' George R.R. Martin',2000,'Group 6','https://m.media-amazon.com/images/I/511+DbzTZ+L.jpg');
INSERT INTO Books VALUES(009,'Rich Dad Poor Dad',' Robert Kiyosaki',1997,'Group 6','https://m.media-amazon.com/images/P/B07C7M8SX9.01._SCLZZZZZZZ_SX500_.jpg');
INSERT INTO Books VALUES(010,'Thinking, Fast and Slow',' Daniel Kahneman ',2010,'Group 6','https://m.media-amazon.com/images/P/0374533555.01._SCLZZZZZZZ_SX500_.jpg');
INSERT INTO Books VALUES(011,'The 5AM Club',' Robin Sharma ',2020,'Group 6','https://m.media-amazon.com/images/I/41PfrH8qb3L.jpg');
INSERT INTO Books VALUES(012,'Magnus Chase and the Gods',' Rick Riodan ',2020,'Group 6','https://m.media-amazon.com/images/I/61qSRYof0-L._SY346_.jpg');
INSERT INTO Books VALUES(013,'Think and Grow Rich',' Napoleon Hill ',1937,'Group 6','https://m.media-amazon.com/images/I/51ncDBWm8ZL.jpg');
INSERT INTO Books VALUES(014,'Six Years','Harlan Coben',2010,'Group 6','https://m.media-amazon.com/images/I/51qzQRQrpHL.jpg');
INSERT INTO Books VALUES(015,'Missing You','Harlan Coben',2014,'Group 6','https://m.media-amazon.com/images/I/51l5AsD5eiS.jpg');
INSERT INTO Books VALUES(016,'No Second Chance','Harlan Coben',2004,'Group 6','https://m.media-amazon.com/images/I/41Sj1nnk1SL.jpg');
INSERT INTO Books VALUES(017,'Tell No One','Harlan Coben',2009,'Group 6','https://m.media-amazon.com/images/I/41KX-GKdzQS.jpg');
INSERT INTO Books VALUES(018,'The Cuban Affair','Nelson Demill',2017,'Group 6','https://m.media-amazon.com/images/I/51+giWD6kqL.jpg');
INSERT INTO Books VALUES(019,'Past Tense: A Jack Reacher','Lee Child',2018,'Group 6','https://m.media-amazon.com/images/I/418C5n1DtKL.jpg');
INSERT INTO Books VALUES(020,'No Middle Name','Lee Child',2017,'Group 6','https://m.media-amazon.com/images/I/51RqNU5E9gL.jpg');


-- Librarians
CREATE TABLE IF NOT EXISTS Librarian
(
  Librarian_Email VARCHAR(30) NOT NULL,
  Librarian_Password VARCHAR(30) NOT NULL,
  Branch_Address VARCHAR(30) NOT NULL,
  Start_Date DATE NOT NULL,
  Librarian_Phone_Number INT NOT NULL,
  City VARCHAR(30),
  Street VARCHAR(30),
  Apartment_Number VARCHAR(30),
  Librarian_First_Name VARCHAR(30),
  Librarian_Surname VARCHAR(30),
  PRIMARY KEY (Librarian_Email),
  FOREIGN KEY (Branch_Address) REFERENCES Branches(Branch_Address) ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO Librarian VALUES('amitkaplan@gmail.com','12345678','yesod hamaala 2 petah tikva','2022-10-10',054111111,'petah tikva','yesod hamaala','2b','amit','kaplan');
INSERT INTO Librarian VALUES('danyamin@gmail.com','12345678','tel aviv 201','2010-10-10',054111111,'petah tikva','yesod hamaala','3b','dan','yamin');
INSERT INTO Librarian VALUES('yuvalshalom@gmail.com','12345678','tel aviv 201','2010-10-10',054111111,'petah tikva','yesod hamaala','4b','dan','yamin');

-- Copies
CREATE TABLE  IF NOT EXISTS Copies
(
  Copy_Status VARCHAR(30),
  CopyID INT NOT NULL auto_increment,
  Branch_Address VARCHAR(30) NOT NULL,
  BookID INT NOT NULL,
  PRIMARY KEY (CopyID, Branch_Address, BookID),
  FOREIGN KEY (Branch_Address) REFERENCES Branches(Branch_Address) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (BookID) REFERENCES Books(BookID) ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO Copies VALUES('Ordered',NULL,'yesod hamaala 2 petah tikva',001);
INSERT INTO Copies VALUES('Ordered',NULL,'yesod hamaala 2 petah tikva',002);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',001);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',001);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',001);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',001);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',003);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',002);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',002);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',002);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',003);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',002);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',003);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',002);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',002);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',001);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',002);
INSERT INTO Copies VALUES('Borrowed',NULL,'tel aviv 201',003);
INSERT INTO Copies VALUES('Borrowed',NULL,'tel aviv 201',002);
INSERT INTO Copies VALUES('Ordered',NULL,'tel aviv 201',004);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',004);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',005);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',005);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',006);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',007);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',005);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',006);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',007);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',006);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',007);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',008);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',010);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',011);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',012);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',013);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',014);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',015);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',016);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',017);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',018);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',019);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',020);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',003);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',004);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',005);
INSERT INTO Copies VALUES('Available',NULL,'yesod hamaala 2 petah tikva',009);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',003);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',004);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',005);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',009);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',006);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',007);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',008);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',010);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',011);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',012);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',013);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',014);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',015);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',016);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',017);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',018);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',019);
INSERT INTO Copies VALUES('Available',NULL,'tel aviv 201',020);

-- Borrows
CREATE TABLE IF NOT EXISTS Borrows
(
  Return_Date DATE,
  Real_Return_Date DATE,
  BorrowDate DATE NOT NULL,
  Extension_Request DATE,
  UserMail VARCHAR(45) NOT NULL,
  CopyID INT NOT NULL,
  PRIMARY KEY (BorrowDate, UserMail,CopyID),
  FOREIGN KEY (UserMail) REFERENCES Users(UserMail) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (CopyID) REFERENCES Copies(CopyID) ON DELETE CASCADE ON UPDATE CASCADE
);
-- active borrows
INSERT INTO Borrows VALUES('2023-02-05',NULL,'2023-01-20',NULL,'orsalem@gmail.com',1);
INSERT INTO Borrows VALUES('2023-02-06',NULL,'2023-01-20',NULL,'yuvalbarhalevy@gmail.com',2);
INSERT INTO Borrows VALUES('2023-02-05',NULL,'2023-01-20',NULL,'nadavilany@gmail.com',18);
INSERT INTO Borrows VALUES('2023-02-05',NULL,'2023-01-21',NULL,'nadavilany@gmail.com',19);
INSERT INTO Borrows VALUES('2023-01-30',NULL,'2023-01-20',NULL,'orsalem@gmail.com',20);
INSERT INTO Borrows VALUES('2023-01-29',NULL,'2023-01-20',NULL,'yuvalbarhalevy@gmail.com',21);
-- history borrows
INSERT INTO Borrows VALUES('2023-01-05','2023-01-02','2022-12-15','2022-12-29','orsalem@gmail.com',4);
INSERT INTO Borrows VALUES('2023-01-03','2023-01-01','2022-12-20',NULL,'orsalem@gmail.com',5);
INSERT INTO Borrows VALUES('2022-03-15','2022-03-05','2022-03-01',NULL,'nadavilany@gmail.com',4);
INSERT INTO Borrows VALUES('2022-11-29','2022-11-29','2022-11-10',NULL,'nadavilany@gmail.com',7);
INSERT INTO Borrows VALUES('2022-12-20','2022-12-05','2022-11-30',NULL,'yuvalbarhalevy@gmail.com',7);
INSERT INTO Borrows VALUES('2022-12-25','2022-12-11','2022-12-07',NULL,'orsalem@gmail.com',7);
INSERT INTO Borrows VALUES('2022-05-26','2022-05-22','2022-05-12',NULL,'yuvalbarhalevy@gmail.com',9);
INSERT INTO Borrows VALUES('2022-03-03','2022-02-22','2022-02-20',NULL,'yuvalbarhalevy@gmail.com',13);
INSERT INTO Borrows VALUES('2022-03-15','2022-02-26','2022-02-24',NULL,'orsalem@gmail.com',13);
INSERT INTO Borrows VALUES('2022-03-18','2022-02-28','2022-02-27',NULL,'nadavilany@gmail.com',13);
INSERT INTO Borrows VALUES('2022-04-03','2022-03-22','2022-02-20',NULL,'orsalem@gmail.com',21);
INSERT INTO Borrows VALUES('2022-04-03','2022-03-22','2022-03-12','2022-03-27','eyalgolan@gmail.com',23);
INSERT INTO Borrows VALUES('2022-04-03','2022-03-25','2022-03-10','2022-03-27','annazack@gmail.com',24);
INSERT INTO Borrows VALUES('2022-04-03','2022-03-28','2022-03-15','2022-03-27','annazack@gmail.com',25);
INSERT INTO Borrows VALUES('2022-05-01','2022-05-01','2022-04-12','2022-04-14','eyalgolan@gmail.com',26);
INSERT INTO Borrows VALUES('2022-05-17','2022-05-15','2022-05-03','2022-05-20','annazack@gmail.com',26);
INSERT INTO Borrows VALUES('2022-03-01','2022-02-25','2022-02-03',NULL,'annazack@gmail.com',2);
INSERT INTO Borrows VALUES('2022-03-05','2022-02-28','2022-02-26',NULL,'eyalgolan@gmail.com',2);


-- Orderes
CREATE TABLE IF NOT EXISTS Orders
(
  Orders_Status VARCHAR(15) NOT NULL,
  Order_Date DATE NOT NULL,
  UserMail VARCHAR(45) NOT NULL,
  CopyID INT NOT NULL,
  PRIMARY KEY (Order_Date, UserMail,CopyID),
  FOREIGN KEY (UserMail) REFERENCES Users(UserMail) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (CopyID) REFERENCES Copies(CopyID) ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO Orders VALUES('Waiting','2022-12-20','nadavilany@gmail.com',21);
INSERT INTO Orders VALUES('waiting','2023-01-25','annazack@gmail.com',2);
INSERT INTO Orders VALUES('waiting','2023-01-25','eyalgolan@gmail.com',1);
INSERT INTO Orders VALUES('taken by user','2022-11-11','yuvalbarhalevy@gmail.com',7);
INSERT INTO Orders VALUES('taken by user','2022-11-30','orsalem@gmail.com',7);
INSERT INTO Orders VALUES('taken by user','2022-02-20','orsalem@gmail.com',13);
INSERT INTO Orders VALUES('taken by user','2022-02-25','nadavilany@gmail.com',13);
INSERT INTO Orders VALUES('taken by user','2022-04-01','annazack@gmail.com',10);
INSERT INTO Orders VALUES('taken by user','2022-04-15','annazack@gmail.com',26);
