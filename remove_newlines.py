#!/usr/bin/env python3
import os
import re

# Read the minified file
input_file = 'index-minified.html'

with open(input_file, 'r') as f:
    content = f.read()

print("Removing all newlines and extra whitespace...")

# Remove all newlines and carriage returns
content = content.replace('\n', '').replace('\r', '')

# Remove multiple spaces (keep single space where needed)
content = re.sub(r'  +', ' ', content)

# Write the final version
output_file = 'index-final.html'
with open(output_file, 'w') as f:
    f.write(content)

# Check file sizes
input_size = os.path.getsize(input_file)
output_size = os.path.getsize(output_file)
original_size = os.path.getsize('index.html')
saved = input_size - output_size
saved_total = original_size - output_size
saved_total_pct = (saved_total / original_size) * 100

print(f"\n{'='*60}")
print(f"Original (index.html):                {original_size:8d} bytes ({original_size/1024:5.1f} KB)")
print(f"Minified (no comments):               {input_size:8d} bytes ({input_size/1024:5.1f} KB)")
print(f"Final (newlines removed):             {output_size:8d} bytes ({output_size/1024:5.1f} KB) [-{saved/1024:.1f} KB]")
print(f"\n{'='*60}")
print(f"TOTAL SAVINGS: {saved_total} bytes ({saved_total_pct:.1f}%)")
print(f"File size reduction: {original_size/1024:.1f} KB → {output_size/1024:.1f} KB")
print(f"Compression ratio: {original_size/output_size:.1f}x smaller")
print(f"{'='*60}")
