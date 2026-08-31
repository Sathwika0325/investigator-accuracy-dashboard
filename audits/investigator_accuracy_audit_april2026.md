# TE Investigator Accuracy Audit — April 2026

**Period:** April 1–30, 2026

This audit scores each `[AI Comment]` posted by the TE Investigator (user 10002980302) on Freshservice tickets during April 2026 against the actual outcome documented in the ticket — developer findings, staging reproductions, applied fixes, and requester confirmations. April 2026 was the TE Investigator's initial pilot period: the system did not begin posting at volume until May 1, 2026 (the May audit opens at ticket #79712 with 92 comments). Because the #investigator-findings Slack channel history does not extend back into April, the April dataset was reconstructed by enumerating April-created Freshservice tickets in descending ID order and inspecting each for a private `[AI Comment]` from user 10002980302. The only AI comments found in April fell on April 29, 2026, immediately before the May 1 ramp — three in total. Tickets without an AI comment are not scored (consistent with the May methodology, which scores only the Investigator's own comments). Accuracy buckets: Accurate (≥85%), Partially Accurate (50–84%), Inaccurate (<50%).

---

## 1. Ticket #79654 — Meta & Insomnia backordering disabled yet orders happen
**Investigator's Conclusion:** Identified a gap between the site-level `backorder_enabled = false` setting and a per-variant `backorder_inventory` counter, laying out three pathways by which backorders could still occur despite the site flag being off — most notably a post-order manual inventory adjustment driving inventory negative without the flag being re-checked.
**Actual Outcome:** Dev confirmed pathway #1: a post-order manual inventory adjustment (by Rachel Reese on Apr 29) drove inventory negative without checking the backorder flag, exactly as the AI described.
**Accuracy:** Accurate (90%)
**Notes:** Deep, DB-backed analysis; the confirmed cause matched the AI's primary pathway.

## 2. Ticket #79660 — Cannot move cart items to project in Hub
**Investigator's Conclusion:** Attributed the failure to a `sku-central-al2-prod-env` backend outage (Severe / IAM-401), framing it as a hard service outage blocking the move-to-project action.
**Actual Outcome:** The agent's "move a few at a time" workaround worked immediately, which points to a batch-size/timeout limitation rather than a hard backend outage. The specific outage root cause was not confirmed.
**Accuracy:** Partially Accurate (65%)
**Notes:** Right subsystem, but the "hard outage" framing was likely overstated; the successful incremental workaround contradicts a full outage. Unconfirmed.

## 3. Ticket #79687 — Customer unable to remove cart item
**Investigator's Conclusion:** Diagnosed that the frontend was sending a stale/nonexistent cart item id (5942820) versus the actual cart item (6084351), producing a Spring `findById` null error on removal; also flagged that a helpdesk "removed" claim was contradicted by the database state.
**Actual Outcome:** Deep, DB-backed diagnosis consistent with the observed error, but the customer went unresponsive and there was no explicit developer/requester confirmation of the fix.
**Accuracy:** Accurate (85%)
**Notes:** Strong, evidence-based root cause with exact IDs; docked slightly for lack of a confirming close-out.

---

## Summary Statistics

| Bucket | Count | Percentage |
| --- | --- | --- |
| Accurate (≥85%) | 2 | 66.7% |
| Partially Accurate (50–84%) | 1 | 33.3% |
| Inaccurate (<50%) | 0 | 0.0% |
| **Total scored** | **3** | **100%** |

**Average accuracy score:** ~80.0%

Note: April 2026 was the TE Investigator's pilot month. Only three `[AI Comment]` entries were posted during April — all on April 29, 2026 — and all three are scored above. The much larger May 2026 volume (92 comments starting May 1 at ticket #79712) reflects the system's move to full production. April-created tickets without an AI comment (the vast majority — configuration changes, product setups, access requests, Pace ERP admin tasks, and human-handled incidents) are correctly excluded from scoring.

## Key Observations

- **April was a limited pilot.** The Investigator posted only three comments all month, clustered on April 29 — the day before the May 1 production ramp. This is the earliest activity on record; there is no earlier audit month.

- **Strong on deep, DB-backed cart/inventory diagnoses.** Both Accurate cases (#79654 backorder flag vs. per-variant counter, #79687 stale cart-item id vs. actual id with the Spring `findById` null error) traced concrete database state to the exact records involved. #79654 was explicitly confirmed by dev.

- **The one partial case shows the recurring "overstated single root cause" pattern later seen in May.** On #79660 the Investigator called a hard `sku-central` backend outage, but the immediate success of a "move a few at a time" workaround indicates a batch/timeout limitation instead. Hedging the severity claim would have improved accuracy.

- **Confirmation gaps cap otherwise-strong comments.** #79687's diagnosis was precise but the customer went unresponsive, so it lacked an explicit confirming close-out — the reason it scored 85% rather than higher.

- **Sourcing note for future audits.** Because #investigator-findings Slack history does not reach April, this month was reconstructed directly from Freshservice by scanning April-created tickets for the Investigator's private comments. Any additional April comments outside the scanned window would be net-new; none were found in the active April 29–30 window where all three known comments reside.
