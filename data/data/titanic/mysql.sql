create table titanic_gender_submission
(	PassengerId	int,
	Survived	int
);

create table titanic_test
(	PassengerId	int,
	Pclass		tinyint,
	Name		text,
	Sex		char(8),
	Age		float(4,1),
	SibSp		tinyint,
	Parch		tinyint,
	Ticket		varchar(20),
	Fare		float(8,4),
	Cabin		varchar(20),
	Embarked	char(1)
);
create table titanic_train
(	PassengerId	int,
	Survived	tinyint,
	Pclass		tinyint,
	Name		text,
	Sex		char(8),
	Age		float(4,1),
	SibSp		tinyint,
	Parch		tinyint,
	Ticket		varchar(20),
	Fare		float(8,4),
	Cabin		varchar(20),
	Embarked	char(1)
);
