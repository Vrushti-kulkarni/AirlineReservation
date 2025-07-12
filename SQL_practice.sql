create database practice;
USE practice;

create table Students 
(St_id int PRIMARY KEY AUTO_INCREMENT,
 St_name varchar(10) NOT NULL,
 St_ph_no varchar(15) NOT NULL
 );
 
 desc Students;
 
 ALTER TABLE Students 
 ADD column (St_course char(20) NOT NULL);
 ALTER TABLE Students 
 DROP St_course;
 ALTER TABLE Students 
 modify column St_name varchar(15) NOT NULL; 
 
 Rename TABLE Students to Student;
 
 truncate TABLE Student;
 DROP TABLE Student;
 
 