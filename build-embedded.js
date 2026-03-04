#!/usr/bin/env node

const fs = require("fs");

console.log("🔗 Creating self-contained blockchain deployment file...\n");

// Read the compressed game data
const compressedData = fs.readFileSync("game-compressed.txt", "utf-8");
console.log(
  `✓ Loaded compressed data: ${(compressedData.length / 1024).toFixed(2)} KB`,
);

// Read the template
const template = fs.readFileSync("blockchain-loader-embedded.html", "utf-8");
console.log("✓ Loaded template");

// Replace the placeholder with actual data
const finalHTML = template.replace("{{COMPRESSED_DATA}}", compressedData);

// Save the final file
fs.writeFileSync("blockchain-single-file.html", finalHTML, "utf-8");
const finalSize = fs.statSync("blockchain-single-file.html").size;

console.log("✓ Created blockchain-single-file.html");
console.log("\n" + "=".repeat(50));
console.log("📊 FINAL FILE STATS");
console.log("=".repeat(50));
console.log(`Total file size:     ${(finalSize / 1024).toFixed(2)} KB`);
console.log(
  `Compressed data:     ${(compressedData.length / 1024).toFixed(2)} KB`,
);
console.log(
  `Loader overhead:     ${((finalSize - compressedData.length) / 1024).toFixed(2)} KB`,
);
console.log("=".repeat(50));
console.log("\n✅ Single-file blockchain deployment ready!");
console.log("   Upload: blockchain-single-file.html");
console.log("   Note: Requires internet to load fflate library\n");
