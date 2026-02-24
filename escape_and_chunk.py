#!/usr/bin/env python3
import os
import json

# Read the file
with open('index-finale.html', 'r') as f:
    content = f.read()

print(f"Original file size: {len(content)} bytes")

# Escape all quotes (both single and double)
escaped_content = content.replace('\\', '\\\\')  # Escape backslashes first
escaped_content = escaped_content.replace('"', '\\"')  # Escape double quotes
escaped_content = escaped_content.replace("'", "\\'")  # Escape single quotes

print(f"Escaped content size: {len(escaped_content)} bytes")

# Save escaped version
with open('index-finale-escaped.html', 'w') as f:
    f.write(escaped_content)

escaped_size = os.path.getsize('index-finale-escaped.html')
print(f"✓ Created index-finale-escaped.html ({escaped_size/1024:.1f} KB)")

# Split escaped content into 5KB chunks
chunk_size = 5000
chunks = []
for i in range(0, len(escaped_content), chunk_size):
    chunk = escaped_content[i:i+chunk_size]
    chunks.append(chunk)
    print(f"Chunk {len(chunks)-1}: {len(chunk)} bytes")

print(f"\nTotal chunks: {len(chunks)}")

# Save individual chunk files
for i, chunk in enumerate(chunks):
    with open(f'escaped-chunk-{i}.txt', 'w') as f:
        f.write(chunk)

# Create JSON structure
chunks_data = {
    "totalChunks": len(chunks),
    "chunks": chunks
}

# Write to JSON file
with open('game-chunks-escaped.json', 'w') as f:
    json.dump(chunks_data, f)

json_size = os.path.getsize('game-chunks-escaped.json')
print(f"✓ Created game-chunks-escaped.json ({json_size/1024:.1f} KB)")

# Create a loader HTML that loads from JSON and unescapes
loader_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loading Verus Blaster...</title>
    <style>
        body { margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background-color: #222; font-family: Arial, sans-serif; }
        #loader { text-align: center; color: #fff; }
        #progress { font-size: 20px; margin-bottom: 20px; }
        #game-container { width: 100%; height: 100vh; }
    </style>
</head>
<body>
    <div id="loader">
        <div id="progress">Loading game... <span id="percent">0</span>%</div>
    </div>
    <div id="game-container"></div>

    <script>
        async function loadGame() {
            try {
                // Fetch the JSON file
                const response = await fetch('game-chunks-escaped.json');
                const data = await response.json();
                
                let loadedContent = '';
                
                // Reassemble chunks from JSON
                for (let i = 0; i < data.totalChunks; i++) {
                    loadedContent += data.chunks[i];
                    
                    const percent = Math.round(((i + 1) / data.totalChunks) * 100);
                    document.getElementById('percent').textContent = percent;
                }

                // Unescape the content
                loadedContent = loadedContent
                    .replace(/\\"/g, '"')
                    .replace(/\\'/g, "'")
                    .replace(/\\\\\\\\/g, '\\\\')  // Unescape backslashes last
                    .replace(/\\\\/g, '\\\\');

                // Hide loader and show game
                document.getElementById('loader').style.display = 'none';
                
                // Create iframe with the complete content
                const blob = new Blob([loadedContent], { type: 'text/html' });
                const blobUrl = URL.createObjectURL(blob);
                
                const iframe = document.createElement('iframe');
                iframe.src = blobUrl;
                iframe.style.width = '100%';
                iframe.style.height = '100%';
                iframe.style.border = 'none';
                iframe.style.margin = '0';
                iframe.style.padding = '0';
                
                document.getElementById('game-container').appendChild(iframe);
            } catch (error) {
                document.getElementById('loader').innerHTML = '<div style="color: red;">Error loading game: ' + error.message + '</div>';
                console.error('Error:', error);
            }
        }

        loadGame();
    </script>
</body>
</html>"""

with open('loader-escaped.html', 'w') as f:
    f.write(loader_html)

print("✓ Created loader-escaped.html")

print("\n" + "="*50)
print(f"SUMMARY:")
print("="*50)
print(f"Original:                {len(content):7} bytes")
print(f"Escaped:                 {len(escaped_content):7} bytes (increase: {len(escaped_content)-len(content)} bytes)")
print(f"Total chunks:            {len(chunks)}")
print(f"Chunk sizes:             {[len(c) for c in chunks]}")
print("="*50)
print("\nTo use:")
print("1. Upload game-chunks-escaped.json and loader-escaped.html")
print("2. Open loader-escaped.html in a browser")
print("3. Game will load, unescape, and display")
