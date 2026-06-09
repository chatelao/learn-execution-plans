CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    dept_id INTEGER REFERENCES departments(id)
);

INSERT INTO departments (name) VALUES ('HR'), ('Engineering'), ('Sales');
INSERT INTO employees (name, dept_id) VALUES
('Alice', 1), ('Bob', 2), ('Charlie', 2), ('David', 3);
