// "The World in One Image - 19 November 2026" (Node 22, standard library only).
//
// The entry image is the entry.png beside this file, drawn by draw.py.
// This program copies it into the output directory the grader provides
// (MAKEFUN_OUTPUT_DIR, defaulting to /output), creating that directory
// first so the copy always has somewhere to land.
//
// Run locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
