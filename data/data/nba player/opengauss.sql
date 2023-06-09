create table player_data
(	name		varchar(30),
	year_start	int,
	year_end	int,
	position	char(4),
	height		char(8),
	weight		int,
	birth_date	varchar(20),
	college		text
);
create table Players
(	player		varchar(30),
	height		int,
	weight		int,
	college		text,
	born		int,
	birth_city	varchar(40),
	birth_state	varchar(40)
);
create table Seasons_Stats
(	Year 		int,
	Player		varchar(30),
	Pos		char(6),
	Age		smallint,
	TM		char(4),
	G		smallint,
	GS		smallint,
	MP		int,
	PER		numeric(4,1),
	"TS%"		numeric(4,3),
	"3PAr"		numeric(4,3),
	FTr		numeric(4,3),
	"ORB%"		numeric(4,1),
	"DRB%"		numeric(4,1),
	"TRB%"		numeric(4,1),
	"AST%"		numeric(4,1),
	"STL%"		numeric(4,1),
	"BLK%"		numeric(4,1),
	"TOV%"		numeric(4,1),
	"USG%"		numeric(4,1),
	blanl		numeric,
	OWS		numeric(4,1),
	DWS		numeric(4,1),
	WS		numeric(4,1),
	"WS/48"		numeric(4,3),
	blank2		numeric,
	OBPM		numeric(4,1),
	DBPM		numeric(4,1),
	BPM		numeric(4,1),
	VORP		numeric(4,1),
	FG		int,
	FGA		int,
	"FG%"		numeric(4,3),
	"3P"		int,
	"3PA"		int,
	"3P%"		numeric(4,3),
	"2P"		int,
	"2PA"		int,
	"2P%"		numeric(4,3),
	"eFG%"		numeric(4,3),
	FT		int,
	FTA		int,
	"FT%"		numeric(4,3),
	ORB		int,
	DRB		int,
	TRB		int,
	AST		int,
	STL		int,
	BLK		int,
	TOV		int,
	PF		int,
	PTS		int
);
