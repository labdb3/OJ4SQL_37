# OJ4SQL

An Online Judge Sysetm for Database Courses

## 关于pg 和 og 

因为华为服务器总是有很奇怪的问题，包括重启之后文件莫名回退到历史的更改，mac or windows 远程连接之后无法正常修改文件，操作系统为华为自研导致常规命令无法执行，后期只在oj 模块提供mysql,postgresql,其他模块只提供mysql的使用，去掉opengauss 的支持。


## 网站初始化流程

# 1. OJ 部分初始化流程

1. 运行sql下的sql语句，创建必要的表结构
2. 增加题目
3. data目录下的题目进行初始化，插入数据。

### postgresql后台数据库初始化

```sh
docker run --name pg_oj4db_backend -p 127.0.0.1:64320:5432 -e POSTGRES_PASSWORD=root@lab3 -d postgres
docker exec -it pg_oj4db_backend psql -U postgres -W
```

输入 `sql/oj4db_admin_postgresql.sql` 中的全部语句

### mysql

```sh
docker run --name=my_oj_test -p 43062:3306 -d mysql/mysql-server
# 获取初始密码
docker logs my_oj_test 2>&1 | grep GENERATED
# 修改密码
docker exec -it my_oj_test mysql -uroot -p
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root@lab3';
```

输入 `sql/mysql/init.sql` 中的全部语句

### postgresql

```sh
docker run --name pg_oj_test -p 127.0.0.1:64321:5432 -e POSTGRES_PASSWORD=root@lab3 -d postgres
docker exec -it pg_oj_test psql -U postgres -W
```

输入 `sql/postgresql/init.sql` 中的全部语句

### opengauss

```sh
docker run --name og_oj_test --privileged=true -d -e GS_PASSWORD=root@LAB3 -p 35432:5432 enmotech/opengauss:latest
docker exec -it og_oj_test bash
gsql -d postgres -U gaussdb -W'root@LAB3'
```

输入 `sql/opengauss/init.sql` 中的全部语句


# 2. learnsql部分初始化流程

关于这部分的初始化，可以直接执行 bash reinit_docker.sh 文件，如遇到某些命令无法执行成功的情况，可以直接copy 命令单独执行

### mysql

```shell
# 新建容器
docker run --name learnsql_mysql -e MYSQL_ROOT_PASSWORD=root@lab3 -p 33062:3306 -d mysql/mysql-server

# 开启远程连接
docker exec -it learnsql_mysql bash
mysql -u root -p
use mysql;
update user set host = '%' where user = 'root';
flush privileges;
```

### postgresql

```shell
docker run --name learnsql_postgres -e POSTGRES_PASSWORD=root@lab3 -p 33063:5432 -d postgres

docker exec -it learnsql_postgres psql -U postgres -W

create database learnsql_pg_database;
```

# 3. learncase 部分初始化流程

## mysql

```shell
# 新建容器
docker run --name learncase_mysql -e MYSQL_ROOT_PASSWORD=root@lab3 -p 53306:3306 -d mysql/mysql-server

# 开启远程访问
docker exec -it learncase_mysql bash
mysql -u root -p
use mysql;
update user set host = '%' where user = 'root';
flush privileges;
```

## postgresql

```shell
docker run --name learncase_postgres -e POSTGRES_PASSWORD=root@lab3 -p 53307:5432 -d postgres

docker exec -it learncase_postgres psql -U postgres -W

create database learncase_pg_database;
```

# 4. practise 部分初始化流程

practise 部分虽然新建了数据库，但是并没有提供数据集的支持，鼓励学生们用mysql 完成实习。

## mysql

```shell
# 新建容器
docker run --name practise_mysql -e MYSQL_ROOT_PASSWORD=root@lab3 -p 43306:3306 -d mysql/mysql-server

# 开启远程访问
docker exec -it practise_mysql bash
mysql -u root -p


# 需要新建数据库 dataset 用于存储数据
create database dataset;
use mysql;
update user set host = '%' where user = 'root';
flush privileges;
```

## postgresql

```shell
docker run --name practise_postgres -e POSTGRES_PASSWORD=root@lab3 -p 43307:5432 -d postgres

docker exec -it practise_postgres psql -U postgres -W

create database practise_pg_database;
```

当上述docker 容器全部启动之后，可以执行addstudents.py 文件，目前已经添加了异常处理机制，添加重复的学生时会直接忽略。
PYTHONPATH=/home/fcg/deploy/OJ4SQL2021 python addstudents.py --add_user_account --add_user_db_learnsql --add_user_db_learncase --add_user_db_practise

# 5. jupyterhub 配置

```shell
# 将服务器学生名单拷贝到容器jupyterhub内部
docker cp 数据库选课名单.csv jupyterhub:/root/scripts/data

# 如果需要更新案例，可以使用下述命令
docker cp 银行案例.ipynb jupyterhub:/root/commons

# jupyterhub 内部脚本
# add_user 是增加容器内用户，可见于/home/XXXX
# cp2allusers 是拷贝 /root/commons/* 所有文件到所有用户家目录下
# data 目录下存储的是用户名单
(py37) root@fee96ed93219:~# ls scripts/
add_user.py  cp2allusers.py  data
(py37) root@fee96ed93219:~# 

# 关于 jupyterhub 的重启
# 需要首先删除 jupyterhub-proxy.pid 和 jupyterhub_cookie_secret
# 然后执行 `jupyterhub` 命令即可。
# 需要重启失败,可以查看是否端口占用,lsof -i:8000,然后 kill -9 pid 
(py37) root@fee96ed93219:~/jupyterhub# ls
jupyterhub-proxy.pid  jupyterhub.sqlite  jupyterhub_config.py  jupyterhub_cookie_secret
(py37) root@fee96ed93219:~/jupyterhub#
```

