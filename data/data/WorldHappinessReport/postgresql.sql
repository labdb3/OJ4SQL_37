create table world_happiness_report_2015
(	region		varchar(30), 
	rank		int,
	happiness	numeric(6,4),
	gdp_per_capita numeric(6,5),
	healthy_life_expectancy	numeric(6,5),
	freedom_to_life_choise		numeric(6,5),
	corruption_perceptions		numeric(6,5),
	generosity	numeric(6,5),
	year		int
);
create table world_happiness_report_2016
(	region		varchar(30), 
	rank		int,
	happiness	numeric(4,3),
	gdp_per_capita numeric(6,5),
	healthy_life_expectancy	numeric(6,5),
	freedom_to_life_choise		numeric(6,5),
	corruption_perceptions		numeric(6,5),
	generosity	numeric(6,5),
	year		int
);
create table world_happiness_report_2017
(	region		varchar(30), 
	rank		int,
	happiness	numeric(10,9),
	gdp_per_capita numeric(10,9),
	healthy_life_expectancy	numeric(10,9),
	freedom_to_life_choise		numeric(10,9),
	generosity	numeric(10,9),
	corruption_perceptions		numeric(10,9),
	year		int

);
create table world_happiness_report_2018
(	rank		int,
	region		varchar(30), 
	happiness	numeric(4,3),
	gdp_per_capita numeric(4,3),
	social_support numeric(4,3),
	healthy_life_expectancy	numeric(4,3),
	freedom_to_life_choise		numeric(4,3),
	generosity	numeric(4,3),
	corruption_perceptions		numeric(4,3),
	year		int
);
create table world_happiness_report_2019
(	rank		int,
	region		varchar(30), 
	happiness	numeric(4,3),
	gdp_per_capita numeric(4,3),
	social_support numeric(4,3),
	healthy_life_expectancy	numeric(4,3),
	freedom_to_life_choise		numeric(4,3),
	generosity	numeric(4,3),
	corruption_perceptions		numeric(4,3),
	year		int
);
