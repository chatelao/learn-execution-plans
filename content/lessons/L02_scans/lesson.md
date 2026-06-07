# Scans in PostgreSQL

A scan operation is how PostgreSQL reads data from a table. The most basic type is a Sequential Scan.

![Scan](../../../imges/pgadmin/ex_scan.svg)

### Sequential Scan (Seq Scan)
A Sequential Scan reads the entire table from beginning to end. It is typically used when:
- The table is small.
- A large portion of the table needs to be read.
- No suitable index is available for the query's filter conditions.

Example SQL:
```sql
SELECT * FROM users;
```
