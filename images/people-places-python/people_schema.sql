/* A SQL script that creates 'people' table with defined schemas. */
drop table if exists people;

create table `people` (
  `given_name` varchar(80),
  `family_name` varchar(80),
  `date_of_birth` date,
  `place_of_birth` varchar(100),
  `id` varchar(36) not null,
  primary key (`id`)
);
