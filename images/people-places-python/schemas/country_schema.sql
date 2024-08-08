drop table if exists country;

create table `country` (
  `country_id` varchar(80) not null,
  `country_name` varchar(80),
  primary key (`country_id`)
);