## 关于机器代理配置

因为这个机器不能直接访问外网，这样会造成无法安装各种库，所以我们搭建了一个代理链路，将该机器的所有请求都通过实验室的另一台机器代理。

原本代理服务器是 162.105.88.120，后来该机器出现了网络问题，更改为162.105.88.116。

如果新的代理机器出现问题，可以按照如下教程更改新的代理服务器。

### 1. 首先搭建代理机器

使用 tinyproxy 配置新的代理服务器，具体教程可以参考https://blog.51cto.com/u_15278282/2931913

### 2. 配置需要代理的机器

使用 proxychains4 ，具体配置教程可以参考https://zhuanlan.zhihu.com/p/385463291

### 3. docker 配置

```sudo vim /etc/systemd/system/docker.service.d/http-proxy.conf
sudo vim /etc/systemd/system/docker.service.d/proxy.conf
sudo vim /etc/systemd/system/docker.service.d/proxy.conf/http-proxy.conf
```

更改后需要重启docker

```
sudo systemctl daemon-reload
sudo systemctl restart docker
```

### 4. 容器配置

修改docker 配置后发现容器内部还是不能访问外网，后来经过在容器内配置以下环境变量
```
export proxy="http://162.105.88.116:3128"
export http_proxy=$proxy
export https_proxy=$proxy
export ftp_proxy=$proxy
export no_proxy="localhost, 127.0.0.1, ::1"
```


## Fix Bugs

[python - I use pymysql to execute query in MySQL, but why the process is still alive after I close the connectio
n? - Stack Overflow](https://stackoverflow.com/questions/56002258/i-use-pymysql-to-execute-query-in-mysql-but-why
-the-process-is-still-alive-afte)

## TODO

### P1

- [x] 导入SC数据集
- [x] 处理eval_ans, noeval_ans, noeval_noans三种回显类型
- [x] 实习数据集，可读可写
- [x] 评测场作答界面添加一个执行按钮，显示执行结果
- [ ] 代码自动保存和恢复（利用浏览器即可，不需要服务器端操作）

### P2

- [ ] 编写测试代码，主要是测试答案SQL能否正确运行并返回结果，以及压力测试。
- [x] 导入employees练习数据集
- [x] 问题列表中的难度现在是假的，在问题表中添加一列难度等级，然后修改每个问题的难度
- [x] 问题列表在难度右边添加一栏通过,如果通过就显示对号或鲜花，已经尝试但未通过显示减号，未尝试不显示
- [x] 标准答案不需要每次都执行获取结果，使用redis做一个LRU缓存
- [x] 浮点数近似评测
- [ ] 超时限制字段以及实现
- [ ] 成绩导出更新和备份

### P3

- [ ] SQL高亮
- [x] 用户请求列出组中题目时检查权限

## 注意事项

所有数据库名称使用小写

## 导入数据集和问题格式

`data/data`目录下每个文件夹都是一个数据库，里面每个文件是csv格式的表格内容。

`data/problems`目录下每个文件夹都是一个问题的集合，通常是一组问题，对应一个数据库，比如`./data/problems/spj`里面的每个文件夹都是一个问题，文件夹名称是问题名。

`./data/problems/spj/problems_list`文件罗列了问题列表，该顺序便是导入和网站显示的顺序。

`./data/problems/spj/列出所有供应商的信息` 里面的`desc`文件是问题描述，`judge_type`是裁判类型，裁判分为无序裁判`unordered`，有序裁判`ordered`，自定义裁判`custom`，无序裁判用于题目最后输出无序考虑元组顺序，有序裁判用于题目输出要考虑元组顺序的情况，自定义裁判暂时不会用到。

`./data/problems/spj/列出所有供应商的信息` 里面的`mysql/ans.sql``postgresql/ans.sql``opengauss/ans.sql`存放了各个数据库引擎的答案，如果该问题不支持的数据库引擎就不要为该数据库引擎编写答案

## [GuassDB基于python开发](https://support-it.huawei.com/docs/zh-cn/gaussdb-all/gaussdb100_1.0.1_development_guide_appliance/zh-cn_topic_0138590648.html)

```sh
sudo mkdir -p /opt/gaussdb/lib
sudo cp pyzenith.so /opt/gaussdb/lib/
echo 'export LD_LIBRARY_PATH=/opt/gaussdb/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

本目录下 export PYTHONPATH=$PYTHONPATH:`pwd`

## 其他

## 导出mysql到csv文件

```sh
mysql -uroot -proot@LAB3 -e "select * from testdb.dept_manager;" | sed -e  "s/\t/,/g" -e "s/NULL/  /g" -e "s/\n/\r\n/g" > dept_manager.csv
```

## 测试和部署分离

测试数据库的各种端口最高位+1,容器名称后边加_dev
