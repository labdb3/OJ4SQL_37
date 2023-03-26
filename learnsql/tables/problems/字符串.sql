--d Like中的转义字符----建表
create table  testLike (str  char(10));
insert into testLike  values ('x%x_x'), ('%xx_x'), ('%xx_xx'), ('%__x');

--d Like中的转义字符----查询
select  *  from  testLike where  str  like  'x%%x__xx'  escape 'x';

--d Like操作示例的数据准备
create table  guest(gname char(20));
insert into  guest  values  ('tOm'),('jerry'),('John'),('Carefully_李');

--d Like操作---查询1
select   	gname from     	guest where   	gname  like  '%o%';

--d Like操作---查询2
select   	gname from     	guest where   	gname  like binary  '%o%';

--d Like操作---查询3
select   	gname from     	guest where   	upper(gname)  like binary  '%O%';

--d 列出姓名中含有3个以上字符，且倒数第三个是y，倒数第二个是_的游客
select 	 gname from   guest where   gname  like '%_yx__'  escape 'x' ;

--d 列出姓名中包含字母o且至少包含4个字符的游客--写法1
select   gname from     guest where   	gname  like  '%o%'	and 	gname not like '___' 	and 	gname not like '__'     and     gname not like '_';

--d 列出姓名中包含字母o且至少包含4个字符的游客--写法2
select   	gname from     	guest where   	gname  like  'o___%'    or	 	gname  like  '_o__%'    or	 	gname  like  '__o_%'    or	 	gname  like  '___o%';

--d 列出姓名中包含字母o且至少包含4个字符的游客--写法3
select   	gname from     	guest where   	gname  like  '%o%'    and   	length(gname)>3;

--d 正则表达式语法查询示例
select 'abc' regexp '^a','abc' regexp 'a$';
select 'abc' regexp '.a','abc' regexp 'a';
select 'abc' regexp '[xbz]','a' regexp '[^ab]','ab' regexp '[^a]';

--d 正则表达式语法查询示例
select 'abc' regexp '.b*.','abc' regexp 'a.b+','abbc' regexp 'ab+c';
select  'ca'  regexp  '^(a|b)','ca'  regexp '[^(a|b)]';
select 'xaaaay' regexp 'xa{3,5}y','xababay' regexp 'x(bab)y';

--d 正则表达式语法查询示例--建表
create table my_name (id int auto_increment, name char(10),CONSTRAINT pk PRIMARY KEY (id));
insert into my_name(name) values ('陈佳'),('李佳'),('刘佳');
insert into my_name(name) values ('郝运来'),('牛得草'),('于得水'),('于成龙'),('吴法天'),('吴奈和');
insert into my_name(name) values ('赵子轩'),('钱多多'),('孙宇轩'),('李子涵'),('周蕴涵'),('郑其时'),('王蕴佳');

--d 正则表达式语法查询示例1
select name from my_name where name regexp '^吴';

--d 正则表达式语法查询示例2
select name from my_name where name regexp '轩$';

--d 正则表达式语法查询示例3
select name from my_name where name regexp '轩涵?';

--d 正则表达式语法查询示例4
select name from my_name where name regexp '钱..';

--d 正则表达式语法查询示例5
select name from my_name where name regexp '[^轩佳涵]';

--d 全文索引查询示例---建表
create table  myDoc (
	id  	int  auto_increment  primary key,
	title  	varchar(100), content text,
	fulltext (title, content) );
insert into myDoc (title,content) values
	('MySQL Tutorial', 'DBMS stands for DataBase ...'),
	('How To Use MySQL Well', 'After you went through a ...'),
	('Optimizing MySQL', 'In this tutorial we will show ...'),
	('1001 MySQL Tricks', '1. Never run mysqld as root. 2. ...'),
	('MySQL vs. YourSQL', 'In the following database comparison ...'),
	('MySQL Security', 'When configured properly, MySQL ...');

--d 全文检索查询示例
select  id, content, match(title, content)  against ('Security implications of running MySQL as root' ) as  score  from myDoc where   match(title, content) against ('Security implications of running MySQL as root')

--d 全文检索查询示例
select  *  from myDoc where match(title, content)  against ('+MySQL -YourSQL' in boolean mode);
