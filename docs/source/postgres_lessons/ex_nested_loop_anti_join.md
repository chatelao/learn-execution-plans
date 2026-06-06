# Nested Loop Anti Join

![Nested Loop Anti Join](../../../imges/pgadmin/ex_nested_loop_anti_join.svg)

| Example SQL |
| :--- |
| ```sql SELECT * FROM users u WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);``` |
