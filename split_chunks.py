#!/usr/bin/env python3
import os

# Read the file
with open('index-finale.html', 'r') as f:
    content = f.read()

print(f"Total file size: {len(content)} bytes")

# Split into 5KB chunks
chunk_size = 5000
chunks = []
for i in range(0, len(content), chunk_size):
    chunk = content[i:i+chunk_size]
    chunks.append(chunk)
    
    # Write each chunk to a separate file
    with open(f'chunk-{len(chunks)-1}.txt', 'w') as f:
        f.write(chunk)
    print(f"Created chunk-{len(chunks)-1}.txt ({len(chunk)} bytes)")

print(f"\nTotal chunks: {len(chunks)}")
print(f"Chunk sizes: {[len(c) for c in chunks]}")

# Create a loader HTML that reassembles the chunks
loader_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loading Verus Blaster...</title>
    <style>
        body {{ margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background-color: #222; font-family: Arial, sans-serif; }}
        #loader {{ text-align: center; color: #fff; }}
        #progress {{ font-size: 20px; margin-bottom: 20px; }}
        #game-container {{ width: 100%; height: 100vh; }}
    </style>
</head>
<body>
    <div id="loader">
        <div id="progress">Loading game... <span id="percent">0</span>%</div>
    </div>
    <div id="game-container"></div>

    <script>
        const totalChunks = {len(chunks)};
        let loadedContent = '';

        async function loadChunks() {{
            try {{
                for (let i = 0; i < totalChunks; i++) {{
                    const response = await fetch(`chunk-${{i}}.txt`);
                    const text = await response.text();
                    loadedContent += text;
                    
                    const percent = Math.round(((i + 1) / totalChunks) * 100);
                    document.getElementById('percent').textContent = percent;
                }}

                // Hide loader and show game
                document.getElementById('loader').style.display = 'none';
                
                // Create iframe with the complete content
                const blob = new Blob([loadedContent], {{ type: 'text/html' }});
                const blobUrl = URL.createObjectURL(blob);
                
                const iframe = document.createElement('iframe');
                iframe.src = blobUrl;
                iframe.style.width = '100%';
                iframe.style.height = '100%';
                iframe.style.border = 'none';
                iframe.style.margin = '0';
                iframe.style.padding = '0';
                
                document.getElementById('game-container').appendChild(iframe);
            }} catch (error) {{
                document.getElementById('loader').innerHTML = '<div style="color: red;">Error loading game: ' + error.message + '</div>';
                console.error('Error:', error);
            }}
        }}

        loadChunks();
    </script>
</body>
</html>"""

with open('loader.html', 'w') as f:
    f.write(loader_html)

print("\n✓ Created loader.html")
print("\nTo use:")
print("1. Upload all chunk-N.txt files and loader.html to your server")
print("2. Open loader.html in a browser")
print("3. It will automatically fetch and assemble all chunks, then display the game")
