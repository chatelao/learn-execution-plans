# Window Aggregate

![Window Aggregate](../../../imges/pgadmin/ex_window_aggregate.svg)

| Example SQL |
| :--- |
| ```sql
SELECT name, SUM(salary) OVER (PARTITION BY dept) FROM employees;
``` |
