# Verus Blaster - Blockchain Deployment Guide

## 🎮 Overview

Verus Blaster can be deployed in multiple ways, including optimized blockchain storage with gzip compression.

## 📊 File Size Comparison

| Format                 | Size        | Compression | Use Case                  |
| ---------------------- | ----------- | ----------- | ------------------------- |
| Original HTML          | 67.5 KB     | -           | Development               |
| Minified               | 31.6 KB     | 53%         | Standard web hosting      |
| Gzipped (binary)       | 6.81 KB     | 78.5%       | Server with gzip          |
| **Gzipped + Base64**   | **9.09 KB** | **71.8%**   | **Blockchain storage**    |
| Single-file (embedded) | 12.84 KB    | -           | Self-contained blockchain |

## 🔧 Build Commands

### 1. Standard Build (with gzip support)

```bash
node build.js
```

**Generates:**

- `game-chunks.json` - Regular minified chunks
- `game-compressed.txt` - Gzipped + base64 (9 KB) ⭐
- `game-chunks-gzip.json` - 5KB chunks of one gzipped+base64 payload
- `chunk-X-gzip.txt` files

### 2. Create Self-Contained File

```bash
node build.js
node build-embedded.js
```

**Generates:**

- `blockchain-single-file.html` - Complete game in one file (12.84 KB)

## 🚀 Deployment Options

### Option 1: Single Compressed File (Recommended for Blockchain)

**Files needed:**

- `game-compressed.txt` (9.09 KB)
- `blockchain-loader.html` (loader)

**Configuration in blockchain-loader.html:**

```javascript
const LOAD_METHOD = "single";
const COMPRESSED_DATA_URL = "./game-compressed.txt";
```

**Blockchain storage:**

1. Store `game-compressed.txt` on-chain (9 KB)
2. Host `blockchain-loader.html` separately or on-chain
3. Loader fetches and decompresses the game

### Option 2: Self-Contained Single File

**Files needed:**

- `blockchain-single-file.html` (12.84 KB total)

**Blockchain storage:**

- Store entire file on-chain
- No external dependencies except fflate CDN
- Most convenient but slightly larger

### Option 3: Chunked Gzipped Storage

**Files needed:**

- `game-chunks-gzip.json` (9.11 KB)
- `blockchain-loader.html` (loader)

**Configuration in blockchain-loader.html:**

```javascript
const LOAD_METHOD = "chunks";
const CHUNKS_JSON_URL = "./game-chunks-gzip.json";
```

**Use case:** Splitting one compressed payload across multiple blockchain transactions

### Option 4: Standard Web Hosting

Use `game-chunks.json` + `loader-escaped.html` for traditional hosting without compression overhead.

## 📦 What Gets Compressed

The gzip compression works exceptionally well because:

- Repetitive JavaScript patterns
- Similar function names and keywords
- CSS rules with common properties
- HTML structure

**Compression ratio: 78.5%** (31.6 KB → 6.81 KB gzipped)

## 🔐 Blockchain Considerations

### Storage Costs

```
Uncompressed: 31.6 KB × $X/byte = $$$
Compressed:    9.1 KB × $X/byte = $   (71% cheaper!)
```

### Decompression

- Uses `fflate` library (~8 KB, loaded from CDN)
- Decompression happens in browser (client-side)
- One-time ~50-100ms overhead on load
- No server-side processing needed

### Dependencies

- **fflate CDN:** `https://cdn.jsdelivr.net/npm/fflate@0.8.2/umd/index.js`
- Can be embedded for fully offline use (adds 8 KB)

## 🔄 Update Workflow

When you update the game:

```bash
# 1. Edit index.html
# 2. Rebuild everything
node build.js

# 3. (Optional) Create self-contained version
node build-embedded.js

# 4. Deploy new compressed files to blockchain
```

## 🌐 Browser Compatibility

All modern browsers support:

- Gzip decompression (via fflate)
- Base64 decoding (native)
- TextDecoder API

**Tested on:**

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers (iOS/Android)

## 📝 Technical Details

### Compression Process

1. **Minification:** Remove comments, whitespace → 31.6 KB
2. **Gzip:** Compress with zlib → 6.81 KB (binary)
3. **Base64:** Encode for text storage → 9.09 KB (string)
4. **Chunking (optional):** Split base64 payload into 5,000-byte chunks

### Decompression Process

1. **Fetch:** Load base64 string from chain
2. **Decode:** Convert base64 → binary (Uint8Array)
3. **Gunzip:** Decompress with fflate → original HTML
4. **Inject:** Load game into browser

For `LOAD_METHOD = "chunks"`, the loader first combines all chunk strings, then runs steps 2-4 once.

## 🎯 Recommendation for Blockchain

**Best option:** Use `game-compressed.txt` (9.09 KB)

**Why:**

- Smallest on-chain footprint
- Easy to update (single file)
- Fast decompression
- Standard base64 encoding
- Works with any blockchain

**Alternative:** Use `blockchain-single-file.html` (12.84 KB) for ultimate simplicity

## 🔍 File Structure

```
fighter/
├── index.html                          # Original game (67.5 KB)
├── build.js                            # Main build script
├── build-embedded.js                   # Create self-contained file
├── blockchain-loader.html              # Loader for compressed files
├── blockchain-loader-embedded.html     # Template for embedded version
├── blockchain-single-file.html         # Self-contained final version
├── game-compressed.txt                 # Gzipped game (9.09 KB) ⭐
├── game-chunks-gzip.json              # Gzip-first 5KB chunks (9.11 KB)
└── chunk-X-gzip.txt                   # Chunk parts of base64 gzip payload
```

## 💡 Tips

1. **Test locally first:** Open `blockchain-loader.html` in browser
2. **Check compression:** Run `node build.js` to see stats
3. **Verify integrity:** Hash the compressed file for chain verification
4. **Update URL:** Change `COMPRESSED_DATA_URL` to your blockchain endpoint
5. **Cache fflate:** Consider embedding it for offline functionality

## 🆘 Troubleshooting

**Error: "fflate library failed to load"**

- Check internet connection (CDN required)
- Consider embedding fflate locally

**Error: "Failed to decompress"**

- Ensure base64 data is not corrupted
- Verify the full string was stored on chain

**Game doesn't load:**

- Check browser console for errors
- Verify CORS headers if loading from external source
- Test with `blockchain-single-file.html` first

## 📚 Additional Resources

- fflate documentation: https://github.com/101arrowz/fflate
- Base64 encoding: https://developer.mozilla.org/en-US/docs/Web/API/btoa
- Gzip format: https://www.gnu.org/software/gzip/

---

**Ready to deploy!** 🚀

For blockchain deployment, start with `game-compressed.txt` (9.09 KB)
