# Investigator Accuracy Dashboard — Documentation

Last updated: August 2026

---

## What This Is

A self-updating GitHub Pages dashboard that tracks the TE Investigator (Freshservice AI) accuracy
across monthly audit sessions. Drop a new `.md` audit file into `audits/`, push it — the dashboard
rebuilds itself automatically. No AI credits spent on the update step.

Live URL: `https://sathwika0325.github.io/investigator-accuracy-dashboard/`

---

## How to Add a New Month's Audit (manual flow)

1. Run the Kiro prompt (see section below) to generate the `.md` file.
2. Copy the file into `audits/` — name it `investigator_accuracy_audit_<month><year>.md`
   e.g. `investigator_accuracy_audit_september2026.md`
3. Push to `main`:

```bash
git add audits/
git commit -m "Add September 2026 accuracy audit"
git push
```

The `update-dashboard.yml` workflow triggers automatically, regenerates
`data/accuracy_data.json`, and redeploys the Pages site. Takes under a minute.

---

## Audit File Format (standard — all files must use this)

Every audit `.md` must follow this structure exactly so the parser works:

```markdown
# TE Investigator Accuracy Audit — <Month> <Year>

**Period:** <Month> 1–31, <Year>

<optional intro paragraph>

---

## 1. Ticket #<ID> — <Subject>

**Investigator's Conclusion:** <2-3 sentence summary of what the AI said>

**Actual Outcome:** <2-3 sentences on what actually happened / how resolved>

**Accuracy:** <Accurate|Partially Accurate|Inaccurate> (<NN>%)

**Notes:** <1-2 sentences on key gaps or strengths>

---

## 2. Ticket #<ID> — <Subject>
...
```

**Key rules:**
- Title line must start with `# ` (single hash)
- `**Period:**` line must be present for the dashboard to label the period correctly
- Ticket headers must be `## N. Ticket #ID — Title` (double hash, em-dash or hyphen)
- `**Accuracy:** Label (NN%)` — bold, label then percentage in parentheses
- All field labels must be `**bold:**`

---

## Kiro Prompt — Generate Monthly Audit File

Use this prompt in Kiro every month. Edit the three values at the top
(`MONTH_NAME`, `oldest`, `latest`) and the rest runs automatically.

```
You are auditing the TE Investigator's accuracy for <MONTH_NAME> <YEAR>.

## Setup (do this ONCE, first turn)

1. Get channel history from `#investigator-findings` for <MONTH_NAME> <YEAR>:
   - Channel: C0AKY9ABMKP
   - oldest: <UNIX_TIMESTAMP_START>
   - latest: <UNIX_TIMESTAMP_END>
   - limit: 100
   This gives you ALL ticket numbers for the month. Extract them in
   chronological order (oldest first).

2. NOTE: Slack thread text is ALWAYS empty for this channel.
   Do NOT fetch any Slack threads.
   The investigator's conclusions are ONLY on the Fresh Service tickets
   as `[AI Comment]` internal notes.

## Processing (batch aggressively)

For each ticket number from step 1, fetch the Fresh Service ticket with
`include=conversations`. Process in batches of 5 tickets per turn
(call all 5 in parallel).

From each ticket response, extract:
- **Subject** (from `subject` field)
- **Investigator's conclusion** (the conversation entry from
  `user_id: 10002980302` with `[AI Comment]` prefix — summarize in 2-3 sentences)
- **Actual outcome** (from the remaining conversation — what actually
  happened / how it was resolved)
- **Accuracy rating**:
    - Accurate: 85–100%
    - Partially Accurate: 50–75%
    - Inaccurate: <50%

If NO `[AI Comment]` exists from user 10002980302, flag it and move on.

## Output format

Write ALL results to a single markdown file
`investigator_accuracy_audit_<month><year>.md` using EXACTLY this format:

---

# TE Investigator Accuracy Audit — <Month> <Year>

**Period:** <Month> 1–31, <Year>

