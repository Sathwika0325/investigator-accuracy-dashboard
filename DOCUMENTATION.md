# Investigator Accuracy Dashboard — Documentation

## What This Is

A dashboard that tracks and visualizes the **accuracy of the Freshservice AI Investigator** across monthly audit periods. Each audit evaluates how well the AI investigation tool performs on production support tickets — scoring correctness, identifying failure patterns, and tracking improvement over time.

---

## Repo Structure

| Path | Purpose |
|------|---------|
| `audits/` | One Markdown file per audit period (e.g., `investigator_accuracy_audit_july1st2026_July_31_2026.md`) |
| `scripts/parse_audits.py` | Python script that parses all `.md` files in `audits/` and generates structured JSON |
| `data/accuracy_data.json` | Auto-generated JSON consumed by the dashboard (do NOT edit manually) |
| `index.html` | Static dashboard — reads `data/accuracy_data.json` and renders charts/tables |
| `.github/workflows/update-dashboard.yml` | GitHub Actions workflow: parses audits → regenerates JSON → deploys to Pages |
| `README.md` | Quick overview |
| `DOCUMENTATION.md` | This file |

---

## How the Automation Works

```
Push a new .md file to audits/
         ↓
GitHub Actions triggers (on push to main)
         ↓
Runs scripts/parse_audits.py
  → Reads all .md files in audits/
  → Extracts accuracy scores, ticket IDs, categories, patterns
  → Writes data/accuracy_data.json
         ↓
Commits updated accuracy_data.json
         ↓
Deploys index.html + data/ to GitHub Pages
         ↓
Live dashboard updates automatically
```

**No manual edits to `data/accuracy_data.json` are needed.**
**No AI/LLM calls are involved in the update step** — it's pure text parsing.

---

## Adding Next Month's Audit

1. Create a new `.md` file in the `audits/` folder following the existing format:
   ```
   audits/investigator_accuracy_audit_aug1st2026_aug_31_2026.md
   ```

2. Add, commit, and push:
   ```bash
   git add audits/investigator_accuracy_audit_aug1st2026_aug_31_2026.md
   git commit -m "Add August 2026 accuracy audit"
   git push
   ```

3. The workflow runs automatically — dashboard updates within 1-2 minutes.

---

## Live Dashboard

**URL:** https://sathwika0325.github.io/investigator-accuracy-dashboard/

---

## Repo Visibility & Access

- **Visibility:** Public
- **Owner:** Sathwika0325
- **Access:** Anyone with the link can view the dashboard and source

---

## Setup Details

- **Date set up:** August 24, 2026
- **Set up by:** Naga Sathwika
- **GitHub Pages source:** GitHub Actions workflow (build_type: workflow)
- **Branch:** main
