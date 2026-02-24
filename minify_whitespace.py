#!/usr/bin/env python3
import re
import os

def minify_css(css):
    """Minify CSS by removing unnecessary whitespace"""
    # Remove comments
    css = re.sub(r'/\*[\s\S]*?\*/', '', css)
    # Remove whitespace around selectors and properties
    css = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', css)
    # Remove leading/trailing whitespace
    css = css.strip()
    # Remove extra spaces
    css = re.sub(r'\s+', ' ', css)
    return css

def minify_js(js):
    """Minify JavaScript by removing unnecessary whitespace"""
    # Remove single-line comments carefully (not in strings)
    lines = []
    for line in js.split('\n'):
        # Skip lines that are pure comments
        if line.strip().startswith('//'):
            continue
        # Remove inline comments (try to avoid URLs with //)
        match = re.search(r'(?<!:)//(?![/\s])', line)
        if match:
            line = line[:match.start()]
        lines.append(line)
    js = '\n'.join(lines)
    
    # Remove extra whitespace around brackets and operators
    js = re.sub(r'\s*([{}()[\];:,=+\-*/%<>!&|^?])\s*', r'\1', js)
    # Remove newlines
    js = js.replace('\n', '')
    # Clean up multiple spaces
    js = re.sub(r' +', ' ', js)
    return js.strip()

# Read the file
with open('index-finale.html', 'r') as f:
    content = f.read()

print(f"Original size: {len(content)} bytes ({len(content)/1024:.1f} KB)")

# Minify CSS in <style> tags
def replace_style(match):
    css = match.group(1)
    minified = minify_css(css)
    return f'<style>{minified}</style>'

content = re.sub(r'<style>(.*?)</style>', replace_style, content, flags=re.DOTALL)
print("✓ Minified CSS in <style> tags")

# Minify JS in <script> tags (exclude src attributes)
def replace_script(match):
    js = match.group(1)
    minified = minify_js(js)
    return f'<script>{minified}</script>'

content = re.sub(r'<script>(.*?)</script>', replace_script, content, flags=re.DOTALL)
print("✓ Minified JavaScript in <script> tags")

# Write the result
with open('index-minimize-ws.html', 'w') as f:
    f.write(content)

new_size = os.path.getsize('index-minimize-ws.html')
saved = len(content.encode()) - new_size if new_size else 0

print(f"\nOptimized size: {new_size} bytes ({new_size/1024:.1f} KB)")
print(f"Saved: {saved} bytes ({(saved/len(content.encode()))*100:.1f}%)")

# Now update chunks with the new optimized version
print("\n" + "="*50)
print("Regenerating chunks with optimized content...")
print("="*50)

import json

# Read optimized content
with open('index-minimize-ws.html', 'r') as f:
    optimized_content = f.read()

# Split into 5KB chunks
chunk_size = 5000
chunks = []
for i in range(0, len(optimized_content), chunk_size):
    chunk = optimized_content[i:i+chunk_size]
    chunks.append(chunk)

print(f"Total chunks: {len(chunks)}")
print(f"Chunk sizes: {[len(c) for c in chunks]}")

# Create JSON with individual chunk entries
chunks_data = {}
for i, chunk in enumerate(chunks):
    chunks_data[f"chunk-{i}"] = chunk
    
    # Escape quotes for individual chunk files
    escaped_chunk = chunk.replace('\\', '\\\\')  # Escape backslashes first
    escaped_chunk = escaped_chunk.replace('"', '\\"')  # Escape double quotes
    escaped_chunk = escaped_chunk.replace("'", "\\'")  # Escape single quotes
    
    # Save individual chunk files with escaped content
    with open(f'chunk-{i}.txt', 'w') as f:
        f.write(escaped_chunk)

# Write to JSON file (json.dump handles escaping automatically)
with open('game-chunks.json', 'w') as f:
    json.dump(chunks_data, f)

json_size = os.path.getsize('game-chunks.json')
print(f"\n✓ Updated game-chunks.json ({json_size/1024:.1f} KB)")
print(f"✓ Saved individual chunk files with escaped quotes (chunk-0.txt through chunk-{len(chunks)-1}.txt)")

# Verify
total_reassembled = sum(len(v) for v in chunks_data.values())
print(f"\nVerification:")
print(f"Content size: {len(optimized_content)} bytes")
print(f"Reassembled size: {total_reassembled} bytes")
print(f"Match: {total_reassembled == len(optimized_content)}")
