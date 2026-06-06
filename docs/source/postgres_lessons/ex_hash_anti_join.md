# Hash Anti Join

![Hash Anti Join](../../imges/pgadmin/ex_hash_anti_join.svg)

| Example SQL |
| :--- |
| ```sql
SELECT * FROM users u WHERE u.id NOT IN (SELECT user_id FROM orders);
``` |
