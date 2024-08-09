
CREATE TABLE people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    city_of_birth VARCHAR(100)
);

CREATE TABLE places (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100),
    county VARCHAR(100),
    country VARCHAR(100)
);



SELECT * FROM people;
SELECT * FROM places;