# Why the .xlsx isn't in this repo

This repo is public (GitHub Pages requires it on the free plan). The compiled
`Airbnb_STR_ROI_Calculator.xlsx` used to be committed here, which meant the exact file
customers pay $19 for on Payhip was freely downloadable from this repo for anyone who found it.

Removed from the current tree on 2026-07-20 (iteration 9) once the repo went public, so the
paid product isn't sitting next to the free marketing site.

- Buy the current file: https://payhip.com/b/EIy4L
- Rebuild it yourself from source: `build.py` in this folder (same formulas, same layout).
- The file still exists in this repo's git history (commit `f1623f0` and after) — removing it
  from the working tree does not scrub history. Fully purging it requires a git history rewrite
  + force-push to `main`, which this agent will not do unilaterally (destructive, and this repo
  may have other clones/forks depending on the current history). Flagged in `morning-queue.md`
  for the human to decide whether that's worth doing.
