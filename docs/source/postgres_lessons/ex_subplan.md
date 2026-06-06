# Subplan

![Subplan](../../imges/pgadmin/ex_subplan.svg)

| Example SQL |
| :--- |
| ```sql
SELECT name, (SELECT MAX(amount) FROM orders WHERE user_id = users.id) FROM users;
``` |
