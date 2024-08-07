DROP TABLE IF EXISTS places;

CREATE TABLE places (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(255),
    county VARCHAR(255),
    country VARCHAR(255),
    UNIQUE (city, county, country)
);

DROP TABLE IF EXISTS people;

CREATE TABLE people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    given_name VARCHAR(255),
    family_name VARCHAR(255),
    date_of_birth DATE,
    place_of_birth INT,
    FOREIGN KEY (place_of_birth) REFERENCES places(id)
);