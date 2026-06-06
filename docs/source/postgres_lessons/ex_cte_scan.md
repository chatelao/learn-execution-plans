# Cte Scan

![Cte Scan](../../../imges/pgadmin/ex_cte_scan.svg)

| Example SQL |
| :--- |
| ```sql WITH regional_sales AS (SELECT region, SUM(amount) AS total_sales FROM orders GROUP BY region) SELECT * FROM regional_sales;``` |
