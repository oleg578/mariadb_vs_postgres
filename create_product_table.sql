-- Table creation script for both MariaDB and PostgreSQL
CREATE TABLE product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    -- auto-increment integer
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER NOT NULL
);