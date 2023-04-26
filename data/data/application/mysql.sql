create table  if not exists application(   
    id varchar(20),
    gender varchar(20),
    department varchar(20),
    acceptance varchar(20),
    primary key (id),
    check(gender = 'male' or gender ='female'),
    check(acceptance = 'yes' or acceptance ='no')
);
