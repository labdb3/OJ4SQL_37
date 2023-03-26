create table titanic_gender_submission
(	PassengerId	int,
	Survived	int
);

create table titanic_test
(	PassengerId	int,
	Pclass		smallint,
	Name		text,
	Sex		char(8),
	Age		numeric(4,1),
	SibSp		smallint,
	Parch		smallint,
	Ticket		varchar(20),
	Fare		numeric(8,4),
	Cabin		varchar(20),
	Embarked	char(1)
);
create table titanic_train
(	PassengerId	int,
	Survived	smallint,
	Pclass		smallint,
	Name		text,
	Sex		char(8),
	Age		numeric(4,1),
	SibSp		smallint,
	Parch		smallint,
	Ticket		varchar(20),
	Fare		numeric(8,4),
	Cabin		varchar(20),
	Embarked	char(1)
);
