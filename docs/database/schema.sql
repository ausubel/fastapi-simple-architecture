CREATE TABLE users (
    id INTEGER NOT NULL,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    dateOfBirth DATE NOT NULL,
    createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
)

-- CREATE TABLE roles(
--     id INTEGER NOT NULL,
--     name VARCHAR(255) NOT NULL,
--     PRIMARY KEY (id)
-- )

-- CREATE TABLE user_roles(
--     userId INTEGER NOT NULL,
--     roleId INTEGER NOT NULL,
--     PRIMARY KEY (userId, roleId),
--     FOREIGN KEY (userId) REFERENCES users(id),
--     FOREIGN KEY (roleId) REFERENCES roles(id)
-- )
