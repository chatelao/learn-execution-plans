CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL
);

INSERT INTO users (username) SELECT 'user' || i FROM generate_series(1, 100) i;
