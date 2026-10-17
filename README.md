# Investigator Accuracy Dashboard

A self-updating dashboard for the Freshservice AI Investigator accuracy audits.
Drop a new audit `.md` file into `audits/`, push it — the dashboard updates itself.
No AI credits are spent on the update; a plain Python script parses the markdown.

## One-time setup

1. **Create a GitHub repo** and push this folder to it (see commands below).
2. **Enable GitHub Pages**: repo → Settings → Pages → Build and deployment →
   Source: **GitHub Actions**. (Not "Deploy from a branch" — the workflow
   here uses the Pages Actions deployment method.)
3. That's it. The first push will build `data/accuracy_data.json` and deploy
   `index.html` to `https://<your-username>.github.io/<repo-name>/`.

```bash
cd dashboard-repo
git init
git add .
git commit -m "Initial accuracy dashboard"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

## Adding a new month's audit

Just add the next markdown file to `audits/` (same format as the July doc)
and push to `main`:

```bash
cp ~/Downloads/investigator_accuracy_audit_august2026.md audits/
git add audits/
git commit -m "Add August 2026 accuracy audit"
git push
```

The `update-dashboard.yml` workflow triggers automatically on any push that
touches `audits/**.md`, re-parses **all** files in that folder (so edits or
removals are reflected too), commits the regenerated `data/accuracy_data.json`,
and redeploys the Pages site. Takes under a minute, and costs nothing beyond
GitHub Actions' free minutes for public repos.

## Parser assumptions

`scripts/parse_audits.py` expects each doc to follow the structure of the
July 2026 audit:

- `# <Doc title>` at the top
- `**Period:** <text>` metadata line
- Ticket sections: `## N. Ticket #ID — Title`
- `**Accuracy:** <Label> (<NN>%)` inside each ticket section

If a future doc's format drifts, update the regexes at the top of
`parse_audits.py` — the rest of the pipeline (dashboard, workflow) doesn't
need to change.

## Local preview

```bash
python3 scripts/parse_audits.py   # regenerate data/accuracy_data.json
python3 -m http.server 8000       # serve the folder
# open http://localhost:8000
```
(A local `file://` open won't work — `fetch()` needs an HTTP server.)

## Monthly audit prompt

`prompts/monthly-audit.md` is a paste-ready Kiro prompt. It needs no editing: it runs
`node scripts/month_window.js` to find the previous month and its Slack timestamps, writes the audit
into `audits/` in the format the parser expects, and checks its own counts. Then `git add`,
commit and push as above.

## Dashboard extras

- Cards show the change versus the previous month and a 75% target (`TARGET` at the top of the script in `index.html`).
- Click a bar to filter to that month; the rating-mix chart and "Needs attention" list follow the filter.
- "Count each ticket once" removes repeat audits of the same ticket.
- The data-quality panel flags repeats, unrated tickets, placeholder titles and generic titles.
- Click a ticket title to read the conclusion, outcome and notes. Sort by any column. Export the current view as CSV.
- The URL hash keeps the current filters, so a view can be shared as a link.
