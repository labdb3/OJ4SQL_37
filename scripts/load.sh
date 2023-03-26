python load.py --type create --dbname spj --engines mysql postgresql opengauss --path ./data/data/SPJ/ --perm readonly
python load.py --type load --dbname spj --engines mysql postgresql opengauss --path ./data/data/SPJ/
./batch_load.sh ./data/problems/spj/ spj 2

python load.py --type create --dbname employees --engines mysql postgresql opengauss --path ./data/data/employees/ --perm readonly
python load.py --type load --dbname employees --engines mysql postgresql opengauss --path ./data/data/employees/
./batch_load.sh ./data/problems/employees/ employees 3

python load.py --type create --dbname elective --engines mysql postgresql opengauss --perm readonly
python load.py --type load --dbname elective --engines mysql postgresql opengauss --path ./data/data/elective/
./batch_load.sh ./data/problems/elective/ elective 4

python load.py --type create --dbname adventureworks --engines mysql postgresql opengauss --perm readonly
先拷贝到容器里面
导入mysql
use adventureworks;
source data/data/adventureworks/adventureworks_mysql.sql
导入postgresql
psql -U teacher -d adventureworks -f "/tmp/adventureworks_postgresql.sql"

./batch_load.sh ./data/problems/adventureworks/ adventureworks 5


python createwdb.py
python load.py --type load --dbname dataset --engines mysql  --path './data/data/nba player/'
python load.py --type load --dbname practisedb --schema dataset --engines postgresql  --path './data/data/nba player/'


python load.py --type load --dbname dataset --engines mysql  --path './data/data/titanic/'
python load.py --type load --dbname practisedb --schema dataset --engines postgresql  --path './data/data/titanic/'

python load.py --type load --dbname dataset --engines mysql  --path ./data/data/WorldHappinessReport/
python load.py --type load --dbname practisedb --schema dataset --engines postgresql  --path ./data/data/WorldHappinessReport/

docker cp test_a.csv my_oj_test:/var/lib/mysql-files/
docker exec -it my_oj_test mysql -uroot -Ddataset -p -e "load data infile '/var/lib/mysql-files/test_a.csv' into table test_a fields terminated by ','  lines terminated by '\n' IGNORE 1 LINES;"

docker exec -it pg_oj_test psql -U postgres -d practisedb -W
\copy dataset.feed_embeddings FROM '/tmp/feed_embeddings.csv' DELIMITER ',' CSV HEADER;

python load.py --type load --dbname dataset --engines mysql  --path ./data/data/onestock/
python load.py --type load --dbname practisedb --schema dataset --engines postgresql  --path ./data/data/onestock/

python load.py --type load --dbname dataset --engines mysql  --path ./data/data/SurnameOrigin/
python load.py --type load --dbname practisedb --schema dataset --engines postgresql  --path ./data/data/SurnameOrigin/

docker cp data/data/astock/astock.csv my_oj_test:/var/lib/mysql-files/
docker exec -it my_oj_test chmod a+r /var/lib/mysql-files/
docker exec -it my_oj_test chown mysql /var/lib/mysql-files/
docker exec -it my_oj_test mysql -uroot -Ddataset -p -e "load data infile '/var/lib/mysql-files/astock.csv' into table astock fields terminated by ','  lines terminated by '\n' IGNORE 1 LINES;"
docker exec -it my_oj_test rm /var/lib/mysql-files/astock.csv
docker cp data/data/astock/astock.csv pg_oj_test:/tmp/
docker exec -it pg_oj_test psql -U postgres -d practisedb -W
\copy dataset.astock FROM '/tmp/astock.csv' DELIMITER ',' CSV HEADER;
