import os
import re

lessons_data = {
    "Scan": "SELECT * FROM users;",
    "Index Scan": "SELECT * FROM users WHERE id = 1;",
    "Index Only Scan": "SELECT id FROM users WHERE id = 1;",
    "Nested": "SELECT * FROM users u JOIN orders o ON u.id = o.user_id;",
    "Join": "SELECT * FROM users u JOIN orders o ON u.id = o.user_id;",
    "Hash": "SELECT * FROM users u JOIN orders o ON u.id = o.user_id;",
    "Merge": "SELECT * FROM users u JOIN orders o ON u.id = o.user_id ORDER BY u.id;",
    "Bmp Index": "SELECT * FROM users WHERE id < 10 OR id > 100;",
    "Bmp Heap": "SELECT * FROM users WHERE id < 10 OR id > 100;",
    "Bmp And": "SELECT * FROM users WHERE id > 10 AND age > 20;",
    "Bmp Or": "SELECT * FROM users WHERE id < 10 OR age > 60;",
    "Sort": "SELECT * FROM users ORDER BY name;",
    "Aggregate": "SELECT COUNT(*) FROM users;",
    "Group": "SELECT department, COUNT(*) FROM employees GROUP BY department;",
    "Unique": "SELECT DISTINCT name FROM users;",
    "Limit": "SELECT * FROM users LIMIT 10;",
    "Insert": "INSERT INTO users (name) VALUES ('John');",
    "Update": "UPDATE users SET name = 'Jane' WHERE id = 1;",
    "Delete": "DELETE FROM users WHERE id = 1;",
    "Lock Rows": "SELECT * FROM users WHERE id = 1 FOR UPDATE;",
    "Materialize": "SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);",
    "Result": "SELECT 1;",
    "Cte Scan": "WITH regional_sales AS (SELECT region, SUM(amount) AS total_sales FROM orders GROUP BY region) SELECT * FROM regional_sales;",
    "Worktable Scan": "WITH RECURSIVE t(n) AS (VALUES (1) UNION ALL SELECT n+1 FROM t WHERE n < 100) SELECT sum(n) FROM t;",
    "Subplan": "SELECT name, (SELECT MAX(amount) FROM orders WHERE user_id = users.id) FROM users;",
    "Append": "SELECT * FROM t1 UNION ALL SELECT * FROM t2;",
    "Merge Append": "SELECT * FROM p1 UNION ALL SELECT * FROM p2 ORDER BY id;",
    "Recursive Union": "WITH RECURSIVE t(n) AS (VALUES (1) UNION ALL SELECT n+1 FROM t WHERE n < 100) SELECT sum(n) FROM t;",
    "Nested Loop Semi Join": "SELECT * FROM users u WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);",
    "Nested Loop Anti Join": "SELECT * FROM users u WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);",
    "Hash Semi Join": "SELECT * FROM users u WHERE u.id IN (SELECT user_id FROM orders);",
    "Hash Anti Join": "SELECT * FROM users u WHERE u.id NOT IN (SELECT user_id FROM orders);",
    "Merge Semi Join": "SELECT * FROM users u WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id) ORDER BY u.id;",
    "Merge Anti Join": "SELECT * FROM users u WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id) ORDER BY u.id;",
    "Gather Merge": "SELECT * FROM big_table ORDER BY id;",
    "Gather Motion": "SELECT * FROM big_table;",
    "Window Aggregate": "SELECT name, SUM(salary) OVER (PARTITION BY dept) FROM employees;",
    "Projectset": "SELECT generate_series(1,10);",
    "Foreign Scan": "SELECT * FROM foreign_table;",
    "Tid Scan": "SELECT * FROM users WHERE ctid = '(0,1)';",
    "Values Scan": "VALUES (1, 'one'), (2, 'two');",
    "Named Tuplestore Scan": "-- Internal PostgreSQL node, often used in PL/pgSQL functions",
    "Table Func Scan": "SELECT * FROM json_to_recordset('[{\"a\":1,\"b\":\"foo\"}]') as x(a int, b text);",
    "Seek": "SELECT * FROM users WHERE id = 1; -- Often synonymous with Index Scan in some dialects",
    "Setop": "SELECT id FROM t1 EXCEPT SELECT id FROM t2;",
    "Hash Setop Unknown": "SELECT id FROM t1 INTERSECT SELECT id FROM t2;",
    "Hash Setop Except": "SELECT id FROM t1 EXCEPT SELECT id FROM t2;",
    "Hash Setop Except All": "SELECT id FROM t1 EXCEPT ALL SELECT id FROM t2;",
    "Hash Setop Intersect": "SELECT id FROM t1 INTERSECT SELECT id FROM t2;",
    "Hash Setop Intersect All": "SELECT id FROM t1 INTERSECT ALL SELECT id FROM t2;",
    "Citus": "SELECT * FROM distributed_table;",
    "Citus Worker Task": "-- Citus internal task execution",
    "Citus Distributed One Of One": "SELECT * FROM distributed_table WHERE id = 1;",
    "Citus Distributed One Of Many": "SELECT * FROM distributed_table WHERE id > 100;",
    "Broadcast Motion": "-- Greenplum/Citus data movement",
    "Redistribute Motion": "-- Greenplum/Citus data movement",
    "Unknown": "-- Unknown plan node"
}

def generate_lessons():
    roadmap_path = "ROADMAP.md"
    output_dir = "docs/source/postgres_lessons"
    os.makedirs(output_dir, exist_ok=True)

    with open(roadmap_path, 'r') as f:
        content = f.read()

    # Extract PostgreSQL lessons section
    pg_section_match = re.search(r"Produce PostgreSQL execution plan constructs lessons [⏳✅](.*?)(?=- \[ \] Create interactive)", content, re.DOTALL)
    if not pg_section_match:
        print("Could not find PostgreSQL lessons section in ROADMAP.md")
        return

    pg_section = pg_section_match.group(1)
    lessons = re.findall(r"- \[[x ]\] Lesson: (.*?) \((.*?)\) [⏳✅]", pg_section)

    for title, icon in lessons:
        filename = icon.replace(".svg", ".md")
        filepath = os.path.join(output_dir, filename)
        sql_example = lessons_data.get(title, "-- Example SQL not provided")

        md_content = f"""# {title}

![{title}](../../imges/pgadmin/{icon})

| Example SQL |
| :--- |
| ```sql
{sql_example}
``` |
"""
        with open(filepath, 'w') as f:
            f.write(md_content)
        print(f"Generated {filepath}")

if __name__ == "__main__":
    generate_lessons()
