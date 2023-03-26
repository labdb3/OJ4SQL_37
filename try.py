from db.conn import trainee_conn

sql = '''select msalary.avg_salary, fsalary.avg_salary, msalary.avg_salary-fsalary.avg_salary
from
(
        select sum(salary/360*datediff(if(to_date='9999-01-01','2003-08-01',to_date),from_date))/sum(datediff(if(to_date='9999-01-01','2003-08-01',to_date),from_date)) as avg_salary
        from employees natural join salaries
        where gender='M'
        ) msalary,
(
        select sum(salary/360*datediff(if(to_date='9999-01-01','2003-08-01',to_date),from_date))/sum(datediff(if(to_date='9999-01-01','2003-08-01',to_date),from_date)) as avg_salary
        from employees natural join salaries
        where gender='F'
        ) fsalary'''
with trainee_conn('mysql','employees') as c:
    c.execute(sql)
    r = c.fetchall()
    print(r)


sql=''' select avg(salary) from salaries '''
with trainee_conn('postgresql','employees') as c:
    c.execute(sql)
    r = c.fetchall()
    print(r)

with trainee_conn('mysql','employees') as c:
    c.execute(sql)
    r = c.fetchall()
    print(r)

with trainee_conn('opengauss','employees') as c:
    c.execute(sql)
    r = c.fetchall()
    print(r)

sql='''SELECT dept_emp.emp_no, dept_manager.emp_no FROM dept_emp JOIN dept_manager ON dept_emp.dept_no = dept_manager.dept_no
WHERE exists (
    select * from 
        (select * from salaries where salaries.emp_no = dept_emp.emp_no) s1, 
            (select * from salaries where salaries.emp_no = dept_manager.emp_no) s2
                where (s1.salary > s2.salary) AND (GREATEST(dept_emp.from_date, dept_manager.from_date, s1.from_date, s2.from_date) <= LEAST(dept_emp.to_date, dept_manager.to_date, s1.to_date, s2.to_date))
                )
                ORDER BY dept_emp.emp_no, dept_manager.emp_no
                LIMIT 10;'''
sql = 'select UnitPrice,LineTotal from salesorderdetail limit 10'
with trainee_conn('mysql','adventureworks') as c:
    c.execute(sql)
    r = c.fetchall()
    print(r)
sql = 'select "UnitPrice","LineTotal" from salesorderdetail limit 10'
with trainee_conn('postgresql','adventureworks') as c:
    c.execute(sql)
    r = c.fetchall()
    print(r)
