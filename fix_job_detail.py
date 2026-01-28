import re
import os

file_path = r"c:\Users\Dell\Desktop\ScrapeWale\templates\core\agent_job_detail.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix the HTML Rate Display
# Pattern: ₹{{ \n whitespace ... }}/kg
# We replace it with the single-line version
# This regex looks for the split pattern specifically
content = re.sub(
    r'₹\{\{\s*pickup\.scrap_category\.rate_per_kg\s*\}\}/kg', 
    '₹{{ pickup.scrap_category.rate_per_kg }}/kg', 
    content
)
# Also try capturing the whitespace version if the above doesn't catch it
content = re.sub(
    r'₹\{\{\s+pickup\.scrap_category\.rate_per_kg\s+\}\}/kg', 
    '₹{{ pickup.scrap_category.rate_per_kg }}/kg', 
    content
)


# 2. Fix the JS Rate Variable
# Pattern: const ratePerKg = {{ ... \n ... }}
content = re.sub(
    r'const ratePerKg = \{\{\s*pickup\.scrap_category\.rate_per_kg\|default:\s*"0"\s*\}\};', 
    'const ratePerKg = {{ pickup.scrap_category.rate_per_kg|default:"0" }};', 
    content,
    flags=re.DOTALL
)

# Broaden regex for the JS one since it had a newline in the "before" state
content = re.sub(
    r'const ratePerKg = \{\{\s*pickup\.scrap_category\.rate_per_kg\|default:\s*"0"\s*\n\s*\}\};', 
    'const ratePerKg = {{ pickup.scrap_category.rate_per_kg|default:"0" }};', 
    content
)


# 3. Add Estimated Weight if not present
# We look for the "Scrap Category" col-12 div and inject "Est Weight" after it if it's not there
est_weight_html = """
                <div class="col-6">
                    <small class="text-muted">Est. Weight</small>
                    <p class="fw-bold mb-0 text-dark">{{ pickup.estimated_weight }} kg</p>
                </div>"""

if "pickup.estimated_weight" not in content:
    # Find the closing div of Scrap Category col-12
    # This is a bit risky with regex, so we'll look for a specific anchor point
    # The anchor is the closing </p> of scrap category, then </div>
    # We'll insert it before the "Address" block
    
    address_block_start = r'<div class="col-12">\s*<small class="text-muted">Address</small>'
    
    # Check if we can find the address block
    if re.search(address_block_start, content):
        # Insert Est Weight before Address block
        content = re.sub(
            r'(<div class="col-12">\s*<small class="text-muted">Address</small>)', 
            est_weight_html + r'\n                \1', 
            content
        )

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed agent_job_detail.html")
