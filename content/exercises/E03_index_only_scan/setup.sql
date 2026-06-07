CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT,
    salary DECIMAL
);

INSERT INTO employees (name, department, salary)
SELECT
    'employee' || i,
    CASE WHEN i % 3 = 0 THEN 'HR' WHEN i % 3 = 1 THEN 'IT' ELSE 'Sales' END,
    (random() * 5000 + 3000)::decimal
FROM generate_series(1, 1000) i;

-- Create an index that covers common queries to encourage Index Only Scan
CREATE INDEX idx_employees_dept_name ON employees(department, name);
ANALYZE employees;
