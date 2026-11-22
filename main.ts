import { copyFileSync, mkdirSync, readdirSync, rmSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// This program copies the front-page image next to it into the output
// directory, leaving the directory itself in place and clearing only
// whatever it already holds, one entry at a time.
const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
for (const name of readdirSync(outDir)) {
  rmSync(join(outDir, name), { recursive: true, force: true });
}
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
