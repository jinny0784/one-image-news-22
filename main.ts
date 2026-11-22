// Entry hand-in for news-image-20261122 ("Sum up 22 November's world
// news in one image"). The repository holds the finished front page as
// entry.png; this program copies it to the output directory as
// /output/entry.png, exactly the bytes the judge should see.
//
// Node 22, standard library only, no network. The output directory is
// created if needed and its previous contents are cleared entry by
// entry -- the directory itself is never deleted, because on the
// grader it is a mount point that cannot be removed.

import { copyFileSync, existsSync, mkdirSync, readdirSync, rmSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const target = join(outputDir, "entry.png");

if (!existsSync(source)) {
  console.error(`entry.png not found next to main.ts (looked in ${here})`);
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });

// Clear whatever a previous run left behind, one entry at a time.
for (const name of readdirSync(outputDir)) {
  rmSync(join(outputDir, name), { recursive: true, force: true });
}

copyFileSync(source, target);
const bytes = statSync(target).size;
console.log(`wrote ${target} (${bytes} bytes)`);
