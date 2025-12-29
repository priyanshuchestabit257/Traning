#!/usr/bin/env node

const fs = require("fs");
const fsp = fs.promises;
const path = require("path");
const { performance } = require("perf_hooks");


const args = process.argv.slice(2);

function parseArgs(args) {
  const tasks = [];

  for (let i = 0; i < args.length; i += 2) {
    const flag = args[i];
    const file = args[i + 1];

    if (!flag || !file) continue;

    tasks.push({ flag, file });
  }

  return tasks;
}

const tasks = parseArgs(args);
console.log("ARGS:", args);
console.log("TASKS:", tasks);


if (tasks.length === 0) {
  console.log("\nUsage:");
  console.log(" node stats.js --lines file1.txt --words file2.txt --chars file3.txt");
  console.log(" Bonus: --unique file");
  process.exit(0);
}


const logsDir = path.join(__dirname, "logs");
const outDir = path.join(__dirname, "output");

if (!fs.existsSync(logsDir)) fs.mkdirSync(logsDir, { recursive: true });
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });


async function readFileSafe(file) {
  try {
    return await fsp.readFile(file, "utf8");
  } catch (err) {
    console.error("File error:", file, err.message);
    return null;
  }
}

function countLines(text) {
  return text.split("\n").length;
}

function countWords(text) {
  return text.trim().split(/\s+/).length;
}

function countChars(text) {
  return text.length;
}

async function removeDuplicates(file, text) {
  const lines = text.split("\n");
  const unique = [...new Set(lines)].join("\n");

  const outputPath = path.join(outDir, `unique-${path.basename(file)}`);
  await fsp.writeFile(outputPath, unique);

  return outputPath;
}

// ------------------------------
// Performance Logger
// ------------------------------
async function logPerformance(type, file, startTime) {
  const end = performance.now();
  const duration = end - startTime;

  const metrics = {
    file,
    operation: type,
    timeMs: duration.toFixed(2),
    memoryMB: (process.memoryUsage().rss / 1024 / 1024).toFixed(2),
    cpuUsage: process.cpuUsage(),
    resourceUsage: process.resourceUsage(),
    timestamp: new Date().toISOString()
  };

  const logPath = path.join(logsDir, `performance-${type}-${path.basename(file)}.json`);
  await fsp.writeFile(logPath, JSON.stringify(metrics, null, 2));

  console.log(`📁 Logged → ${logPath}`);
}

// ------------------------------
// Main Worker (per task)
// ------------------------------
async function processTask({ flag, file }) {
    console.log("Running task:", flag, "for file:", file);
  const text = await readFileSafe(file);
  if (!text) return;

  const start = performance.now();

  if (flag === "--lines") {
    const count = countLines(text);
    console.log(`Lines in ${file}:`, count);
    await logPerformance("lines", file, start);
  }

  else if (flag === "--words") {
    const count = countWords(text);
    console.log(`Words in ${file}:`, count);
    await logPerformance("words", file, start);
  }

  else if (flag === "--chars") {
    const count = countChars(text);
    console.log(`Characters in ${file}:`, count);
    await logPerformance("chars", file, start);
  }

  else if (flag === "--unique") {
    const outPath = await removeDuplicates(file, text);
    console.log(`Unique lines saved at:`, outPath);
    await logPerformance("unique", file, start);
  }

  else {
    console.log("Unknown flag:", flag);
  }
}

// ------------------------------
// PARALLEL EXECUTION (Promise.all)
// ------------------------------
async function start() {
  console.log("\n🚀 Running Day 2 CLI Tool...\n");
  await Promise.all(tasks.map(processTask));
  console.log("\n✅ All tasks completed.\n");
}

start();
