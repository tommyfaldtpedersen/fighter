#!/usr/bin/env python3
import json
import os

# Read the file (use the original, NOT the escaped version)
with open('index-finale.html', 'r') as f:
    content = f.read()

print(f"Total content size: {len(content)} bytes")

# Split into 5KB chunks (NO manual escaping - json.dump will handle it)
chunk_size = 5000
chunks = []
for i in range(0, len(content), chunk_size):
    chunk = content[i:i+chunk_size]
    chunks.append(chunk)
    print(f"Chunk {i}: {len(chunk)} bytes")

print(f"\nTotal chunks: {len(chunks)}")

# Create JSON with individual chunk entries
# json.dump() will automatically escape all special characters
chunks_data = {}
for i, chunk in enumerate(chunks):
    chunks_data[f"chunk-{i}"] = chunk

# Write to JSON file - json.dump handles all escaping automatically
with open('game-chunks.json', 'w') as f:
    json.dump(chunks_data, f)

json_size = os.path.getsize('game-chunks.json')
print(f"✓ Created game-chunks.json ({json_size/1024:.1f} KB)")
print(f"\nJSON structure:")
print(json.dumps(list(chunks_data.keys()), indent=2))

# Verify the chunks reassemble correctly
total_reassembled = sum(len(v) for v in chunks_data.values())
print(f"\nVerification:")
print(f"Original size: {len(content)} bytes")
print(f"Reassembled size: {total_reassembled} bytes")
print(f"Match: {total_reassembled == len(content)}")

