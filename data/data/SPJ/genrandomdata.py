import csv
from collections import defaultdict
from random import choice, randint

SNUMS = 500
PNUMS = 500
JNUMS = 500
SPJNUMS = 1000
'''
S(SNO, SNAME, STATUS, CITY)
P(PNO, PNAME, COLOR, WEIGHT, CITY)
J(JNO, JNAME,CITY)
SPJ(SNO, PNO, JNO, QTY, PRICE)
'''
cities = ['北京', '上海', '广州', '南京', '天津', '重庆']
colors = ['红色', '黄色', '黑色', '蓝色', '绿色']
statuses = [10, 20, 30]
xings = ['赵', '钱', '孙', '李']
parts = ['剪刀', '石头', '布', '螺丝', 'CPU']
jnames = ['南京基地', '面壁', '智子', '古筝计划', '水滴']
srows = []
for s_counter in range(SNUMS):
    sno = 'S'+str(s_counter)
    sname = choice(xings)+str(s_counter)
    status = choice(statuses)
    city = choice(cities)
    srows.append([sno, sname, status, city])
# 求只向与自己位于相同城市的工程供应零件的供应商姓名。
srows += [['S'+str(SNUMS), '章北海', 10, '北京'],
          ['S'+str(SNUMS+1), '叶文洁', 10, '南京']]
prows = []
for p_counter in range(PNUMS):
    pno = 'P'+str(p_counter)
    pname = choice(parts)+str(p_counter % (PNUMS//10))
    color = choice(colors)
    weight = randint(1, 100)
    city = choice(cities)
    prows.append([pno, pname, color, weight, city])

city_jnos = defaultdict(list)
jrows = []
for j_counter in range(JNUMS):
    jno = 'J'+str(j_counter)
    jname = choice(jnames)+str(j_counter)
    city = choice(cities)
    city_jnos[city].append(jno)
    jrows.append([jno, jname, city])

spjrows = []
for spj_counter in range(SPJNUMS):
    sno = 'S'+str(randint(0, SNUMS-1))
    pno = 'P'+str(randint(0, PNUMS-1))
    jno = 'J'+str(randint(0, JNUMS-1))
    qty = randint(1, 100)
    price = randint(1, 10000)
    spjrows.append([sno, pno, jno, qty, price])

spjrows += [['S'+str(SNUMS), 'P'+str(randint(0, PNUMS-1)), choice(city_jnos['北京']), 51, 1000],
            ['S'+str(SNUMS+1), 'P'+str(randint(0, PNUMS-1)), choice(city_jnos['南京']), 55, 1200]]

# 求供应了所有零件的供应商姓名。
sno_all = 'S'+str(randint(0, SNUMS-1))
sno_all_pnos = [r[1] for r in spjrows if r[0] == sno_all]
for p_counter in range(PNUMS):
    pno = 'P'+str(p_counter)
    if pno not in sno_all_pnos:
        qty = randint(1, 100)
        price = randint(1, 10000)
        jno = 'J'+str(randint(0, JNUMS-1))
        spjrows.append([sno_all, pno, jno, qty, price])


with open('s.csv', 'wt') as f:
    w = csv.writer(f, quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
    w.writerows(srows)

with open('p.csv', 'wt') as f:
    w = csv.writer(f, quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
    w.writerows(prows)

with open('j.csv', 'wt') as f:
    w = csv.writer(f, quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
    w.writerows(jrows)

with open('spj.csv', 'wt') as f:
    w = csv.writer(f, quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
    w.writerows(spjrows)
