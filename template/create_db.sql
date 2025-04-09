CREATE DATABASE test_db;
USE test_db;
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL
);
INSERT INTO products (name, description, price)
VALUES ('TV', 'LCD 40 Inch', 749.99),
    (
        'Laptop',
        '2x2.6 GHz CPU; 6GB RAM; HD Graphics',
        699.99
    ),
    ('Smartphone', '6.55\" HD+, 5G', 1349.90),
    (
        'Keyboard',
        'Full-size Layout, Mechanical',
        99.00
    );