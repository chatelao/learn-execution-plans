# Table Func Scan

![Table Func Scan](../../../imges/pgadmin/ex_table_func_scan.svg)

| Example SQL |
| :--- |
| ```sql
SELECT * FROM json_to_recordset('[{"a":1,"b":"foo"}]') as x(a int, b text);
``` |
