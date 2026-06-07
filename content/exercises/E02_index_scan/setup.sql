CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INT
);

CREATE INDEX idx_employees_dept ON employees(department_id);

INSERT INTO employees (name, department_id)
SELECT 'Employee ' || i, (i % 10) + 1
FROM generate_series(1, 1000) i;

ANALYZE employees;
