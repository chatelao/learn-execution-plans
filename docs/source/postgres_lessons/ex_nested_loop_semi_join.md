# Nested Loop Semi Join

![Nested Loop Semi Join](../../imges/pgadmin/ex_nested_loop_semi_join.svg)

| Example SQL |
| :--- |
| ```sql
SELECT * FROM users u WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);
``` |