---

## 1. Ticket #<ID> — <Subject>

**Investigator's Conclusion:** <2-3 sentences>

**Actual Outcome:** <2-3 sentences>

**Accuracy:** <Label> (<NN>%)

**Notes:** <1-2 sentences>

---

(repeat for every ticket)

---

At the end, add:
- Summary Statistics table (total, accurate %, partially accurate, inaccurate, average)
- Key Observations section (patterns across the full set)

## Rules to minimise turns

- Do NOT fetch Slack threads — they are always empty
- Fetch 5 Fresh Service tickets per parallel call (never 1 at a time)
- Write to the markdown file in large batches (10+ tickets at once), not one by one
- Do NOT re-fetch any ticket for any reason
- If a ticket has no AI comment, flag it in one line and move on
- Keep summaries concise (2-3 sentences max per field)
- Use a sub-agent for bulk processing if possible
```

### Unix timestamps for upcoming months

| Month | oldest | latest |
|---|---|---|
| July 2026 | 1782864000 | 1785542400 |
| August 2026 | 1785542400 | 1788220800 |
| September 2026 | 1788220800 | 1790812800 |
| October 2026 | 1790812800 | 1793491200 |
| November 2026 | 1793491200 | 1796083200 |
| December 2026 | 1796083200 | 1798761600 |

---

## Dashboard Features

### Period filter
Click `July 1–31, 2026` or `August 1–31, 2026` chips above the ticket table
to filter all cards, charts, and the table to that period only.
Click `All periods` to go back to the combined view.

### Rating filter
Filter by `Accurate`, `Partial`, or `Inaccurate` using the rating chips.

### Search
Search by ticket number or title text.

### Charts
- **Accuracy distribution** — donut chart showing Accurate / Partial / Inaccurate split
- **Avg accuracy by period** — bar chart showing month-over-month trend

Both charts update live when you change the period filter.

---

## Parser — How It Works

`scripts/parse_audits.py` is a pure-regex Python script. It:

1. Scans every `.md` file in `audits/`
2. Extracts the title, period, and all ticket blocks
3. From each ticket block, extracts: ticket ID, title, accuracy label, accuracy %, conclusion, actual outcome, notes
4. Writes everything to `data/accuracy_data.json`

The parser is run automatically by the GitHub Actions workflow on every push
that touches `audits/**.md` or `scripts/parse_audits.py`.

**If a future audit's format drifts**, update the regexes at the top of
`parse_audits.py` — the dashboard and workflow don't need to change.

---

## Findings & Changes Log

### August 2026 — Parser format fix

**Problem:** The August audit file used a different format from July:
- Section headers were `1. Ticket #ID` (no `##`)
- Separators were `==` instead of `---`
- Field labels were plain text instead of `**bold:**`

**Result:** Every August ticket showed `n/a%` on the dashboard.

**Fix applied:**
1. Converted `investigator_accuracy_audit_august2026.md` to the standard format
   using an automated script (search-and-replace, no content changed).
2. Reverted `parse_audits.py` to the clean single-format version.

**Going forward:** Always use the standard format above when generating audit files.
The Kiro prompt in this document produces the correct format.

---

### August 2026 — Dashboard improvements

- **Period filter chips** added above the ticket table — click a period to filter
  all cards, charts, and the table to that period only.
- **Charts replaced** — Chart.js CDN was blocked on the corporate network, causing
  blank chart panels. Charts are now drawn with inline SVG (no external dependency).
  They always render regardless of network/firewall restrictions.
- **Summary cards update** live when the period filter is changed.
- **Row count** shown below the ticket table.
- **Accuracy % colored** green / amber / red in the table.

---

## Local Preview

```bash
cd dashboard-repo
python3 scripts/parse_audits.py       # regenerate data/accuracy_data.json
python3 -m http.server 8000           # serve locally
# open http://localhost:8000
```

A local `file://` open won't work — `fetch()` needs an HTTP server.
