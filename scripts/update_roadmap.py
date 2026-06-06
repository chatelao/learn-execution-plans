import re
from datetime import datetime

roadmap_path = "ROADMAP.md"
with open(roadmap_path, 'r') as f:
    content = f.read()

today = datetime.now().strftime("%Y-%m-%d")

# Find the PostgreSQL section
start_marker = "Produce PostgreSQL execution plan constructs lessons ⏳"
end_marker = "- [ ] Create interactive optimization exercises ⏳"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Markers not found")
    exit(1)

section = content[start_idx:end_idx]

# Update the main task
section = section.replace(start_marker, f"Produce PostgreSQL execution plan constructs lessons ✅ ({today})")

# Update subtasks
updated_section = re.sub(r"- \[ \] (Lesson: .*? ⏳)", r"- [x] \1", section)
updated_section = updated_section.replace(" ⏳", f" ✅ ({today})")

new_content = content[:start_idx] + updated_section + content[end_idx:]

with open(roadmap_path, 'w') as f:
    f.write(new_content)

print("Updated ROADMAP.md")
