SCHEMA_STATEMENTS = [
    'DROP TABLE IF EXISTS product;',
    'CREATE TABLE product ('
    ' id INT PRIMARY KEY AUTO_INCREMENT,'
    ' name VARCHAR(20) UNIQUE NOT NULL,'
    ' price INT NOT NULL'
    ');',
]
