/* A SQL script that creates 'places' table with defined schemas. */
drop table if exists places;

create table `places` (
  `city` varchar(80),
  `county` varchar(80),
  `country` varchar(80) not null,
  primary key (`city`)
);
