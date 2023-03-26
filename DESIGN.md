在加入问题前应该对数据库进行增加或新建
一个问题属于至少一个组，有一个评测数据库，有标准答案
组可以属于另一个组

User(uid, nickname, name, accountname, studentid, passwd)

Problem(编号, 描述, 题目, mysql, postgresql, opengauss, 裁判, 评测数据库)
Problem(pid, description, title, mysql, postgresql, opengauss, judge, testdb)
judge: 只读有序评测ordered，只读无序评测unordered，题目自定义评测custom

Group(gid, description, father, type, perm, recordsubmission)
perm: 开放提交O，只读不能提交R，不能显示组中内容U，隐藏组本身H
type: 不评测不显示答案，不评测显示答案，评测不显示答案，评测显示答案

UserGroup(uid, gid)
ProblemGroup(pid, gid)


Practise(pid)

重做提交记录
