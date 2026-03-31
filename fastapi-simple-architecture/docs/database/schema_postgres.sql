-- TABLES
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    dateOfBirth DATE NOT NULL,
    roleId INTEGER NOT NULL REFERENCES roles(id),
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    userId INTEGER NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES users(id) ON DELETE CASCADE
);
-- INSERTS
INSERT INTO roles (name, description)
VALUES ('admin', 'Administrator'),
    ('user', 'Standard user');
INSERT INTO users (
        firstName,
        lastName,
        email,
        password,
        dateOfBirth,
        roleId
    )
VALUES (
        'admin name',
        'admin lastname',
        'admin@admin.com',
        '$2b$12$i0u4DyNJBBuXhlT0j0u51.9MtyNEhNYoC/vXUYmoYxUxEBMAXZjhW',
        -- borntofeel
        '2000-01-01',
        1
    );

-- Test data for Pact contract testing
INSERT INTO users (
        id,
        firstName,
        lastName,
        email,
        password,
        dateOfBirth,
        roleId,
        createdAt,
        updatedAt
    )
VALUES (
        2,
        'Test',
        'User',
        'test@example.com',
        '$2b$12$xDhx93lQIPN3pwxwZjHxLuzaL/4Eu5VGEInOWk5hGGbGtHDg7dR0O',
        -- password: password123
        '1990-01-01',
        2,
        '2024-01-01 00:00:00',
        '2024-01-01 00:00:00'
    );

INSERT INTO posts (
        title,
        content,
        userId,
        createdAt,
        updatedAt
    )
VALUES (
        'Pact Title',
        'Pact Content',
        2,
        '2024-01-01 00:00:00',
        '2024-01-01 00:00:00'
    );