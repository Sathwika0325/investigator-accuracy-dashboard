# Monthly audit prompt for Kiro

Paste the block below into Kiro on the last day of each month (or any day after it). It needs no editing: Kiro works out
which month to audit, writes the file in the format the parser expects and puts it in `audits/`.
Pushing to `main` is the only step left, and it is yours.

On the last day of a month it audits that month; on any other day it audits the previous month.
To audit a specific month instead, add this line at the very top:
`Audit month: 2026-08`

---

```
You are auditing the TE Investigator's accuracy for one calendar month. This repo is the
investigator-accuracy-dashboard; work from its root.

## Step 0 - Work out the month (no questions, no hard-coded dates)

Run `node scripts/month_window.js` (add the month, for example `2026-08`, if I gave an
"Audit month" line). It prints JSON with month_name, year, period, oldest, latest and file.
Use those values everywhere below. If the script cannot run, compute them yourself in UTC:
oldest = first second of the month, latest = first second of the next month.

If `audits/<file>` already exists, stop and tell me. Do not overwrite a past audit.

## Step 1 - Collect ticket numbers (once)

Read #investigator-findings (channel C0AKY9ABMKP) with limit 100, oldest and latest from step 0.
If the response has a cursor or says there are more messages, keep paging until there are none.
Extract every Freshservice ticket number, oldest first, and drop repeats within the month.
Never fetch Slack threads: their text is always empty. The investigator's conclusions live only on
the Freshservice ticket, as internal notes starting with `[AI Comment]`.

## Step 2 - Fetch and rate (delegate to ONE sub-agent if you can)

For each ticket, fetch it from Freshservice with include=conversations, 5 tickets per parallel
call. Never re-fetch a ticket. Extract:
- Subject
- Investigator's conclusion: the `[AI Comment]` note from user_id 10002980302, in 2-3 sentences
- Actual outcome: what the rest of the conversation shows happened, in 2-3 sentences
- Accuracy rating: Accurate 85-100, Partially Accurate 50-84, Inaccurate under 50
  Rate the diagnosis against what the team confirmed. If nobody confirmed anything, say so in the
  notes and rate the strength of the analysis, not a guess.

Edge cases:
- No `[AI Comment]` from that user: write the ticket section but omit the Accuracy line, and say
  "No AI comment" in Notes. The dashboard shows it as unrated.
- Ticket cannot be fetched (403, deleted): use the title `[FAILED TO FETCH]`, no Accuracy line.
- A ticket you can see was already audited in an earlier month: still audit it, and add
  "Also audited in <month>" to Notes.

## Step 3 - Write the file

Write `audits/<file>` with EXACTLY this structure. The parser is regex based, so do not change
the heading levels, the em dash or the bold labels.

# TE Investigator Accuracy Audit — <Month> <Year>

**Period:** <period from step 0>

<one short intro sentence>

---

## 1. Ticket #<id> — <subject>

**Investigator's Conclusion:** <2-3 sentences>

**Actual Outcome:** <2-3 sentences>

**Accuracy:** <Accurate|Partially Accurate|Inaccurate> (<NN>%)

**Notes:** <1-2 sentences>

---

(repeat for every ticket, numbered 1..N in chronological order)

After the last ticket add:
## Summary Statistics   - a table: total, rated, accurate (count and %), partially accurate,
                           inaccurate, without AI comment, failed to fetch, average accuracy
## Key Observations     - 4-6 bullets: what the AI did well, the most common failure pattern,
                           and any ticket families that clustered this month

Write the file in large batches (10+ tickets per write), not one ticket at a time.

## Step 4 - Self-check, then stop

Before finishing, verify and report in 5 lines or fewer:
- the number of `## N. Ticket #` headings equals the ticket count from step 1
- the average in the summary equals the mean of the individual percentages
- how many tickets had no AI comment and how many failed to fetch
Do not run git. Tell me the file is ready to commit with:
  git add audits/<file> && git commit -m "Add <Month> <Year> accuracy audit" && git push
```
