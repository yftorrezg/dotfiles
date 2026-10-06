---
name: lazarillo-project-status
description: "Current status of the Lazarillo Android thesis project (blind-assistance app) — models trained, pending device verification, where to find everything"
metadata: 
  node_type: memory
  type: project
  originSessionId: fe618673-a603-4392-bd1e-3f9a597ea92a
  modified: 2026-09-11T04:06:01.183Z
---

Lazarillo is a native Android (Kotlin) blind-assistance app the user is building for their university thesis (Taller de Grado). Package `com.lazarillo.app`, in `/home/yafer/Proyectos/Ciego`.

**Why:** university thesis project, must be a real working/tested product, not a demo.
**How to apply:** always read `/home/yafer/Proyectos/Ciego/CLAUDE.md` first when resuming work in this repo — it has the up-to-date status, and the full architecture/plan lives at `/home/yafer/.claude/plans/que-opinas-sobre-este-wobbly-elephant.md`.

As of 2026-09-11: both ML models (obstacle detector + path segmenter) are trained (via Kaggle "Save & Run All" commits) and placed in `app/src/main/assets/models/`. A voice-repeat bug in the alert system was fixed. A foreground-service migration (so the app keeps detecting with the screen locked) is code-complete in git worktree branch `worktree-agent-aaff555bbd087c837` but NOT YET verified on the real device (Samsung SM-S928B) because the phone disconnected from adb mid-session — this is the top pending item.

See [[kaggle-markdown-cell-trap]] for a real gotcha that wasted two training attempts.
