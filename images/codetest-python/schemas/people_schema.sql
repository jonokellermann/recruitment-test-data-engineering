/* A SQL script that creates 'people' table with defined schemas. */
drop table if exists people;

create table `people` (
  `person_id` varchar(80) not null,
  `given_name` varchar(80),
  `family_name` varchar(80),
  `date_of_birth` date,
  `place_of_birth` varchar(100),
  primary key (`person_id`)
);
