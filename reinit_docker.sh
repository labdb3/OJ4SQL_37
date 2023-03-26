# docker run -itd --name jupyterhub_practise -v commons:/root/commons -v Data:/root/Data -p 8004:8000 jupyterhub:v3
# docker run -itd --name jupyterhub_learncase -p 8005:8000 jupyterhub:v3
docker stop practise_mysql && docker rm practise_mysql
docker stop learncase_mysql && docker rm learncase_mysql
docker stop learnsql_mysql && docker rm learnsql_mysql
docker stop practise_postgres && docker rm practise_postgres
docker stop learncase_postgres && docker rm learncase_postgres
docker stop learnsql_postgres && docker rm learnsql_postgres


docker run --name practise_mysql -e MYSQL_ROOT_PASSWORD=root@lab3 -p 43306:3306  -d mysql/mysql-server
docker run --name practise_postgres -e POSTGRES_PASSWORD=root@lab3 -p 43307:5432 -d postgres

docker run --name learncase_mysql -e MYSQL_ROOT_PASSWORD=root@lab3 -p 53306:3306  -d mysql/mysql-server
docker run --name learncase_postgres -e POSTGRES_PASSWORD=root@lab3 -p 53307:5432 -d postgres


docker run --name learnsql_mysql -e MYSQL_ROOT_PASSWORD=root@lab3 -p 33062:3306  -d mysql/mysql-server
docker run --name learnsql_postgres -e POSTGRES_PASSWORD=root@lab3 -p 33063:5432 -d postgres

docker exec -u root -it learnsql_postgres sh -c 'PGPASSWORD=root@lab3 psql -U postgres -c "create database learnsql_pg_database;"'
docker exec -u root -it practise_postgres sh -c 'PGPASSWORD=root@lab3 psql -U postgres -c "create database practise_pg_database;"'
docker exec -u root -it learncase_postgres sh -c 'PGPASSWORD=root@lab3 psql -U postgres -c "create database learncase_pg_database;"'


# enable remote access
# update user set host = "%" where user = "root";
# FLUSH PRIVILEGES;
docker exec -u root -it learnsql_mysql sh -c 'mysql -u root --password=root@lab3 --database=mysql -e "update user set host = \"%\" where user = \"root\";"'
docker exec -u root -it learncase_mysql sh -c 'mysql -u root --password=root@lab3 --database=mysql -e "update user set host = \"%\" where user = \"root\";"'
docker exec -u root -it practise_mysql sh -c 'mysql -u root --password=root@lab3 --database=mysql -e "update user set host = \"%\" where user = \"root\";"'