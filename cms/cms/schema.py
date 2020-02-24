SCHEMA_STATEMENTS = [
    'DROP TABLE IF EXISTS entry',
    'DROP TABLE IF EXISTS user',

    'CREATE TABLE user ('
    ' id INT PRIMARY KEY AUTO_INCREMENT,'
    ' username VARCHAR(20) UNIQUE NOT NULL,'
    ' password VARCHAR(200) NOT NULL'
    ')',

    'CREATE TABLE entry ('
    ' id INT PRIMARY KEY AUTO_INCREMENT,'
    ' author_id INT,'
    ' title VARCHAR(100) NOT NULL,'
    ' body TEXT NOT NULL,'
    ' created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,'
    ' FOREIGN KEY (author_id) REFERENCES user (id) ON DELETE SET NULL'
    ')',
]
