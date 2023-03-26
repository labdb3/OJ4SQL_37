--d 数据准备工作-1
--t mysql
create table  seqNums(sn int);

--d 数据准备工作-2
--t mysql
create table digits (digit int);

--d 数据准备工作-3
--t mysql
insert into  digits (digit)	values (0),(1),(2),(3),(4),(5),(6),(7),(8),(9);

--d 数据准备工作-4
--t mysql
insert into seqNums
(select 		D3.digit * 100 +	D2.digit * 10 +		D1.digit  + 1 
from 		digits as D1	cross join 	digits as D2   cross join 	digits as D3);

--d 数据准备工作查看-5
--t mysql
select * from seqNums;

--d 随机生成中奖门号码
--t mysql
create  table S0(prize_door int);

--d 随机生成选择门号码
--t mysql
create  table S1(prize_door int, your_door int);

--d 随机生成打开门号码
--t mysql
create  table S2(prize_door int, your_door int, open_door int);

--d 计算剩余没有打开门的号码
--t mysql
create table S3(
    prize_door int,
    your_door int,
    open_door int,
    other_door int
);

--d 计算中奖门分别等于选择门以及剩余门的概率
--t mysql
create  table S4(staying_wins int, switching_wins int, trials int);

--d 中奖门数据生成
--t mysql
insert into
    S0 (
        select
            1 + floor(rand() * 10000 + 100) % 3 as prize_door 
        from
            seqNums
        where
            sn <= 1000 
    );

--d 选择门号码生成
--t mysql
insert into
    S1 (
        select
            prize_door,
            1 + floor(rand() * 10000 + 100) % 3 as your_door
        from
            S0
    );

--d 打开门号码生成
--t mysql
insert into
    S2 (
        select
            prize_door,
            your_door,
            case
                when prize_door <> your_door then 6 - prize_door - your_door
                else substring(
                    replace('123', right(your_door, 1), ''),
                    1 + floor(rand() * 10000 + 100) % 2,
                    1
                )
            end as open_door
        from
            S1
    );

--d 没有打开门的号码生成
--t mysql
insert into
    S3 (
        select
            prize_door,
            your_door,
            open_door,
            6 - your_door - open_door as other_door
        from
            S2
    );

--d 计算中奖门分别等于选择门以及剩余门的概率
--t mysql
insert into
    S4 (
        select
            count(
                case
                    when prize_door = your_door then 'Don''t Switch'
                end
            ) as staying_wins,
            count(
                case
                    when prize_door = other_door then 'Do Switch!'
                end
            ) as switching_wins,
            count(*) as trials
        from
            S3
    );

--d 最后结果展示
--t mysql
select
    trials,
    cast(100.0 * staying_wins / trials as decimal(5, 2)) as staying_winsPercent,
    cast(
        100.0 * switching_wins / trials as decimal(5, 2)
    ) as switching_winsPercent
from
    S4;
