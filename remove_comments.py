#!/usr/bin/env python3
import re

# Read the file
with open('index-optimized.html', 'r') as f:
    content = f.read()

# Remove single-line comments (//), but preserve :// in protocols
lines = content.split('\n')
processed_lines = []

for line in lines:
    # Skip pure comment lines
    if line.strip().startswith('//'):
        processed_lines.append('')
        continue
    
    # Remove inline comments (// ...) while being careful with URLs
    # Look for // that's not preceded by :
    parts = []
    current = 0
    for match in re.finditer(r'(?<!:)//(?!/)', line):
        parts.append(line[current:match.start()])
        current = len(line)
        break
    if current < len(line):
        parts.append(line[current:])
    
    processed_lines.append(''.join(parts).rstrip() if parts else line)

# Join back
content = '\n'.join(processed_lines)

# Remove multi-line comments /* ... */
content = re.sub(r'/\*[\s\S]*?\*/', '', content)

# Write the result
with open('index-minified.html', 'w') as f:
    f.write(content)

import os
size = os.path.getsize('index-minified.html')
original_size = os.path.getsize('index-optimized.html')
saved = original_size - size
saved_pct = (saved / original_size) * 100

print(f"Original: {original_size} bytes ({original_size/1024:.1f} KB)")
print(f"Minified: {size} bytes ({size/1024:.1f} KB)")
print(f"Saved: {saved} bytes ({saved_pct:.1f}%)")
