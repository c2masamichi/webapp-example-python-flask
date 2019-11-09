SCHEMA_STATEMENTS = [
    'DROP TABLE IF EXISTS user',
    'DROP TABLE IF EXISTS post',

    'CREATE TABLE user ('
    '  id INT PRIMARY KEY AUTO_INCREMENT,'
    '  username VARCHAR(20) UNIQUE NOT NULL,'
    '  password VARCHAR(200) NOT NULL'
    ')',

    'CREATE TABLE post ('
    '  id INT PRIMARY KEY AUTO_INCREMENT,'
    '  title VARCHAR(100) NOT NULL,'
    '  body TEXT NOT NULL,'
    '  created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP'
    ')',
]
