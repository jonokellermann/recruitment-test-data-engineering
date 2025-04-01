
DROP TABLE IF EXISTS people;

DROP TABLE IF EXISTS places;


CREATE TEMPORARY TABLE IF NOT EXISTS people (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  given_name VARCHAR (50),
  family_name VARCHAR (50),
  date_of_birth DATE,
  place_of_birth VARCHAR (125),
  INDEX (place_of_birth)
);


CREATE TEMPORARY TABLE IF NOT EXISTS places (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  city VARCHAR (50),
  county VARCHAR (50),
  country VARCHAR (50),
  INDEX (city, country)
);
