TEST_DATA_STATEMENTS = [
    'INSERT INTO user (role, username, password)'
    ' VALUES'
    '  ("administrator", "user-admin01", "pbkdf2:sha256:150000$uruHRLDK$e7291b6efdd7439668e47fbd509e9fadad0cd7511073fb47d9846161c9605e20"),'
    '  ("editor", "user-editor01", "pbkdf2:sha256:150000$uruHRLDK$e7291b6efdd7439668e47fbd509e9fadad0cd7511073fb47d9846161c9605e20"),'
    '  ("author", "user-author01", "pbkdf2:sha256:150000$uruHRLDK$e7291b6efdd7439668e47fbd509e9fadad0cd7511073fb47d9846161c9605e20")',

    'INSERT INTO entry (author_id, title, body, created)'
    ' VALUES'
    '  (1, "Test Title 1", "This body is test.", "2019-01-01 00:00:00"),'
    '  (2, "Test Title 2", "Test Test Test Test", "2019-01-01 12:30:45"),'
    '  (3, "Test Title 3", "Test Test Test Test", "2019-01-02 08:20:01")'
]
