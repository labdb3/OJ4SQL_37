create table S(sno varchar(8), sname varchar(20), status integer, city varchar(10), primary key(sno));
create table P(pno varchar(8), pname varchar(20), color varchar(10), weight integer, city varchar(10), primary key(pno));
create table J(jno varchar(8), jname varchar(20), city varchar(10), primary key(jno));
create table SPJ(sno varchar(8), pno varchar(8), jno varchar(8), qty integer, price integer, primary key(sno, pno, jno), foreign key(sno) references S(sno), foreign key(pno) references P(pno), foreign key(jno) references J(jno));
