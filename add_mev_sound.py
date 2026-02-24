#!/usr/bin/env python3
import re

# Read the file
with open('index.html', 'r') as f:
    content = f.read()

# Define the new MEV shoot sound function
mev_shoot_sound = """function playMEVShootSound() {
            try {
                if (!audioContext) return;
                const now = audioContext.currentTime;
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                oscillator.type = 'sine';
                oscillator.frequency.setValueAtTime(500, now);
                oscillator.frequency.exponentialRampToValueAtTime(150, now + 0.15);
                gainNode.gain.setValueAtTime(0.25, now);
                gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
                oscillator.start(now);
                oscillator.stop(now + 0.15);
            } catch (e) {
                console.error('Error playing MEV shoot sound:', e);
            }
        }"""

# Find the position to insert - after playExtraLifeSound
match = re.search(r'(function playExtraLifeSound\(\).*?\}\s*catch\s*\(e\)\s*\{\s*console\.error\([^}]*\);?\s*\}\s*\})', content)

if match:
    insert_pos = match.end()
    content = content[:insert_pos] + '\n\n        ' + mev_shoot_sound + content[insert_pos:]
    print("✓ Added playMEVShootSound() function")
else:
    print("✗ Could not find insertion point")
    exit(1)

# Now find where MEV shoots and add the sound call
# Look for the pattern where mevProjectiles.push happens
pattern = r'(mevProjectiles\.push\(\{\s*x:\s*mev\.x,\s*y:\s*mev\.y,\s*velocityX:\s*Math\.cos\(mev\.rotation\)\s*\*\s*projectileSpeed,\s*velocityY:\s*Math\.sin\(mev\.rotation\)\s*\*\s*projectileSpeed,\s*lifetime:\s*0,\s*mevId:\s*mev\.id\s*\}\);)'

match = re.search(pattern, content)
if match:
    insert_pos = match.end()
    content = content[:insert_pos] + ' playMEVShootSound();' + content[insert_pos:]
    print("✓ Added playMEVShootSound() call to updateMEV()")
else:
    print("✗ Could not find MEV shoot location for sound call")

# Write the result
with open('index.html', 'w') as f:
    f.write(content)

import os
size = os.path.getsize('index.html')
print(f"Updated file size: {size/1024:.1f} KB")
