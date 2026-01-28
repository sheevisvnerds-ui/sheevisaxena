import re
import os

file_path = r"c:\Users\Dell\Desktop\ScrapeWale\templates\core\agent_dashboard.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Name
# Pattern: {{ \n whitespace pickup.customer.name...
# We use a broad regex to catch the split tag
content = re.sub(
    r'\{\{\s*pickup\.customer\.name\|default:pickup\.customer\.username\s*\}\}', 
    '{{ pickup.customer.name|default:pickup.customer.username }}', 
    content
)

# Fix Phone
# Pattern: }} \n whitespace pickup.customer.phone...
content = re.sub(
    r'\{\{\s*pickup\.customer\.phone\|default:"N/A"\s*\}\}', 
    '{{ pickup.customer.phone|default:"N/A" }}', 
    content
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed agent_dashboard.html")
