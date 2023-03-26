drop table if exists movies;

drop table if exists movieGenres;

drop table if exists ratings;

drop table if exists tags;

create table movies(movieId int, title text);

create table movieGenres(movieId int, genres varchar(50));

create table ratings(
    userId int,
    movieId int,
    rating numeric,
    timestamp date
);

create table tags(
    userId int,
    movieId int,
    tag text,
    timestamp date
);