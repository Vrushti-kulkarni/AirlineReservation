create database practice;
USE practice;

create table Students 
(St_id int PRIMARY KEY AUTO_INCREMENT,
 St_name varchar(10) NOT NULL,
 St_ph_no varchar(15) NOT NULL
 );
 
 desc Students;
 
 ALTER TABLE Students 
 ADD (St_course char(20) NOT NULL);
 ALTER TABLE Students 
 DROP St_course;
 ALTER TABLE Students 
 modify St_name varchar(15) NOT NULL; 
 ALTER TABLE Students
 rename column St_name to St_naming;
 
 Rename TABLE Students to Student;
 
 truncate TABLE Student;
 DROP TABLE Student;
 
 CREATE TABLE student_course(
 ID int PRIMARY KEY auto_increment,
 subject varchar(10)
 );
 
 INSERT into student_course(ID, subject) VALUES (1, 'science');
 INSERT into student_course(ID, subject) VALUES (2, 'maths');
INSERT into student_course(ID, subject) VALUES (3, 'geography');
INSERT into student_course(ID, subject) VALUES (4, 'history');

ALTER TABLE Students ADD COLUMN course_id INT;
ALTER TABLE Students 
ADD CONSTRAINT student_course
FOREIGN KEY (course_id) 
REFERENCES student_course(ID);

desc Students;
insert into Students values (1, 'vrushti', 8928984673, 2);
Select * from Students;
insert into Students values (2, 'ram', 8928984673, 3);
insert into Students values (3, 'lam', 8928984673, 3);
update Students set St_naming = 'ramesh' where St_id = 2;
Select * from Students;

desc student_course;

Select min(course_id) AS lowest from Students;
select * from Students;

Select count(*) from Students where course_id = 2;

select st_naming from Students where course_id = 3;

select * from Students where St_naming LIKE '_a%';

select Students.st_naming, student_course.subject from Students INNER JOIN student_course ON Students.course_id = student_course.ID;

select Students.st_naming, student_course.subject from student_course LEFT JOIN Students ON Students.course_id = student_course.ID;

select Students.st_naming, student_course.subject from student_course RIGHT JOIN Students ON Students.course_id = student_course.ID;

desc Students;
start transaction;
insert into Students values (4,'vru', 8928984673,4);
SET SQL_SAFE_UPDATES = 1;
delete from Students where St_naming = 'ramesh';
ROLLBACK;

SELECT * FROM Students;

CREATE VIEW viewing AS SELECT St_naming, St_id FROM Students where St_id > 1;
select * from viewing;

CREATE VIEW viewing3 AS SELECT Students.St_naming, Students.St_id, student_course.subject From Students, student_course where Students.st_id = student_course.ID; 
select * from viewing3;

delimiter //
CREATE trigger trigger1 
before insert on Students
for each row 
if new.course_id = 2 then SET new.course_id = 5;
end if; //	


select * from Students;
select * from student_course;
insert into Students values (6, 'lelu', 8928984673, 2);
 
INSERT INTO student_course (ID, subject) 
VALUES (5, 'coco'); 
