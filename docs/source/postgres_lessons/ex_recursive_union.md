# Recursive Union

![Recursive Union](../../../imges/pgadmin/ex_recursive_union.svg)

| Example SQL |
| :--- |
| ```sql WITH RECURSIVE t(n) AS (VALUES (1) UNION ALL SELECT n+1 FROM t WHERE n < 100) SELECT sum(n) FROM t;``` |
