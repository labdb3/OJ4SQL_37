-- this script should be run by dba

CREATE DATABASE testdb DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE ROLE teacherrole;
GRANT ALL PRIVILEGES ON *.* TO teacherrole with GRANT OPTION;
CREATE USER teacher identified BY 'Oj4dblcui_';
GRANT teacherrole TO teacher;
SET DEFAULT ROLE ALL TO teacher;

CREATE ROLE student_role_s;
CREATE USER s1 identified by 'students@mysql@DB3';
GRANT student_role_s to s1;
SET DEFAULT ROLE student_role_s to s1;
