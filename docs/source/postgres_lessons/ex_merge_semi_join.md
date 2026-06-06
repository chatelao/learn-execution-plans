# Merge Semi Join

![Merge Semi Join](../../../imges/pgadmin/ex_merge_semi_join.svg)

| Example SQL |
| :--- |
| ```sql
SELECT * FROM users u WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id) ORDER BY u.id;
``` |
