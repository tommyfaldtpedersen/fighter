#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const zlib = require("zlib");

console.log("🎮 Verus Blaster Optimizer - All-in-One Build Script\n");

// ============================================
// 1. Read the original HTML file
// ============================================
console.log("📂 Reading index.html...");
let content = fs.readFileSync("index.html", "utf-8");
console.log(
  `   Original size: ${content.length} bytes (${(content.length / 1024).toFixed(1)} KB)`,
);

// ============================================
// 2. Remove comments
// ============================================
console.log("\n🧹 Removing comments...");
// Remove single-line comments (outside of code)
let lines = content.split("\n");
lines = lines.map((line) => {
  if (line.trim().startsWith("//")) {
    return "";
  }
  // Remove inline comments (be careful with URLs containing //)
  const match = line.match(/^([^/]*?)(?<!:)\/\/(?!\/)/);
  if (match) {
    return match[1].trimRight();
  }
  return line;
});
content = lines.join("\n");

// Remove multi-line comments
content = content.replace(/\/\*[\s\S]*?\*\//g, "");
console.log(`   ✓ Comments removed`);

// ============================================
// 3. Minify CSS and JavaScript
// ============================================
console.log("\n⚙️  Minifying CSS and JavaScript...");

// Minify CSS in <style> tags
content = content.replace(/<style>([\s\S]*?)<\/style>/g, (match, css) => {
  // Remove CSS comments
  css = css.replace(/\/\*[\s\S]*?\*\//g, "");
  // Remove whitespace around operators
  css = css.replace(/\s*([{}:;,>+~])\s*/g, "$1");
  // Remove extra spaces
  css = css.replace(/\s+/g, " ").trim();
  return `<style>${css}</style>`;
});

// Minify JavaScript in <script> tags
content = content.replace(/<script>([\s\S]*?)<\/script>/g, (match, js) => {
  // Remove single-line comments
  js = js
    .split("\n")
    .filter((line) => !line.trim().startsWith("//"))
    .join("\n");
  js = js.replace(/(?<!:)\/\/(?!\/)[^\n]*/g, "");
  // Remove whitespace around operators and brackets
  js = js.replace(/\s*([{}()[\];:,=+\-*/%<>!&|^?])\s*/g, "$1");
  // Remove newlines
  js = js.replace(/\n/g, "");
  // Clean up multiple spaces
  js = js.replace(/\s+/g, " ").trim();
  return `<script>${js}</script>`;
});

console.log(`   ✓ CSS and JavaScript minified`);

// ============================================
// 4. Remove all newlines and extra whitespace
// ============================================
console.log("\n📉 Removing newlines...");
content = content.replace(/\n/g, "").replace(/\r/g, "");
content = content.replace(/\s+/g, " ").trim();
const optimizedSize = content.length;
console.log(`   ✓ Newlines removed`);
console.log(
  `   Optimized size: ${optimizedSize} bytes (${(optimizedSize / 1024).toFixed(1)} KB)`,
);

// ============================================
// 5. Escape quotes for text storage
// ============================================
console.log("\n🔐 Escaping quotes...");
let escapedContent = content
  .replace(/\\/g, "\\\\") // Escape backslashes first
  .replace(/"/g, '\\"') // Escape double quotes
  .replace(/'/g, "\\'"); // Escape single quotes
const escapedSize = escapedContent.length;
console.log(`   ✓ Quotes escaped (size: ${escapedSize} bytes)`);

// ============================================
// 6. Create 5KB chunks
// ============================================
console.log("\n✂️  Creating 5KB chunks...");
const chunkSize = 5000;
const chunks = [];
for (let i = 0; i < optimizedSize; i += chunkSize) {
  chunks.push(content.substring(i, i + chunkSize));
}
console.log(`   ✓ Created ${chunks.length} chunks`);
chunks.forEach((chunk, i) => {
  console.log(`     chunk-${i}: ${chunk.length} bytes`);
});

// ============================================
// 7. Save individual chunk files with escaping
// ============================================
console.log("\n💾 Saving individual chunk files...");
chunks.forEach((chunk, i) => {
  const escapedChunk = chunk
    .replace(/\\/g, "\\\\")
    .replace(/"/g, '\\"')
    .replace(/'/g, "\\'");
  fs.writeFileSync(`chunk-${i}.txt`, escapedChunk, "utf-8");
  console.log(`   ✓ chunk-${i}.txt (${chunk.length} bytes)`);
});

// ============================================
// 8. Create game-chunks.json
// ============================================
console.log("\n� Creating game-chunks.json...");
const chunksData = {};
chunks.forEach((chunk, i) => {
  chunksData[`chunk-${i}`] = chunk;
});
const jsonContent = JSON.stringify(chunksData);
fs.writeFileSync("game-chunks.json", jsonContent, "utf-8");
const jsonSize = fs.statSync("game-chunks.json").size;
console.log(
  `   ✓ game-chunks.json created (${(jsonSize / 1024).toFixed(1)} KB)`,
);

// ============================================
// 9. Gzip compression for blockchain deployment
// ============================================
console.log("\n🗜️  Creating gzipped chunks for blockchain...");

// Gzip the entire optimized content
const gzippedContent = zlib.gzipSync(Buffer.from(content, "utf-8"));
const gzippedBase64 = gzippedContent.toString("base64");
const gzipSize = gzippedContent.length;
const base64Size = gzippedBase64.length;

console.log(
  `   Original size:     ${optimizedSize} bytes (${(optimizedSize / 1024).toFixed(2)} KB)`,
);
console.log(
  `   Gzipped size:      ${gzipSize} bytes (${(gzipSize / 1024).toFixed(2)} KB)`,
);
console.log(
  `   Base64 size:       ${base64Size} bytes (${(base64Size / 1024).toFixed(2)} KB)`,
);
console.log(
  `   Compression ratio: ${((1 - gzipSize / optimizedSize) * 100).toFixed(1)}%`,
);

// Save gzipped content as base64
fs.writeFileSync("game-compressed.txt", gzippedBase64, "utf-8");
console.log(`   ✓ game-compressed.txt saved (base64-encoded gzip)`);

// Create gzipped JSON chunks (for larger blockchain storage)
console.log("\n   Creating gzipped chunk files...");
const gzippedChunks = {};
const gzippedChunkFiles = [];

chunks.forEach((chunk, i) => {
  const gzipped = zlib.gzipSync(Buffer.from(chunk, "utf-8"));
  const base64 = gzipped.toString("base64");
  gzippedChunks[`chunk-${i}`] = base64;
  fs.writeFileSync(`chunk-${i}-gzip.txt`, base64, "utf-8");
  gzippedChunkFiles.push({
    index: i,
    originalSize: chunk.length,
    gzippedSize: gzipped.length,
    base64Size: base64.length,
  });
  console.log(
    `     chunk-${i}-gzip.txt: ${chunk.length}b → ${gzipped.length}b (${((1 - gzipped.length / chunk.length) * 100).toFixed(1)}% reduction)`,
  );
});

// Save gzipped chunks as JSON
const gzippedJsonContent = JSON.stringify(gzippedChunks);
fs.writeFileSync("game-chunks-gzip.json", gzippedJsonContent, "utf-8");
const gzippedJsonSize = fs.statSync("game-chunks-gzip.json").size;
console.log(
  `\n   ✓ game-chunks-gzip.json created (${(gzippedJsonSize / 1024).toFixed(2)} KB)`,
);

// ============================================
// 10. Summary
// ============================================
console.log("\n" + "=".repeat(50));
console.log("✨ BUILD SUMMARY");
console.log("=".repeat(50));
console.log(
  `Original (index.html):        ${(content.length / 1024).toFixed(1)} KB`,
);
console.log(`Game chunks (JSON):           ${(jsonSize / 1024).toFixed(1)} KB`);
console.log(
  `Individual chunks (7 files):  ${chunks.map((c) => c.length).reduce((a, b) => a + b, 0)} bytes total`,
);
console.log(
  `Total optimization:           ${((1 - optimizedSize / content.length) * 100).toFixed(1)}% reduction`,
);
console.log("\n" + "🗜️  BLOCKCHAIN COMPRESSION".padEnd(50, " "));
console.log(
  `Gzipped (single file):        ${(gzipSize / 1024).toFixed(2)} KB (${((1 - gzipSize / optimizedSize) * 100).toFixed(1)}% smaller)`,
);
console.log(
  `Base64 encoded:               ${(base64Size / 1024).toFixed(2)} KB`,
);
console.log(
  `Gzipped chunks (JSON):        ${(gzippedJsonSize / 1024).toFixed(2)} KB`,
);
console.log("=".repeat(50));

console.log("\n📤 Deployment options:");
console.log("   1. Upload game-chunks.json + loader-escaped.html");
console.log("   2. Upload chunk-0.txt through chunk-6.txt + loader.html");
console.log(
  "   3. 🔗 BLOCKCHAIN: Upload game-compressed.txt + blockchain-loader.html",
);
console.log(
  "   4. 🔗 BLOCKCHAIN: Upload game-chunks-gzip.json + blockchain-loader.html",
);
console.log("\n✅ All files ready for deployment!\n");
