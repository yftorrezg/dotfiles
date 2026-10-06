---
name: kaggle-markdown-cell-trap
description: "Kaggle notebook editor gotcha - a code cell can silently become Markdown, causing Save & Run All to report Success while executing nothing"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fe618673-a603-4392-bd1e-3f9a597ea92a
  modified: 2026-09-11T04:06:09.632Z
---

When editing a Kaggle notebook cell through browser automation (or fast typing in general), a stray keystroke sent while the cell is in Jupyter "command mode" (not edit mode) can trigger a single-letter shortcut — notably `m` converts the selected cell to Markdown, `y` converts it back to Code. This happened twice in the Lazarillo project (see [[lazarillo-project-status]]) and each time "Save & Run All (Commit)" reported "Successfully ran" in ~23 seconds with 0 B output, because the cell holding all the actual training code had silently become non-executable Markdown — Kaggle does not warn about this.

**Why:** the fix (select cell, press `y` in command mode) is trivial once diagnosed, but the failure mode is silent (green checkmark, "Successful") and easy to miss if you only glance at the status rather than the run duration and output size.

**How to apply:** whenever a Kaggle "Save & Run All" commit finishes suspiciously fast (a few seconds instead of the expected minutes/hours) with 0 B output, suspect a cell that got demoted to Markdown rather than assuming the job is broken some other way. Verify a cell is genuinely Code (not Markdown) before committing by checking it has an execution-count prompt (`[ ]:`) and a play-triangle icon to its left, and syntax highlighting — if those are missing, select the cell and press `y` to convert it back to Code.
