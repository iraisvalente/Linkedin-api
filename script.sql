USE linkedin;

CREATE TABLE Users(
	Id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	First_Name varchar(255),
    Last_Name varchar(255),
    Email_Address varchar(255),
    Company varchar(255),
    Position varchar(255), 
    Password_user BLOB
);

CREATE TABLE Connections(
	First_Name varchar(255),
    Last_Name varchar(255),
    Email_Address varchar(255),
    Company varchar(255),
    Position varchar(255),
    Connection varchar(255),
    Upload_Date datetime default current_timestamp
);

CREATE TABLE Positions(
	Id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	Position varchar(255)
);

CREATE TABLE Searches(
	Id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Note VARCHAR(255),
    Search BOOLEAN,
    Connection_first_name VARCHAR(255),
    Connection_last_name VARCHAR(255),
    Connection_email VARCHAR(255),
    Connection_company VARCHAR(255),
    Connection_position VARCHAR(255),
    Connection_connection VARCHAR(255)
);