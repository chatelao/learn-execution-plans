# Materialize

![Materialize](../../../imges/pgadmin/ex_materialize.svg)

| Example SQL |
| :--- |
| ```sql
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);
``` |
