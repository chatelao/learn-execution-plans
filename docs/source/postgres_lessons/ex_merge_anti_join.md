# Merge Anti Join

![Merge Anti Join](../../../imges/pgadmin/ex_merge_anti_join.svg)

| Example SQL |
| :--- |
| ```sql
SELECT * FROM users u WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id) ORDER BY u.id;
``` |
