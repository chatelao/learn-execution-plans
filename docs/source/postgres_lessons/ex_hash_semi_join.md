# Hash Semi Join

![Hash Semi Join](../../../imges/pgadmin/ex_hash_semi_join.svg)

| Example SQL |
| :--- |
| ```sql SELECT * FROM users u WHERE u.id IN (SELECT user_id FROM orders);``` |
