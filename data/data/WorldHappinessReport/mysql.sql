create table world_happiness_report_2015
(	region		varchar(30), 
	`rank`		int,
	happiness	float(6,4),
	gdp_per_capita float(6,5),
	healthy_life_expectancy	float(6,5),
	freedom_to_life_choise		float(6,5),
	corruption_perceptions		float(6,5),
	generosity	float(6,5),
	year		int
);
create table world_happiness_report_2016
(	region		varchar(30), 
	`rank`		int,
	happiness	float(4,3),
	gdp_per_capita float(6,5),
	healthy_life_expectancy	float(6,5),
	freedom_to_life_choise		float(6,5),
	corruption_perceptions		float(6,5),
	generosity	float(6,5),
	year		int
);
create table world_happiness_report_2017
(	region		varchar(30), 
	`rank`		int,
	happiness	float(10,9),
	gdp_per_capita float(10,9),
	healthy_life_expectancy	float(10,9),
	freedom_to_life_choise		float(10,9),
	generosity	float(10,9),
	corruption_perceptions		float(10,9),
	year		int

);
create table world_happiness_report_2018
(	`rank`		int,
	region		varchar(30), 
	happiness	float(4,3),
	gdp_per_capita float(4,3),
	social_support float(4,3),
	healthy_life_expectancy	float(4,3),
	freedom_to_life_choise		float(4,3),
	generosity	float(4,3),
	corruption_perceptions		float(4,3),
	year		int
);
create table world_happiness_report_2019
(	`rank`		int,
	region		varchar(30), 
	happiness	float(4,3),
	gdp_per_capita float(4,3),
	social_support float(4,3),
	healthy_life_expectancy	float(4,3),
	freedom_to_life_choise		float(4,3),
	generosity	float(4,3),
	corruption_perceptions		float(4,3),
	year		int
);
