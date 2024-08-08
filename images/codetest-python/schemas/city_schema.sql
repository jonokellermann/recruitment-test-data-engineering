drop table if exists city;

create table `city` (
  `city_id` varchar(80) not null,
  `city` varchar(80),
  `county` varchar(80),
  `country_id` varchar(80),
  primary key (`city_id`)
);
