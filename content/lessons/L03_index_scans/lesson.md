# Index Scans in PostgreSQL

An Index Scan is used when PostgreSQL can use an index to find the rows required by a query. Instead of reading the entire table, it first looks up the values in the index and then retrieves only the matching rows from the table.

![Index Scan](../../../imges/pgadmin/ex_index_scan.svg)

### When is an Index Scan used?
- When there is a filter (WHERE clause) on a column that has an index.
- When only a small fraction of the table's rows are expected to match the filter.
- When the cost of using the index plus retrieving the rows is less than a full table scan.

Example SQL:
```sql
SELECT * FROM users WHERE id = 10;
```
