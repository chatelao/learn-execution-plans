import os
import re

lessons_data = {
    "Table Access Full": "SELECT * FROM users;",
    "Index Unique Scan": "SELECT * FROM users WHERE id = 1;",
    "Index Range Scan": "SELECT * FROM users WHERE id < 10;",
    "Index Full Scan": "SELECT id FROM users ORDER BY id;",
    "Index Fast Full Scan": "SELECT COUNT(id) FROM users;",
    "Index Skip Scan": "SELECT * FROM users WHERE status = 'ACTIVE'; -- where (gender, status) is indexed",
    "Table Access By Index Rowid": "SELECT * FROM users WHERE id = 1;",
    "Nested Loops": "SELECT * FROM users u JOIN orders o ON u.id = o.user_id;",
    "Hash Join": "SELECT * FROM users u JOIN orders o ON u.id = o.user_id;",
    "Merge Join": "SELECT * FROM users u JOIN orders o ON u.id = o.user_id ORDER BY u.id;",
    "Sort Aggregate": "SELECT COUNT(*) FROM users;",
    "Hash Unique": "SELECT DISTINCT name FROM users;",
    "View": "SELECT * FROM user_orders_view;",
    "Union-All": "SELECT * FROM t1 UNION ALL SELECT * FROM t2;",
    "Filter": "SELECT * FROM users WHERE id > 10 AND id < 20;",
    "Bitmap Index Operations": "SELECT * FROM users WHERE status = 'ACTIVE' AND region = 'EAST';",
    "Partitioning Operations": "SELECT * FROM partitioned_table WHERE part_key = 1;",
    "Window Functions": "SELECT name, RANK() OVER (ORDER BY salary DESC) FROM employees;",
    "Hierarchical Queries (Connect By)": "SELECT * FROM employees START WITH manager_id IS NULL CONNECT BY PRIOR id = manager_id;"
}

def generate_lessons():
    roadmap_path = "ROADMAP.md"
    output_dir = "docs/source/oracle_lessons"
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(roadmap_path):
        print(f"Roadmap file not found: {roadmap_path}")
        return

    with open(roadmap_path, 'r') as f:
        content = f.read()

    # Extract Oracle lessons section - more robust regex
    oracle_section_match = re.search(r"Produce Oracle execution plan constructs lessons.*?\n(.*?)(?=\n- \[x\] Produce PostgreSQL)", content, re.DOTALL)
    if not oracle_section_match:
        print("Could not find Oracle lessons section in ROADMAP.md")
        return

    oracle_section = oracle_section_match.group(1)
    # Looking for lessons regardless of their status, we'll filter by to_generate
    lessons = re.findall(r"- \[.\] Lesson: (.*?) [⏳✅🚧]", oracle_section)

    # Lessons we want to ensure are generated
    to_generate = [
        "Table Access Full",
        "Index Unique Scan",
        "Index Range Scan",
        "Index Full Scan",
        "Index Fast Full Scan",
        "Index Skip Scan",
        "Table Access By Index Rowid",
        "Nested Loops",
        "Hash Join",
        "Merge Join"
    ]

    for title in lessons:
        title = title.strip()
        if title not in to_generate:
            continue

        filename = title.lower().replace(" ", "_").replace("-", "_") + ".md"
        filepath = os.path.join(output_dir, filename)
        sql_example = lessons_data.get(title, "-- Example SQL not provided")

        md_content = f"""# {title}

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
