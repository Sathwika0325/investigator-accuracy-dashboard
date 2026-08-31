# TE Investigator Accuracy Audit — August 2026

**Period:** August 1–31, 2026

This report reviews each Freshservice ticket in chronological order (oldest first), comparing the TE Investigator's `[AI Comment]` conclusion against the actual outcome from the ticket conversation.

---
## 1. Ticket #84153 — Lucid sku 101408827-0002 qtys

**Investigator's Conclusion:** The AI said the inventory quantities were incorrect (actual -2, backorder 0) and recommended manually setting actual_inventory = 0 and backorder_inventory = 2 via the admin/DB. It framed the fix as a simple data correction and speculated the WMS/backorder logic mishandled the state.

**Actual Outcome:** L3 investigation found the real root cause was a double-deduction bug: shipment S2535927 was deducted twice (once at picking, once at ship) because a human re-split allocations, resetting the `picked` flag so the guard in TBGInventoryServiceImpl did not fire. Charan reverted the erroneous adjustment; backorder was disabled for the site so the requested values did not apply as the AI stated.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI correctly flagged the negative inventory and hinted at faulty deduction logic, but its proposed fix values were wrong (backorder disabled) and it missed the actual double-deduction root cause.

---
## 2. Ticket #84195 — Not able to apply print points at checkout

**Investigator's Conclusion:** The AI concluded the 1,553,444-point redemption was cancelled/rolled back ~5 minutes before order 2034203 was submitted (points fully restored, no discount applied), speculating a user navigation, session timeout, or UI error caused the rollback. It recommended a manual $15,534.44 adjustment.

**Actual Outcome:** L3 confirmed the redemption coupon jrdotLcA was auto-generated and the apply step failed with an InvalidRequestParameterException, causing a rollback — matching the AI's high-level picture. Fix was a manual $15,534.44 adjustment on the order. The user noted this had happened twice with large point amounts; root cause of the exception was not fully resolved.

**Accuracy:** Accurate (85%)

**Notes:** The AI correctly traced the cancelled/rolled-back redemption and recommended the exact manual fix that was applied; it attributed the cause to user/session rather than the specific InvalidRequestParameterException the L3 identified.

---
## 3. Ticket #84199 — Kohler - Incorrect pricing presenting on orders originating from Configurator

**Investigator's Conclusion:** The AI concluded the price variance originated in the Configurator/BOM Builder upstream of Collaterate, arguing the Configurator submits different per-line prices and Collaterate faithfully records them. It recommended engaging the Configurator team and possibly enforcing a flat price on the share.

**Actual Outcome:** L3 identified the opposite root cause — the defect is in the Collaterate Java monolith: a missing else branch in TBGStorePluginPage.addOrUpdateCart drops the Configurator's price override when session quote data is absent, persisting a stale $69.50 fallback. The Configurator was explicitly ruled out; enforcing a flat price was explicitly rejected as it would break correct lines.

**Accuracy:** Inaccurate (25%)

**Notes:** The AI pointed the finger at the Configurator and suggested a flat-price fix, both of which L3 directly refuted. It correctly identified the affected product/share and confirmed pricing wasn't a data issue, but the core root-cause direction was wrong.

---
## 4. Ticket #84206 — Difficulty Accessing The Loop via TBG MCP Server

**Investigator's Conclusion:** The AI concluded The Loop linking was failing because the required Secrets Manager secret (THELOOP_SECRET_ARN) appeared missing/undiscoverable, recommending verification of the env var, secret contents, WordPress Application Passwords config, and callback URL.

**Actual Outcome:** An agent tested linking their own account successfully, proving the secret and callback setup were fine. The issue was specific to the original user's account (WordPress access/cookie/expired link). Dan R helped the user resolve it directly; ticket closed.

**Accuracy:** Inaccurate (20%)

**Notes:** The AI's central hypothesis (missing secret / broken infrastructure) was disproven — linking worked fine for others. The "secret not found" was a search-tooling limitation, not an actual misconfiguration.

---
## 5. Ticket #84213 — Instant Quote Not Appearing for New SPDC Product

**Investigator's Conclusion:** The AI concluded the instant quote failed due to missing product variant configuration (zero system_offering_variants) and a possible pricing classification mismatch, recommending adding variants and verifying classification ID 5713.

**Actual Outcome:** The backend was actually returning the correct price ($202.46); changing quantity made the quote appear, indicating a front-end rendering/timing issue in calculatorMods.js (listener not registered before the initial QUOTE_SET event / #lfCalculator container targeting). Patrick fixed it as a front-end issue.

**Accuracy:** Inaccurate (25%)

**Notes:** The AI misdiagnosed a front-end rendering bug as a missing-data/config problem. The pricing data was actually present and correct, contradicting the AI's variant/classification theory.

---
## 6. Ticket #84224 — Custom Quote Error

**Investigator's Conclusion:** The AI said it could not definitively locate custom quote e08c-210726, guessed the closest match was an expired Oct 2025 project, speculated the confirmation email fired from a pre-order webhook, and recommended escalation, checking admin, and verifying no charge in Braintree.

**Actual Outcome:** L3 located the exact quote and the specific prod error in CloudWatch: "Unable to create new order ledger" (ServiceException) on the order POST for user natalie.langhorne on icprintstore.com. The customer used Terms payment and selected only 6 partial items; investigation continued with the exact timeframe/order identified.

**Accuracy:** Inaccurate (30%)

**Notes:** The AI failed to locate the quote and its expired-project guess was a dead end. It did correctly surmise the order was never created and suggested checking CloudWatch logs, which is where the actual error was found.

---
## 7. Ticket #84220 — Unable to share projects with others in Hub

**Investigator's Conclusion:** The AI concluded Laura Belz's missing Client/Share toolbar options stemmed from her site 196 account having no site role (site 57 was fine), recommending an admin add a sharing role on site 196 and confirm which site she was using.

**Actual Outcome:** Sheila resolved it by updating Laura's credentials/permissions ("Your credentials have been updated"); the user accepted and planned to test. The fix was a straightforward permission/credential update, broadly consistent with a role/permissions issue.

**Accuracy:** Partially Accurate (65%)

**Notes:** The AI correctly identified this as a role/permissions issue (not a bug), which matched the resolution, but its specific site-196 diagnosis was never confirmed and the actual fix was a general credential update by the agent before the AI comment posted.

---
## 8. Ticket #84266 — Unable to Remove New File Alert from Job

**Investigator's Conclusion:** The AI concluded order_items.flagged_for_new_file_upload = true on job 4542691 was blocking the new file queue with no UI path to clear it, and recommended a developer run an UPDATE to set flagged_for_new_file_upload = false and issue_flag = false on order_item id 6287782.

**Actual Outcome:** The team followed exactly this — CJ ran the precise UPDATE (flagged_for_new_file_upload = FALSE, issue_flag = FALSE WHERE id = 6287782). The requester confirmed the alert was removed from the queue.

**Accuracy:** Accurate (95%)

**Notes:** The AI's diagnosis and the exact SQL fix were adopted verbatim by the dev team and resolved the ticket. Strong match between recommendation and outcome.

---
## 9. Ticket #84273 — Unable to void shipment

**Investigator's Conclusion:** The AI concluded the void was blocked because shipment S-2537685 had shipment_created = true and all 3 jobs shipped = true after Rachel walked back only the order status. It recommended a developer reset shipment_created/enabled = false and order_items shipped = false / shipped_on = null.

**Actual Outcome:** CJ ran SQL to reopen the shipment (shipment_created = FALSE on order_shipments; shipped = FALSE on order_items), which matched the AI's recommendation closely. The requester confirmed it worked. CJ noted the void behavior seemed strange since voiding is a common process.

**Accuracy:** Accurate (90%)

**Notes:** The AI's root-cause and remediation matched what the dev executed. Minor gap: the AI recommended also setting enabled = false, which the dev did not include, and the underlying "why is void blocked" question remained open.

---
## 10. Ticket #84297 — Hub - Need Braille product set up

**Investigator's Conclusion:** The AI concluded Brian Cathers lacked assignment to the "Braille" segment (ID 826) controlling the "Braille Sign" product, recommending an admin add him to segment 826 and verify related sub-segments.

**Actual Outcome:** Sheila first granted Braille product access, but the user clarified he needed a specific Fairview-configured Braille Sign offering. Sheila then corrected the access and the user was set up. The resolution was a segment/product access grant, consistent with the AI's permissions diagnosis.

**Accuracy:** Accurate (85%)

**Notes:** The AI correctly identified this as a segment/product-visibility permission issue and the fix was an access grant. It couldn't anticipate the specific Fairview offering nuance that required a second correction.

---
## 11. Ticket #84322 — Instant Reorder not properly pulling files through

**Investigator's Conclusion:** The AI concluded job 4475937's instant reorder failed to copy the print file at order creation (proof copied fine), calling it an isolated anomaly where zero files copied silently with no error logged; it recommended an engineering investigation, adding error logging, and noted no systemic outage.

**Actual Outcome:** The team could not reproduce it in staging/test and found no error; they confirmed the file was successfully copied but couldn't explain why it didn't land on the 58-day-old order. It was deemed a likely one-time issue and the ticket was closed with a request to report recurrences.

**Accuracy:** Accurate (85%)

**Notes:** The AI's characterization as an isolated, silent, non-reproducible file-copy miss matched the team's conclusion. Its detailed per-job table and "no systemic outage" framing aligned well with the resolution.

---
## 12. Ticket #84330 — getting error code in collaterate

**Investigator's Conclusion:** With no error code, job number, or screenshot, the AI said remote diagnosis was impossible and it was likely an isolated user issue (barcode/scanner/job-state). It recommended following up for the error code, job number, and screenshot.

**Actual Outcome:** Once the user shared a screenshot, the agent found the reporter had no producer-related access; the config team (Sheila) updated the user's Collaterate credentials/permissions to resolve it. The root cause was a permissions/access gap, not a barcode/hardware issue.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI correctly flagged insufficient detail and recommended gathering more info (which led to the fix), but none of its speculated causes matched the actual permissions/access root cause.

---
## 13. Ticket #84331 — PID# Override for double sided treated acrylic

**Investigator's Conclusion:** The AI identified this as a config request to create PID overrides 30994/30995 under Board Printing, found no matching press_sheets, and recommended creating press sheet records, linking to the *TBG Board Printing classification, and clarifying "override" meaning with the requester.

**Actual Outcome:** Sheila (config team) added the two PIDs as an override and closed the ticket. It was a routine config change, consistent with the AI's framing as an admin catalog task.

**Accuracy:** Accurate (85%)

**Notes:** The AI correctly classified it as a config task routed to the config team and the resolution was exactly adding the overrides. Its detailed table-level speculation was more than needed but not wrong.

---
## 14. Ticket #84352 — MANUALREFRESH PLEASE - Quicksight THD Retail Team Projects Dashboard

**Investigator's Conclusion:** The AI identified this as a manual QuickSight SPICE dataset refresh request ahead of a noon THD review, noted Reilly had picked it up, and recommended triggering a Refresh Now on the underlying dataset(s) in the tbg-data account.

**Actual Outcome:** Reilly Melville refreshed the dataset feeding the "Business Review" tab, and Emily confirmed it reflected what she needed. The fix was exactly the manual dataset refresh the AI described.

**Accuracy:** Accurate (90%)

**Notes:** The AI correctly diagnosed the request and the exact remediation (manual SPICE refresh) that the engineer performed. Clean match.

---
## 15. Ticket #84403 — [FAILED TO FETCH]

**Investigator's Conclusion:** N/A — ticket could not be retrieved (Freshservice API 403 access_denied).

**Actual Outcome:** N/A — not retrievable.

**Accuracy:** N/A (ticket failed to fetch)

**Notes:** Access denied by the Freshservice API; excluded from accuracy statistics.

---
## 16. Ticket #84410 — Unable to print shipping label

**Investigator's Conclusion:** The AI concluded the missing print option was because shipment S-2541688 (FC 460) used EPL thermal-format labels that can't render in the web UI, while S-2541689 (FC 627) generated a printable PNG. It called this a config situation and recommended changing the FC's label spec code and using FedEx to reprint by tracking number.

**Actual Outcome:** The team found it was actually the Pick N Transfer (FC 627) shipment that lacked the print button — the opposite shipment from the AI's read. The real cause was UI conditional logic (isShipped / hasPrintableLabels / package selection) tied to the GIF/pickup shipment; they made a config change so print labels appear for future Pick N Transfer orders, and used "View Label" as a workaround.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI correctly identified the two-FC label-format difference (EPL vs GIF) as the crux, but it inverted which shipment was affected and misattributed the missing button to EPL being unrenderable rather than the GIF/pickup shipment's UI print conditions.

---
## 17. Ticket #84411 — Jitbit access

**Investigator's Conclusion:** The AI identified this as an IT access provisioning request (CES to PC team), recommended locating the user, updating Jitbit category/department permissions, confirming read-only vs full access, and reclassifying as a Service Request.

**Actual Outcome:** The agent granted Amy full access to all Jitbit categories and promoted her to Technician; the user confirmed she had access. The resolution was a straightforward Jitbit permission update, matching the AI's diagnosis.

**Accuracy:** Accurate (90%)

**Notes:** The AI correctly identified the request type and the exact remediation path (updating Jitbit permissions). Clean, well-scoped match.

---
## 18. Ticket #84304 — Allowing RDC into the gang queue

**Investigator's Conclusion:** The AI concluded this is a feature request, not a bug: gang eligibility is controlled at production group / press sheet / substrate level, with no per-operation-item flag on RDC001. It recommended converting to a feature request and filing a TTI Jira story to add a gang_eligible flag on operation_items.

**Actual Outcome:** The config team confirmed there is no way to allow an operation item (specific RDC die) into the ganging queue and asked whether the functionality exists or is a feature request — matching the AI's conclusion. The ticket remained open (status 2) pending feature-request handling.

**Accuracy:** Accurate (85%)

**Notes:** The AI's core finding — that per-operation-item gang control doesn't exist and this needs feature development — directly matched the config team's assessment. Outcome still open but consistent.

---
## 19. Ticket #84446 — My Products- color note confusion

**Investigator's Conclusion:** The AI found the "Color Note" (special_instructions) on offering 82409 displayed on job tickets with internal reference codes, said the second URL product couldn't be found, and recommended clarifying note content with prepress/Christi, identifying the second product, and possibly toggling display_special_instructions_on_job_ticket off.

**Actual Outcome:** Christi worked through it with Jill and prepress: the underlying issue was that the color note appeared in two places (operation answer vs press), causing confusion. After several iterations moving/removing the note (operation question priority on the job ticket), Christi consolidated it to a single color-notes area per prepress preference.

**Accuracy:** Partially Accurate (65%)

**Notes:** The AI correctly identified the special_instructions/color-note display as the source of prepress confusion and that display placement was the lever, but it missed the real "shown in two places" duplication and the operation-answer vs press-note mechanics that drove the fix.

---
## 20. Ticket #84449 — Reorder indicator in Activity Log

**Investigator's Conclusion:** The AI validated the prepress pain point, explained reorder type isn't persisted/surfaced today, and tied it to in-flight Jira work (TTI-20735 to persist an exact-reorder flag, plus TTI-20734, TTI-19320). It recommended linking the ticket to TTI-20735 and expanding its scope to add an Activity Log indicator.

**Actual Outcome:** The dev (Steve Carroll, who created TTI-20735) confirmed the AI's finding was accurate and that the bot was requesting additional scope on TTI-20735; discussion with Jana/Nick ensued about adding scope without pushing the deadline. Ticket remained open as a feature-request coordination.

**Accuracy:** Accurate (90%)

**Notes:** The AI correctly connected the request to the exact existing Jira story and correctly noted the Activity Log indicator wasn't yet in scope. The dev explicitly validated the linkage and scope-expansion suggestion.

---
## 21. Ticket #84467 — I am unable to get logged into the TBG HUB site

**Investigator's Conclusion:** The AI concluded the user likely had no account (or an inactive one) on the private tbghub.com site, which is why no reset email arrived; it recommended looking up the user's email and having an admin create/reactivate the account and assign roles.

**Actual Outcome:** Sheila found the user (Deb Angell) did not have a HUB account and created one for her. This matched the AI's primary hypothesis exactly.

**Accuracy:** Accurate (90%)

**Notes:** The AI's leading hypothesis — no account on a private site — was correct, and the remediation (admin creates the account) was exactly what happened.

---
## 22. Ticket #84469 — CQ not showing for customer - WPN

**Investigator's Conclusion:** The AI could not find the two WPN quotes in QuotesTable-Prd, found no Lambda errors, and hypothesized a quote visibility/delivery issue possibly tied to email config or an expired quote, recommending direct record lookup, checking WPN email config, and reviewing the submit-to-customer flow.

**Actual Outcome:** L3 reproduced it and found the real bug: the siteUser.id stored on the DynamoDB quote record becomes mismatched with the customer's login user ID, so user-ID-based filtering hides the quote. The known workaround (same as ticket #59337) is to remove the site-user assignment so email-based access works; long-term bug TK-157 was raised.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI correctly framed it as a quote visibility/filtering issue rather than a system outage and correctly noted quotes weren't surfacing for the user, but it missed the specific siteUser.id mismatch root cause and instead speculated about email/expiry, which were off.

---
## 23. Ticket #84478 — SKU: 102403167-0001-Remove the Reserved for Orders

**Investigator's Conclusion:** The AI reported the reserved_inventory had already been corrected to 0 (from -71) by Charan before its investigation, and concluded the ticket could be closed as resolved. It provided the product/SKU details and confirmed warehouse-managed status.

**Actual Outcome:** The agent adjusted the reserved quantity and Stacy confirmed it looked good. The AI comment posted after the fix and accurately reflected that the correction was already made.

**Accuracy:** Accurate (90%)

**Notes:** The AI accurately reported the already-completed fix and correct current state. Low difficulty since it ran post-resolution, but its reporting matched reality.

---
## 24. Ticket #84491 — Kohler EDI's missing Kohler product

**Investigator's Conclusion:** The AI confirmed the EDI 850s to Kohler omitted the Elate/Rival faucet line items, listing the exact 6 missing SKUs, and concluded the omission happened upstream in Collaterate's EDI item-selection logic (a filter/eligibility condition excluding faucets), recommending corrected 850s and a review of the item-selection logic plus a broader audit.

**Actual Outcome:** Confirmed accurate. L3 (Parin) found the exact cause: EDI Enabled stored as lowercase "true" failed a case-sensitive comparison against "TRUE", so faucets were filtered out before route grouping; the EDI Route Rules were also misconfigured (edimerch/null vs edikohler). Product setup was corrected, a case-insensitive fix was tested in staging, and the missing items were handled (not resent to avoid duplicates). A follow-up AI comment even drove the delivery-address/duplicate-order clarification.

**Accuracy:** Accurate (90%)

**Notes:** The AI nailed the missing SKUs and correctly localized the root cause to upstream item-selection filtering rather than the Lambda. The precise mechanism (case-sensitive TRUE comparison) was found by L3, but the AI's direction and recommendations were on point and its follow-up comment materially advanced the resolution.

---
## 25. Ticket #84530 — Product Set Master Products Bug?

**Investigator's Conclusion:** The AI concluded the master product uses a manual FIXED_QUOTE price that does NOT auto-recalculate from children, called it "by design, not a bug," and said no code/DB logic propagates child changes to the master — recommending the reporter provide repro steps.

**Actual Outcome:** The team reproduced it and found it IS effectively a bug: all site shares share a single variant (ID 40597) because override_pricing=false, and the UI PATCHes /productVariant/40597 without a siteId, so editing any child updates the shared master variant (confirmed in ProductVariantProvider.java). The requester said this needs a dev solution so the master can hold $0 and site shares price independently.

**Accuracy:** Inaccurate (35%)

**Notes:** The AI wrongly asserted there was no propagation mechanism and that child edits couldn't affect the master, then leaned toward "by design." The team proved the exact propagation path (shared variant + missing siteId in PATCH) that the AI said didn't exist.

---
## 26. Ticket #84535 — New Customer - The HUB/PM Ordering Portal

**Investigator's Conclusion:** The AI identified this as a request to add client HTC America, Inc. (HTCAMERI) to the TBG PM Ordering Portal (site 57), confirmed the client didn't yet exist, noted the code follows conventions, and said it's a manual provisioning task with no blockers.

**Actual Outcome:** Sheila added the client and confirmed "Added!" The resolution was exactly the manual client creation the AI described.

**Accuracy:** Accurate (95%)

**Notes:** The AI correctly scoped the request, verified the client didn't exist, and identified the exact provisioning action taken. Clean match.

---
## 27. Ticket #84545 — Site update/Ticket Config - Sheet/Page

**Investigator's Conclusion:** The AI confirmed a config inconsistency where booklet products label the field "Pages" but the pages_tip expects "sheets" for some binding styles, and several Custom Quote PJCs have NULL tips. It recommended populating pages_tip, adding a contextual Sheets/Pages ticket label (dev/Jira), and separately scoping the Perfect Bound pages-to-sheets conversion.

**Actual Outcome:** The ticket was routed as a feature/dev request; an agent added Matt to look into it. No resolution yet (status open) — but the AI's framing as a legitimate config/verbiage inconsistency needing dev work aligned with how it was handled.

**Accuracy:** Accurate (85%)

**Notes:** The AI's detailed DB-backed analysis correctly characterized the sheets-vs-pages inconsistency and appropriately split it into config vs dev work. Outcome still open but consistent with the AI's direction; slight uncertainty since no fix was applied within the thread.

---
## 28. Ticket #84543 — 1785701 - Files won't drop from template

**Investigator's Conclusion:** The AI diagnosed an expired Azure Blob SAS token (expiry 2025-08-12) on the POD template URL with an ARCHIVED session, and a new rework order item (6374969) with no template/file. It recommended dev re-initializing the template session or prepress manually building/uploading the corrected file directly.

**Actual Outcome:** The team reproduced the error, confirmed the job was already shipped and this was a reprint, and Kyle (per a related prior ticket) manually created and uploaded a PDF to the job — exactly the AI's alternative recommendation of prepress building/uploading the file directly.

**Accuracy:** Accurate (85%)

**Notes:** The AI correctly identified the expired-SAS/archived-session root cause and offered the manual-upload path that the team ultimately used. Its technical read matched the reproduction; the chosen fix was the AI's second recommended option.

---
## 29. Ticket #77276 — SC work showing up in the MN queue

**Investigator's Conclusion:** This March ticket was revisited in August; the AI concluded the SC-vs-MN routing shift was caused by intentional router config changes (Texas added to SC states, plus Crump/Saybrus/DSF/HealthMarkets routing), that the referenced jobs were COMPLETE, and recommended closing the ticket.

**Actual Outcome:** The conversation history already contained the router owner's confirmation (from March) that intentional router changes caused the shift and that jobs were manually routed to SC. The August follow-up was just a close-out check; the AI accurately summarized this and recommended closure.

**Accuracy:** Accurate (90%)

**Notes:** The AI correctly synthesized the existing thread — intentional router changes, jobs complete, safe to close. Since the root cause was already documented in-ticket, the AI's value was accurate summarization rather than new discovery.

---
## 30. Ticket #84597 — Collaterate Logging Out Randomly

**Investigator's Conclusion:** The AI's first comment tied random logouts to the Aug 6 prod deploy (Build #346), flagged an empty tomcat_sessions table and Redisson session config as suspects, referenced prior TK-74, and asked for user details. A second AI comment then pivoted to a "root cause" of email-domain conflicts across 15 user records causing session validation conflicts, recommending consolidating the user's email domain.

**Actual Outcome:** The team gathered AWS logs showing SessionTracker "Session destroyed" events and noted a mismatch between the Collaterate admin email (@smartpress.com) vs the SmartPress user page (@thebernardgroup.com). Config was asked to confirm the correct domain. No confirmed root cause or fix within the thread; the AI's email-domain theory was never validated.

**Accuracy:** Partially Accurate (50%)

**Notes:** The AI surfaced useful leads (Aug 6 deploy, prior TK-74, session/Redisson, and the email-domain mismatch the team also noticed), but its confident second "root cause" (email-domain conflicts cause logouts) was speculative and unproven, and the empty tomcat_sessions finding was likely a red herring given Redisson.

---
## 31. Ticket #72650 — Product not present in press batch queue

**Investigator's Conclusion:** This Jan ticket was revisited in August; the AI concluded DQ Cake Labels can't be batched because their press sheet has gang_ready=false (expected behavior, not a bug), corroborated by Christi's note that they print on a pre-perfed Ricoh sheet with no finishing, and that all orders had shipped. It recommended closing.

**Actual Outcome:** The thread already contained Christi's Jan explanation that these labels shouldn't batch (specialty pre-perfed sheet, straight to ship). The August activity was a close-out check. The AI accurately synthesized this and recommended closure.

**Accuracy:** Accurate (90%)

**Notes:** The AI correctly identified the gang_ready=false / specialty-workflow reason (consistent with the in-ticket production note) and appropriately framed it as expected behavior ready to close.

---
## 32. Ticket #84666 — QuickSights Not Loading

**Investigator's Conclusion:** The AI concluded the Rework Summary dashboard was stale due to CJ's disabled nightly extraction (per CJ's own note), pinpointed the staging table online_stage.production_shift_stage as stuck at 2024-12-31 while the raw source was current, and recommended verifying pipeline completion and checking the staging ETL step.

**Actual Outcome:** CJ confirmed he had temporarily disabled extractions and forgot to re-enable them, re-initiated the pipeline (~1hr backfill), and Reilly later confirmed everything was fixed. The root cause matched CJ's note exactly.

**Accuracy:** Accurate (90%)

**Notes:** The AI correctly attributed staleness to the disabled pipeline (already stated by CJ) and added precise value by localizing the lag to the staging transform layer. Resolution matched.

---
## 33. Ticket #84671 — Job # 4604180 (no proofing section)

**Investigator's Conclusion:** The AI concluded the two Door Hanger jobs had proof_id/proof_status_id = NULL (standard PJC vs largeformat), a known intermittent bug, and recommended manually setting proof_id=192 and proof_status_id=1 on the affected order items, plus filing a dev ticket.

**Actual Outcome:** The team confirmed proof_id was NULL, and CJ ran the exact UPDATE (proof_id=192, proof_status_id=1 where proof_id IS NULL) on order 2105822; the proofing section reappeared and the ticket was closed.

**Accuracy:** Accurate (95%)

**Notes:** The AI's diagnosis and the precise remediation values (proof_id=192, proof_status_id=1) were adopted verbatim by the dev. Excellent match.

---
## 34. Ticket #84726 — Items priced differently after duplication in cart

**Investigator's Conclusion:** The AI concluded duplicated card items were mispriced far lower than their source at submission (a "glitch," per CSR Connor Patty's note), that the order was already corrected operationally (duplicates cancelled, originals repriced/combined), and that the underlying cart-duplication pricing bug needed a dev ticket. It theorized incorrect pricing context/quantity-break tier during duplication.

**Actual Outcome:** The team reproduced it and L3 found the precise cause: during duplication the Pricing Engine receives a null sossId, hits a 400 "Missing required parameter(s): sossId," and silently falls back to raw material cost instead of the VALUE_BASED price (ValueBasedPODWholesalePriceStrategy.java). Related to TT-325/333/343; the duplication path was never updated for the VALUE_BASED strategy. Escalated to Cameron.

**Accuracy:** Accurate (85%)

**Notes:** The AI correctly identified it as a real cart-duplication pricing bug producing too-low prices, confirmed the order was already corrected, and recommended a dev bug ticket. It didn't pinpoint the null-sossId/VALUE_BASED mechanism (found by L3), but its direction and framing were on target.

---
## 35. Ticket #84745 — Blattner - Shipping Options no longer populating

**Investigator's Conclusion:** The AI comment failed: "Investigation stopped - rds resources not found after 5 attempts." No analysis or recommendations were provided beyond that.

**Actual Outcome:** The team reproduced it and Megan (shipping) found the real cause: five Blattner banner templates have dimensional-weight defaulted ON/not-editable, and a July 22 change made the flag send real flat dimensions to FedEx, which returns "FedEx service not available to this origin/destination," leaving only "I will describe my shipping method." Workaround: use that option; business decision needed on dimensional shipping for MOD orders.

**Accuracy:** Inaccurate (0%)

**Notes:** The AI produced no usable investigation (aborted due to tooling errors), so it contributed nothing toward the actual dimensional-weight/FedEx root cause the team found. Counts as an AI comment present but effectively failed.

---
## 36. Ticket #84769 — KPI Tracking & Dashboard Creation

**Investigator's Conclusion:** The AI framed this as a feature/build request to automate the Prepress KPI dashboard, inventoried the available data sources (v_production_queue, production_tasks, Redshift coll_src, existing QuickSight), flagged that queue snapshots aren't captured historically and KPI labels need mapping, and recommended routing to TTI with a phased QuickSight/Redash approach.

**Actual Outcome:** The ticket was escalated/open as a feature request (status 2) with no resolution captured in the thread. There were no substantive human replies to validate or contradict the AI's infrastructure analysis within the conversation.

**Accuracy:** Accurate (80%)

**Notes:** The AI correctly classified this as a build request and produced a thorough, plausible data-infrastructure plan aligned to how such work would be routed. Rated slightly lower because there's no human outcome to confirm the specifics, but nothing contradicts it.

---
## 37. Ticket #84779 — Unexpected error (job location)

**Investigator's Conclusion:** The AI tied the "unexpected error" opening Job Location to a PostgreSQL "Cannot change transaction read-only property" error in TbgProductionCalendarService.getEstimatedDeliveryDate(), plus a related UpdateJobLocation Lambda failing against Pace (503s). It recommended a dev fix to the transaction propagation and investigating Pace 503s.

**Actual Outcome:** The team reproduced it and found the real cause was a missing permission — the user lacked the Producer User permission. Adding that permission resolved the error; config was asked to grant it to the user.

**Accuracy:** Inaccurate (25%)

**Notes:** The AI latched onto a coincidental prod DB error and an unrelated Pace Lambda issue, presenting a complex code-level root cause. The actual fix was a simple per-user Producer permission grant, which the AI never considered.

---
## 38. Ticket #84792 — Soft Proof Received for Cancelled Order

**Investigator's Conclusion:** The AI confirmed a real bug: updateProofStatus in RegularOrderItemV2Provider.java has no isCancelled() guard, so a cancelled item (job 4590429, proof_status_id=2) fired a "Pending Review" notification. It noted a dev had already reproduced it and was fixing locally, recommended a TTI ticket, an early isCancelled() check, guarding other proof entry points, and possibly correcting the stale status.

**Actual Outcome:** The team confirmed exactly this — RegularOrderItemV2Provider.java lacked cancelled-item validation in updateProofStatus; reproduced in staging; a fix with the isCancelled guard was developed and a PR (#7393) was later created (V1 first, V2 to follow). Matches the AI's root cause and recommended fix precisely.

**Accuracy:** Accurate (95%)

**Notes:** The AI pinpointed the exact method, missing guard, and fix approach that the dev implemented, and correctly noted the multiple proof-status entry points needing the same guard. Very strong.

---
## 39. Ticket #84807 — Fwd: Invoice L2037583 (line artifact on invoices)

**Investigator's Conclusion:** The AI summarized this as a billing/ops issue: a horizontal line artifact across 23 Scheels invoices breaking their OCR, noted Jason Bierschbach (ERP) had already said it should be fixed and offered to resend, identified the "L" prefix as a Pace/ERP job (not Collaterate), and recommended confirming the resend and checking the Pace invoice PDF template.

**Actual Outcome:** Jason Bierschbach replied that it should be fixed now and offered to resend the batch — exactly what the AI reported. The issue was an ERP/Pace invoice-rendering artifact, consistent with the AI's read; ticket resolved.

**Accuracy:** Accurate (85%)

**Notes:** The AI correctly characterized this as an ERP/Pace invoice rendering issue already being handled by the ERP admin, and correctly noted it wasn't a Collaterate platform problem. Low-difficulty (fix was already stated) but accurate.

---
## 40. Ticket #84821 — Custom Quote page (customer only receives disclaimer, not the quote)

**Investigator's Conclusion:** The AI concluded the "Submit to Customer" email was missing line items, offering two hypotheses: (1) visibleOnSalesEstimate flags hiding items, or (2) a backend email template rendering bug. It recommended checking item visibility, inspecting the DB, and reviewing the server-side template.

**Actual Outcome:** L3 traced it to EmailService in sls-custom-quotes-service: the email handler passes project: null (doesn't fetch project-with-items), so the template's project?... conditional renders nothing — line items/pricing are omitted. Separately, Cameron found the specific quote was assigned "Anonymously" (site-user flag off), so the customer couldn't see it in their Quotes section, with a known workaround.

**Accuracy:** Partially Accurate (60%)

**Notes:** The AI correctly identified it as a backend email-rendering issue (one of its two hypotheses) and correctly flagged the quote-visibility/assignment angle that Cameron ultimately acted on. It didn't pinpoint the null-project handler bug, and its visibleOnSalesEstimate theory wasn't the cause.

---
## 41. Ticket #84842 — Collaterate uploads are spinning

**Investigator's Conclusion:** The AI concluded two proof uploads were stuck at "Not Created" because the proof-trigger event was dropped/never fired for those specific jobs (files in NORMAL vault state, instant-proof service healthy, siblings proofed fine), framing it as a job-specific trigger failure and recommending manual re-trigger and DLQ inspection.

**Actual Outcome:** The team couldn't reproduce in staging; the requester deactivated and re-uploaded the spinning files, which then completed. Per the related ticket 84843, the real cause was a transient spike in async event processing (~3–3:30pm) that delayed events up to ~10 min and self-resolved — files just needed time to process.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI correctly localized the failure to the proof/event-processing path and that uploads themselves succeeded, but it framed it as a permanently dropped per-job trigger rather than the transient async-event backlog that was the actual (self-resolving) cause. Re-upload/time resolved it, not a manual dev re-trigger.

---
## 42. Ticket #84843 — New file Uploads Are Spinning in Collaterate

**Investigator's Conclusion:** The AI concluded the spinning uploads were caused by two failing SQS queues in Prd-Prv-UE1-PaceFileSystem (ContentFileCreate-DLQ 158 msgs, PaceLinker-DLQ 35 msgs, both in ALARM), recommending investigation of those handler logs, DLQ peeks, checking for a recent deploy, and redriving the DLQs.

**Actual Outcome:** Dev (Steve Carroll) found the real cause: a spike of async events between ~3–3:30pm slowed processing (slowest ~10m15s), tied to a "Too many Async Events pending" Zabbix alert; it resolved by 3:30pm on its own. No files needed re-uploading — they just needed time to process. (The AI's cited example jobs were even noted as being from 2021.)

**Accuracy:** Partially Accurate (50%)

**Notes:** The AI correctly identified a queue/async-processing backlog as the cause and that it was downstream of successful uploads, but it fixated on specific PaceFileSystem DLQs as the culprit rather than the broad async-event/S3 processing spike Steve identified, and it recommended a DLQ redrive when the backlog actually self-cleared with time.

---
## 43. Ticket #84845 — Kohler Quick Ship - Inventory adjustment for a product

**Investigator's Conclusion:** The AI concluded SKU 102285922-0001 went negative (actual -1, reserved -1) due to a double-deduction on shipment S-2537785 (pick event -1 and shipment-confirmed -1), recommended a +1 correction to actual (and reserved) with an audit adjustment record, and flagged the double-deduction pattern for dev review.

**Actual Outcome:** The agent adjusted the inventory to 0 available and the requester confirmed. The correction matched the AI's recommendation, and the double-deduction root cause is consistent with the same class of bug seen in ticket #84153.

**Accuracy:** Accurate (90%)

**Notes:** The AI's double-deduction diagnosis and the +1 correction it recommended aligned with the fix applied. Strong, and consistent with the known shipment double-deduction pattern.

---
## 44. Ticket #84847 — Collaterate and Hub proofs are not loading

**Investigator's Conclusion:** The AI concluded proofs weren't loading because 5 of 7 jobs had offsite_storage_requests stuck in NEW (stored_offsite=false), blaming the collaterate-vault-mover pipeline: 0 SQS messages since Aug 15, 0 Lambda invocations, 1,967 stuck NEW requests — a system-wide SQS-enqueue failure. It recommended engineering escalation, checking for an Aug 17 deploy, and re-enqueuing.

**Actual Outcome:** The same-day resolution (shared across the spinning-upload tickets) was a transient async-event/vault processing backlog that cleared with time; the requester had prepress re-upload the files, which then loaded. Per ticket 84843, no re-upload was strictly necessary — the backlog self-resolved. The AI's "systemic, needs a deploy fix + manual re-enqueue" framing overstated a transient condition.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI's per-job stored_offsite breakdown precisely matched the symptom (only 4612171/4612176 loaded), and it correctly identified the offsite-storage/vault-mover pipeline backlog. But it characterized a transient async processing spike as a persistent 1,967-record systemic outage requiring a deploy fix, when it actually cleared on its own with time.

---
## 45. Ticket #84856 — Missing Toolkit Order - 103-1774407

**Investigator's Conclusion:** The AI concluded order 103-1774407/4624368 was never created due to a June 12 UHG intake Lambda validation error ("payments field required") that rejected the XML file, listed the successfully processed orders, and recommended retrieving the failed XML from S3, manual creation, auditing other June 12 failures, and confirming the July 23 fix.

**Actual Outcome:** L3 (Parin) reprocessed the order and it was created successfully ("[PROD] New UHG Order #103-1774407 - #4624368 created"); the requester confirmed it came through. The order was recoverable/reprocessable, consistent with the AI's finding that it failed intake and needed reprocessing.

**Accuracy:** Accurate (85%)

**Notes:** The AI correctly determined the order failed at UHG intake and never reached Collaterate, and reprocessing resolved it. It recommended manual re-entry; the dev instead simply reprocessed it, which is a cleaner version of the same fix.

---
## 46. Ticket #84872 — Dairy Queen Shipping cost issue

**Investigator's Conclusion:** The AI concluded the shipping spike was a split-shipment scenario — the Bollard Sign (FC 5) and Fries (per AI, FC 460) shipping from different fulfillment centers, forcing two FedEx quotes — and recommended reassigning the FC, a flat-rate override, or setting a product weight.

**Actual Outcome:** The team found the AI's FC premise was wrong — both flagged products (and most others) actually ship from Large Format - MN, so split-shipment wasn't the cause. Megan identified it as the recently launched dimensional-weight functionality; DIM weight quotes were turned off for DQ pending a secondary fix.

**Accuracy:** Inaccurate (30%)

**Notes:** The AI's core "split-shipment across FCs" theory was refuted by the team's FC audit (the products share an FC), and its FC-460 assignment for the Fries item was incorrect. It did note the missing product weight / dimensional angle in passing, which is closer to the true dimensional-weight cause, but the primary diagnosis was wrong.

---
## 47. Ticket #84880 — Quick Suites

**Investigator's Conclusion:** The AI interpreted "Quick Suites" as a third-party SaaS app outside TBG's infrastructure (not in service catalog/Confluence/Jira/Slack/AWS), and recommended finding the app owner, checking spam, and provisioning/inviting the user's email.

**Actual Outcome:** "Quick Suites" was actually QuickSight — the user had no QuickSight account (which must be provisioned manually). Reilly created the account and granted the requested dashboards (SF Production Tasks, Online Production Dashboard, Runtime Forecast, Rework Summary).

**Accuracy:** Inaccurate (20%)

**Notes:** The AI misread "Quick Suites" as an unknown third-party product rather than recognizing the near-certain QuickSight typo, and concluded it was outside TBG infrastructure. The generic "invite-only, check spam, find the owner" advice was tangential; the real fix was provisioning a QuickSight account.

---
## 48. Ticket #84905 — Having Issues with Producer

**Investigator's Conclusion:** The AI framed a Producer queue-count mismatch (43 to print vs 7 actual, plus ganged jobs appearing in both queues) as a Producer queue-state synchronization issue with ganged jobs, recommending escalation to the Producer team, confirming whether ganged jobs completed, a refresh/cache clear, and possibly filing a PRD Jira bug.

**Actual Outcome:** The requester replied "Issues solved thanks" before providing a screenshot or further detail — no root cause was captured. The quick self-resolution is loosely consistent with the AI's "display/state, try a refresh" framing, but nothing confirmed the specific ganging-sync theory.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI reasonably characterized it as a Producer display/queue-state issue (not an outage) and suggested a refresh, and the issue resolved quickly. But with no confirmed cause, the specific ganging-synchronization root cause can't be validated.

---
## 49. Ticket #84919 — Unable to View Tax Exemption Images

**Investigator's Conclusion:** The AI confirmed the tax-exemption image files exist in S3 (migration SUCCESS) and concluded "Unable to retrieve image" was an app-layer presigned-URL / S3 access problem — most likely the CollaterateAppServer_Prod IAM role losing s3:GetObject — recommending IAM/CloudTrail/app-log checks. It stated no data remediation was needed.

**Actual Outcome:** The real cause was user permissions: Jami Dixon lacked the User and Division (Manager) role that a colleague (Hailey, who could view the image) had. Assigning the user/division role let her open the image. It was a per-user permission gap, not an IAM/S3 infrastructure issue.

**Accuracy:** Inaccurate (25%)

**Notes:** The AI over-indexed on an infrastructure/IAM presigned-URL theory and even asserted "make sure I still have the appropriate access" was not the issue — but the ticket's own wording (and the fact a coworker could view it) pointed to a per-user Collaterate role gap, which was the actual fix.

---
## 50. Ticket #84997 — Need MyProduct Files - 2041281

**Investigator's Conclusion:** The AI concluded the 3 DwyerOmega jobs were stalled because no print files were uploaded (proof status "Not Created," no files in DB), reframed the request as a file-upload/responsibility issue, and recommended verifying whether Business Hub templates should auto-attach or having the customer/config upload the artwork.

**Actual Outcome:** The config team uploaded files for all three jobs (4598391, 4598394, 4598395), resolving the stall. This matches the AI's core finding that the jobs lacked uploaded files and needed them supplied.

**Accuracy:** Accurate (85%)

**Notes:** The AI correctly identified the missing-files root cause and full order-log timeline, and the resolution was exactly config uploading the files. It framed the request slightly differently than the literal "files without logos" ask, but the operative fix matched.

---
## 51. Ticket #85003 — UHG Agent Toolkit Monthly Billing Report (duplicated cost)

**Investigator's Conclusion:** The AI concluded the report duplicated order L2038186's cost due to a query fan-out — joining orders → order_items → order_shipments without aggregation, producing one row per shipment and repeating order-level totals. It recommended joining order_ledger_entries or aggregating shipments, auditing other multi-shipment orders, and fixing the Redash query.

**Actual Outcome:** The reporter shared the Redash query (query/315), and Reilly fixed the issue. The cause was the report query logic duplicating on multiple shipments, exactly as the AI diagnosed; the fix was to the Redash query.

**Accuracy:** Accurate (90%)

**Notes:** The AI precisely diagnosed the multi-shipment join fan-out as a report-query bug (not a data issue) and recommended the correct remediation, which is what the data engineer did. Strong.

---
## 52. Ticket #85014 — Custom quote page (blank)

**Investigator's Conclusion:** The AI concluded the blank CQ page stemmed from the GetPage Lambda getting "DynamoDB items count: 0" across many sessions (a widespread backend filter/query issue), plus a 413 payload error and an empty-string id ValidationException, recommending dev review of the filter logic and a browser-cache/refresh workaround.

**Actual Outcome:** The support team simply asked the user to clear browser cache and log back in; with no further reproduction reported, the ticket was closed ("if there are any issues, reopen"). No backend fix or confirmation of the AI's Lambda/DynamoDB theory occurred within the thread.

**Accuracy:** Partially Accurate (50%)

**Notes:** The AI's browser-cache workaround matched what the team tried and the ticket closed on, and framing it as a front-end-render/session issue was reasonable. But its confident "widespread DynamoDB 0-items backend bug" narrative was never validated and appears heavier than the actual (cache-cleared) resolution.

---
## 53. Ticket #84736 — PM Notification - Items Scanned to Incoming Items Cart

**Investigator's Conclusion:** The AI concluded the pick-up notification failed because the "Incoming Items" location (RCPMSINC) was missing the PM Cart (PMCART) location tag, theorizing the UpdateJobLocation Lambda triggers notifications on that tag, and recommended adding the PMCART tag to the location.

**Actual Outcome:** L3 (Nick) explicitly refuted the AI's PMCART-tag theory: no code reads that tag, the 10 PMCART-tagged locations are decommissioned, and the scans + Pace handoff worked fine. The real issue is a Pace-side notification trigger that stopped firing (the pick-up email is generated by Pace, not Collaterate); a prior identical failure (FS 82387) predates the location changes. Handed off to Pace admins.

**Accuracy:** Inaccurate (20%)

**Notes:** The AI's specific PMCART-tag root cause and "add the tag" recommendation were directly refuted by L3 as a false trail (no code reads the tag; those locations are decommissioned). It did correctly note the notification is likely Pace-side and that no notification email class exists in Collaterate, but the headline diagnosis/fix was wrong.

---
## 54. Ticket #85031 — Why do freight jobs come over as Customer Pickups?

**Investigator's Conclusion:** The AI concluded freight-vs-pickup misrouting was a by-design limitation: system_offerings has a hard-coded fulfillment_center_id (routing to MN), and changing the shipping method post-order doesn't re-route to SC. It recommended dev work to add freight-based FC re-routing logic, config options, and gating pickup options — framing it as a systemic workflow gap. (Notably, it analyzed a 2021 example order.)

**Actual Outcome:** The shipping team tied it to the recently launched dimensional-shipping functionality (no shipping options shown when weight exceeds threshold); they implemented a site-based flag (enabled for Smartpress) with additional freight fixes coming Sept 2. The actual work centered on the dimensional-weight/shipping-options behavior, not the FC-hardcoding routing rule the AI described.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI correctly framed it as a real routing/shipping workflow gap needing dev work and routed it to the shipping team, which aligned with handling. But its specific root cause (hard-coded fulfillment_center_id, no freight re-routing) diverged from the dimensional-shipping/threshold cause the team actually addressed, and it analyzed a stale 2021 order.

---
## 55. Ticket #85168 — Submitting a Hub Ticket - Requiring a Lam to add Item to cart

**Investigator's Conclusion:** The AI concluded the front-laminate field on the three cut-vinyl classifications (438, 523, 663) was effectively required because show_front_laminate=true, no "None" option existed, and no default was selected — so users must pick a laminate despite require_front_laminate=false. It offered fix options (hide the field, add a None option, or set a default).

**Actual Outcome:** The team reproduced it (with Summa cutting on UV Roll printing, no front lam selected, "Front laminate is required" popup) and took it on to fix as a config/validation issue. The AI's characterization of the laminate-requirement/config problem aligned with the reproduction, though the exact trigger involved the cut-vinyl/premask combination.

**Accuracy:** Accurate (80%)

**Notes:** The AI correctly identified the front-laminate requirement as the blocker and provided sensible config remediation options matching how the team approached it. Slightly lower because the precise trigger (cut vinyl + no lam validation on the PJC) was a bit more specific than the AI's "no None option" framing, and no final fix was confirmed in-thread.

---
## 56. Ticket #85213 — Custom Quotes alert message (session expired / invalid JSON)

**Investigator's Conclusion:** The AI pinned it on the new v2 JWT authorizer deployed 2026-08-20 doing live permission introspection: broadly-permissioned admins have oversized JWTs causing HTTP 413/400 on introspection, so the authorizer fails closed (401) → "session expired," and the HTML error page → "not valid JSON." It cited TTI-20981 (Critical) and the Skinny JWT epic, recommending escalation.

**Actual Outcome:** The dev (Cameron) confirmed the cause was exactly the new authorization mechanism rolled out ~8/20: the Custom Quotes token was still on the old version, breaking auth. A fix went live and Tom confirmed it was working. This matches the AI's JWT-authorizer root cause closely.

**Accuracy:** Accurate (90%)

**Notes:** The AI correctly tied both errors to the new JWT authorizer/token-version rollout on 8/20 and even surfaced the exact tracking tickets. The dev's explanation (old token version vs new auth mechanism) is the same root cause; strong, detailed, and actionable.

---
## 57. Ticket #85234 — Automated placing issue from Jira to Collaterate

**Investigator's Conclusion:** The AI concluded order 2036754 (Sephora: Inventory) was auto-placed with default fulfillment center 460 instead of the "ship to store" FC 31, framing it as a data-mapping gap in the intake automation, and recommended dev investigation, reviewing SCWO-101673, confirming the manual fix, and adding validation.

**Actual Outcome:** The requester replied "Disregard, we figured it out :)" almost immediately — the order had already been manually corrected and no root-cause work was pursued. There's no confirmation of the AI's FC 460-vs-31 theory.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI produced a plausible, detailed fulfillment-center-routing analysis, but the ticket was self-resolved/disregarded with no validation of its specific theory. It correctly recognized the order was already manually fixed. Rated middling due to lack of confirmation.

---
## 58. Ticket #85256 — Auto-approve orders not generating files

**Investigator's Conclusion:** The AI concluded job 4634161 failed to auto-generate a proof (print file present, proof "Not Created," pod_template_order_file_id null on a closed session) while siblings succeeded, theorizing the instant-proof pipeline silently skipped it — possibly a race/callback failure under concurrent submission — and recommended redrops, scoping affected jobs, and a reconciliation job.

**Actual Outcome:** The team confirmed it was a Workflow-server-side issue: CHILI generates files fine, but the Workflow server silently drops some POD jobs when multiple items on an order complete near-simultaneously (Name Tags/Business Cards especially). Redrops fix it; other affected orders were identified. Routed to Production Automation Workflow (Jitbit).

**Accuracy:** Accurate (85%)

**Notes:** The AI correctly identified a silent, concurrency-related skip in the proof-generation pipeline affecting some jobs while siblings succeed, and that redrops remediate — matching the team's Workflow-server finding. It attributed it to the instant-proof Lambda rather than the Workflow server specifically, but the mechanism (concurrent burst → silently dropped jobs) was right.

---
## 59. Ticket #85267 — New MOD Site config calculating sales tax on a "zeroed" out product

**Investigator's Conclusion:** The AI framed this pre-sales config question (split billing: user pays shipping+tax via CC, product cost invoiced to corporate) around TERMS+CREDIT_CARD dual payment, the audit_sales_tax_for_terms and system_pays_tax flags, and credit-account limitations, warning the zeroed-product tax base is the core problem and recommending Solutions/accounting review plus checking tax-exempt status.

**Actual Outcome:** CJ clarified the real technical crux: the tax engine should send the total of the ledger entries' "SupplierPrice" to OneSource, not finalPriceAfterAdjustments; his testing showed it wasn't, so he directed a ticket for a Java dev/AI to inspect the tax payload code. The investigation moved to the OneSource payload value, and a Kiro code investigation was attached.

**Accuracy:** Partially Accurate (60%)

**Notes:** The AI correctly identified the zeroed-product taxable-base problem and that dual TERMS+CC billing is supported, which is the right problem space. But it didn't reach the specific OneSource payload issue (SupplierPrice vs finalPriceAfterAdjustments) that CJ pinpointed, and it leaned on config flags rather than the tax-payload code path that became the focus.

---
## 60. Ticket #85289 — Customer Registration Issue

**Investigator's Conclusion:** The AI concluded the registration form was rejecting Susan Kell ("Username already in use" / "User exists for that email") but no matching user existed in prod, theorizing a soft-deleted/inactive account or a uniqueness-check collision, and recommended asking which storefront, searching admin including inactive accounts, resetting the password, or manually creating the account.

**Actual Outcome:** The agent tested registration and it succeeded (in stage and prod); the user was directed to the Smartpress registration link, then successfully registered on the Smartpress storefront and placed an order. It appears to have been a storefront/URL issue rather than a stuck duplicate account.

**Accuracy:** Partially Accurate (50%)

**Notes:** The AI correctly flagged that no matching user existed and that identifying the correct storefront was key (which is what resolved it). But its leading "soft-deleted/reserved account" theory wasn't the cause — registration simply worked once done on the right storefront link.

---
## 61. Ticket #84874 — Hub issue requiring back lam under UV Roll Product Type

**Investigator's Conclusion:** The AI's first comment (on the Aug 26 status check) reported the root cause per Jira TK-264: a logic-ordering bug in getBackLaminates() in largeFormatConfigureController.js (mount-substrate check ran before the self-adhesive check, forcing an adhesive laminate; plus forms.dd not rendering "None" for an empty list). It confirmed PR #7377 merged 8/25, QA Ready, awaiting release.

**Actual Outcome:** This exactly matches the L3 developer's own root-cause writeup earlier in the ticket (Sravani: getBackLaminates ordering issue, self-adhesive check, forms.dd "None" rendering, frontend-only fix in largeFormatConfigureController.js) and the confirmed fix status. The AI accurately synthesized the merged fix and QA status.

**Accuracy:** Accurate (90%)

**Notes:** The AI's second comment ran after the dev had already diagnosed and merged the fix, so it was largely reporting/confirming, but it did so accurately with the correct file, mechanism, PR, and Jira status.

---
## 62. Ticket #85353 — Vituity - Missing PO field - due ASAP

**Investigator's Conclusion:** The AI concluded order 2048381 had an empty orders.po field (never populated at checkout) blocking client approval; confirmed via a comparison order that the PO field works when populated (not a theme/config bug); answered the agent's question that updating orders.po drives the AOD PO display; and recommended getting the PO from the client and running a DB UPDATE on orders.po for id 2110930.

**Actual Outcome:** Exactly this — the client provided PO #28214, and CJ ran the DB UPDATE on orders.po for id 2110930 to set it. The AI's diagnosis (single-order missing PO, fixable via a direct DB update) and its answer to the agent's question matched the resolution.

**Accuracy:** Accurate (95%)

**Notes:** The AI precisely diagnosed the empty-PO data issue, correctly answered the agent's specific "will a DB update populate the AOD field?" question, and provided the exact UPDATE that CJ ran. Strong end-to-end match.

---
## 63. Ticket #85402 — Collaterate Image Upload "Queued"

**Investigator's Conclusion:** The AI concluded the "Queued" state meant the presign call to /s3FileUploadConfiguration/v2/create failed silently (auth/session/CORS/size), keeping plupload stuck, and recommended checking the browser console/network for the failed POST, verifying file size/type, and re-logging in.

**Actual Outcome:** The team pulled AWS logs showing the exact cause: the presign POST returned "Username candice.gieseke... was unauthorized... AccessDeniedException" — a permissions issue. Adding the "User & Division Manager" role resolved it (verified in stage), and config granted it in prod.

**Accuracy:** Partially Accurate (65%)

**Notes:** The AI correctly localized the failure to the /s3FileUploadConfiguration/v2/create presign call failing silently and leaving the file queued — which is exactly where the AccessDenied occurred. But it listed session/CORS/size as likely causes and didn't identify the user-permission/role gap that was the actual fix.

---
## 64. Ticket #85417 — HUB Printer Selection (Tauro 1X spins)

**Investigator's Conclusion:** The AI concluded no device named "Tauro 1X" exists (only Agfa Tauro 3300 / Roll), flagged a config change to the Agfa Tauro 3300 on 8/26 (day before) by Sheila, and theorized a cost-table/version-price misconfig causing the quote spinner; recommended contacting Sheila, checking cost table 6905, and clarifying the device name.

**Actual Outcome:** The team reproduced it: selecting color-critical device "Agfa Tauro 1X" produced a "color critical device mapping error" / infinite spinner. CJ fixed a loop and found the default page load wasn't selecting a printing method (likely a substrate not added as a press sheet to the default press); config investigated and the user confirmed they could then select the Tauro X1.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI correctly tied the spinner to a recent Tauro device config change and a device-mapping/quote problem, and "Tauro 1X" was indeed the Agfa Tauro device. But the actual fault was a color-critical-device mapping / press-sheet-on-default-press issue and a front-end loop, not the cost-table 6905 theory; the "device doesn't exist" framing was a naming red herring (it did exist as Agfa Tauro 1X/X1).

---
## 65. Ticket #85424 — Dev Request/Idea - Product Attributes & Additional Information Fields on Master Products

**Investigator's Conclusion:** The AI confirmed this is a valid, data-backed feature request: the Collaterate data model has no mechanism to define Product Attributes or Additional Information Fields at the master (system_offerings) level — they exist only per site share (system_offering_site_share_metadata). It quantified the repetition (17,484 duplicate metadata entries; e.g. Golden Outlook Postcard = 292 across 99 shares), noted related in-flight ticket TTI-20466, and recommended creating a new TTI story with a system_offering_metadata template table plus propagation/override logic.

**Actual Outcome:** No non-AI conversation entries exist; ticket remains Open (status 2), escalated, assigned to a responder as a Feature/Dev Request. No human reply confirmed or refuted the analysis, but the request is well-scoped for Jira intake, which matches the AI recommendation.

**Accuracy:** Accurate (85%)

**Notes:** Thorough, evidence-based schema analysis with concrete implementation path; unverified by a human response but consistent with the request and standard dev-intake handling.

---
## 66. Ticket #85425 — Dev Request - Test Production Ticket button on product pages

**Investigator's Conclusion:** The AI framed this as a net-new feature request for a "Test Production Ticket" button paralleling the existing "Test Pricing" button, and traced the existing button to systemOfferingShare.jsp / calcTest.testCalculator(), noting the telling testPJC CSS class and pre-loaded cpricingpjcs data. It scoped the work (new dry-run backend endpoint, JSP button, JS function, modal template), found no prior Jira ticket, and recommended filing a TTI story.

**Actual Outcome:** No non-AI conversation entries; ticket is Open (status 2), escalated, in dev-request queue with a responder assigned. Nothing contradicted the AI's code-level scoping; the requester supplied a UI mockup the AI referenced.

**Accuracy:** Accurate (85%)

**Notes:** Strong code investigation and well-scoped feature breakdown; no human outcome yet to fully confirm, but the analysis is internally consistent and actionable.

---
## 67. Ticket #85427 — Dev Request - Sorting Options on Master Products

**Investigator's Conclusion:** The AI validated this UI enhancement request (sort/filter controls for site-share lists on master products), quantifying scale: 118,447 site-share records, ~45% on inactive/non-live sites, ~36% on DELETED/RETIRED master products. It confirmed all requested sort/filter columns exist in the schema (name, status, sites.active/live, override_pricing, override_turnaround_times), found no existing Jira ticket, and recommended a low-priority TTI story with a default "hide inactive" filter.

**Actual Outcome:** No non-AI conversation entries; ticket is Open (status 2), escalated, in the dev-request queue with a responder assigned. No human reply confirmed or refuted, but the feasibility mapping is sound and matches typical intake.

**Accuracy:** Accurate (85%)

**Notes:** Well-supported feasibility assessment tying each requested control to an existing column; unverified by human response but internally consistent.

---
## 68. Ticket #85432 — LIFEWISE SKU 101197499-0001 ADJUST QTYS

**Investigator's Conclusion:** The AI identified variant ID 68376 with corrupted negatives (actual_inventory -2, reserved_inventory -2) and backorder_inventory 2, recommending actual→0, reserved→0, and leaving backorder at 2 (asserting the single backorder on Job 4632405/Order 2052472 was correct). It flagged the negatives as a WMS sync issue and suggested the backorder-not-showing symptom might be display logic.

**Actual Outcome:** The agent worked it interactively with the requester. It turned out Job 4632405 had 2 shipped + 2 backordered, so Job 4592415 also needed to show as backordered — the requester confirmed backorder qty should be 3 (not 2). The agent set backorder to 3 and had Curt Johnson adjust Job 4592415 in the backend so it displayed as backordered; ticket resolved (status 5).

**Accuracy:** Partially Accurate (60%)

**Notes:** The AI correctly diagnosed the corrupted negatives and the actual→0 fix, but its backorder recommendation (leave at 2) was wrong — the real answer was 3, and a second job needed a backend backorder flag the AI did not identify.

---
6b. Ticket #84223 — [FAILED TO FETCH]

**Investigator's Conclusion:** N/A — the Freshservice API returned 403 access_denied on every attempt; ticket contents could not be retrieved.

**Actual Outcome:** N/A — no data available.

**Accuracy:** N/A (excluded from statistics)

**Notes:** Ticket #84223 (chronological position 6) could not be fetched due to a persistent 403 access-denied error; excluded from all accuracy math.

---
## 69. Ticket #85429 — [FAILED TO FETCH]

**Investigator's Conclusion:** N/A — the Freshservice API returned 403 access_denied on every attempt; ticket contents could not be retrieved.

**Actual Outcome:** N/A — no data available.

**Accuracy:** N/A (excluded from statistics)

**Notes:** Ticket #85429 could not be fetched due to a persistent 403 access-denied error; excluded from all accuracy math.

---
## 70. Ticket #85352 — AmeriLife: Additional Information Field Questions - Issue - Due 8/27/26 if possible

**Investigator's Conclusion:** The AI pinpointed the "Career Business Card – NO PHOTO" share (ID 136264) and blamed the required-field validation popup on the personalize_content_template being changed to personalize-chili.html on 2026-08-03 by sheila.luiken, asserting the Chili template fires required-field validation on first focus. It recommended reverting the template to personalize.html or deferring Chili validation to submit time.

**Actual Outcome:** The agent reproduced the issue on the AmeriLife Print storefront ("Career Business Card – NO PHOTO"), identified the root cause, and raised Jira TK-265 with a code fix PR (collaterate/collaterate #7421) under review — indicating the real fix was a code change to the validation logic, not merely a per-product template revert.

**Accuracy:** Partially Accurate (65%)

**Notes:** The AI correctly identified the exact product and the required-field-validation nature of the bug, but the resolution was a code fix (PR #7421), suggesting the AI's template-config theory and revert recommendation were not the actual remedy.

---
## 71. Ticket #85466 — Stock Product Inventory Adjustment Issues

**Investigator's Conclusion:** The AI concluded the "spinning" inventory-adjustment saves were caused by backend instability in the sku-central-al2-prod-env service, citing repeated SEVERE health episodes (82–95% HTTP 4xx) and an SQS sendMessage messaging error on 2026-08-28, plus a missing variant record for SKU 120527621. It recommended engineering review the environment health and the user retry after recovery.

**Actual Outcome:** The real cause was a permissions gap — the user lacked the "Inventory Adjusting" role. After logout/cache-clear failed, the agent escalated to the Config team; Sheila Luiken granted the role/permissions, and the user confirmed inventory adjustment worked. Ticket resolved (status 5).

**Accuracy:** Inaccurate (25%)

**Notes:** The AI produced an elaborate infra-instability root cause, but the actual fix was a simple per-user role grant. The correlated 4xx/SQS log noise led it away from the real permission issue.

---
## 72. Ticket #85471 — Reworks are not arriving in the manual queue

**Investigator's Conclusion:** The AI concluded rework items were being set to production_status_id = 4 ("Queued For Print") instead of 1 ("Production Ready") on submission, describing a ~5x spike starting Aug 20 as a code regression. It recommended escalating to dev (TTI), reviewing deploys around Aug 20, and a data fix resetting affected items to status 1, with sample job numbers.

**Actual Outcome:** The ticket was worked through examples with Preston Fisher; the agent's first sample job numbers turned out to be a stock-product/order-number mix-up (2050465 was a stock order), and a corrected example job (4632914) was provided. The investigator's findings (FS-85471-findings.md) were shared with developer Charan Pelleti for confirmation; ticket remained Open (status 2) with root cause still under dev review, not yet confirmed.

**Accuracy:** Partially Accurate (60%)

**Notes:** The AI's status-4-vs-1 regression theory was plausible and detailed and was forwarded to a developer, but it was not confirmed within the ticket, and some of its sample job numbers were mismatched, requiring clarification.

---
## 73. Ticket #85450 — 4641906 - Customer Job Name Not Syncing

**Investigator's Conclusion:** The AI found the job_name for order 2056070 / Job 4641906 was already correctly set to "Audrey Robinette" on both line items, so no data fix was needed. It concluded the customer was actually seeing the order-level Project Name ("Embossed Logo Perfect Bound Book [Copy]") and framed it as a portal display/sync gap for custom-quote orders, recommending escalation if the portal doesn't surface job_name.

**Actual Outcome:** The agent confirmed exactly the AI's distinction: the storefront shows the Project Name while the job view shows the Job Name (correctly "#4641906 – Audrey Robinette"), so job specs are unaffected. When the customer asked to change the Project Name, the agent replied it can't be changed once the order is submitted. Ticket remained Open (status 2).

**Accuracy:** Accurate (85%)

**Notes:** The AI correctly diagnosed the project-name-vs-job-name confusion and that no job-spec data fix was needed, matching the agent's explanation; the only nuance is the project name being immutable post-submission, which the AI floated as a possible edit.

---
## 74. Ticket #85474 — BOM Builder - Missing SKU - Order 2048362

**Investigator's Conclusion:** The AI concluded order 2048362 was on hold because SKU S-1583734 was missing in Collaterate on the KOHLER Professional Channel site (system offering 83361 / site 533), with all 3 line items failing the BOM Builder ("Missing SKU(s)"). It framed this as a config/catalog gap (not a code defect) and recommended adding the SKU variant, then re-triggering the BOM Builder and verifying the jobs.

**Actual Outcome:** Brian Serbus confirmed the product had been retired and was reactivated on 8/28, matching the AI's missing-SKU/catalog-gap diagnosis. The BOM Builder was then manually re-triggered on 8/31 (it does not auto-retry), rebuilding order 2048362 from 3 to 33 line items and order 2049804 from 42 to 62, with no DLQ errors. Both orders remained flagged on hold pending manual resolution of the original hold entries.

**Accuracy:** Accurate (90%)

**Notes:** The AI correctly identified the missing-SKU root cause, the catalog/config nature, and the exact re-trigger steps. It didn't cover the second order (2049804) or the nuance that a successful rebuild doesn't auto-clear the hold, but the core diagnosis and remediation were right.

---
## 75. Ticket #85478 — Not able to create tickets in BBY SF Hub

**Investigator's Conclusion:** The AI concluded the status-500 error on the Best Buy Internal storefront was an Order Number Sequence Conflict: the order_numbers tracker (1,965,803) was ~91K behind the actual max order number (2,057,463), so every new order threw a "java.lang.RuntimeException: Order number conflict." It cited order-intake prod logs and recommended a DBA update the tracker above the current max, calling it system-wide, not user-specific.

**Actual Outcome:** The agent asked the user to log out and clear cache, then whether they could create new projects; the user replied "it seems to be working now" and the ticket was closed (status 5). No DBA sequence update was performed or referenced — the issue resolved on its own / after a session refresh.

**Accuracy:** Inaccurate (35%)

**Notes:** The AI's elaborate order-number-sequence-conflict theory was never validated; the problem cleared after a simple logout/cache-clear, and its assertion that it was system-wide (not user/session-specific) appears contradicted by the self-resolution.

---
## 76. Ticket #85479 — Auto Approve Proof files not processing to Collaterate and approving

**Investigator's Conclusion:** The AI concluded the auto-approve proof pipeline was broken because the auto_uploaded flag stayed false on order_item_consumer_proof_files for 9 jobs, so the complete_soft_proof Lambda kept skipping them ("not complete") and proofs stayed "Not Created." It said the upstream auto-upload/file-linking step never fired, ruled out Lambda errors/DLQ/proof config, and recommended manual approval plus an engineering fix and alerting.

**Actual Outcome:** Investigation traced it to a recent deployment in the sls-pace-file-system service (Art In flow) blocking file linking; a revert was merged but not deployed because the release build failed. Separately, job 4645181 caused an infinite loop that stalled others. New jobs processed fine, but affected jobs still would not link even after a file re-drop, so the resolution was a manual proof-file upload workaround; ticket closed (status 5).

**Accuracy:** Partially Accurate (70%)

**Notes:** The AI correctly localized the failure to the upstream file-linking/auto-upload step (not Collaterate proof config or the complete_soft_proof Lambda), which matched reality. It missed the specific cause (a bad sls-pace-file-system deploy plus an infinite-loop job) and the fact that the merged revert never reached production.

---
## 77. Ticket #85496 — Custom Quote Appearance on Smartpress Dashboard

**Investigator's Conclusion:** The AI concluded the "huge font" for custom quote orders on the Smartpress dashboard was a front-end CSS rendering difference in the server-rendered [[ orderlist ]] template: custom quote items (with a job_name) render under a larger heading element than standard items. It called it cosmetic (no data/pricing impact) and recommended a dev fix to the heading element/CSS class or a targeted smartpress-theme CSS override, plus a TTI ticket.

**Actual Outcome:** The agent reproduced it in Stage, confirmed exactly this: custom quotes render a project-name heading styled by the broad .orders-page h3 rule (2.4em) while normal orders use the smaller .c-order-item-names-preview (17px). The fix landed as a CSS change in smartpress-theme (legacyOrdersPage.css) — a developer directed changing .orders-page h3 to .orders-page h3:not(.c-order-project-name) to scope the styling to custom quotes only.

**Accuracy:** Accurate (90%)

**Notes:** The AI nailed the root cause (a broad heading CSS rule affecting only the custom-quote project-name element), the affected repo/file, and the targeted-CSS-override remedy; the final fix was a slightly different but equivalent selector-scoping approach.

---
## Summary Statistics

| Metric | Count | % of rated tickets |
|---|---|---|
| Total tickets (chronological list) | 78 | — |
| Tickets successfully fetched | 75 | — |
| Tickets with AI comments | 75 | 100% of fetched |
| Accurate (85-100%) | 39 | 52.0% |
| Partially Accurate (50-75%) | 23 | 30.7% |
| Inaccurate (<50%) | 13 | 17.3% |
| Tickets without AI comments | 0 | 0% |
| Tickets that failed to fetch (403) | 3 | excluded |
| Average accuracy % (across 75 rated) | 67.6% | — |

Notes on counts:
- Every successfully fetched ticket (75) contained exactly one `[AI Comment]` from the TE Investigator (user 10002980302), so "tickets without AI comments" is 0.
- 3 tickets could not be fetched at all due to persistent Freshservice 403 access_denied errors and are excluded from all accuracy math: **#84403**, **#84223**, **#85429**.
- The average accuracy of 67.6% is the mean of the 75 individual percentage ratings.

## Key Observations

- **Common reasons for inaccurate conclusions:** The most frequent failure mode was the Investigator constructing an elaborate infrastructure/code root cause from correlated log or data "noise" when the real cause was mundane and local. Examples: #85466 and #84779/#84919/#85402 (actual fix was a per-user Collaterate role/permission grant, not the cited infra instability or code path); #85478 (an "order number sequence conflict" theory that never materialized — the issue cleared after a simple logout/cache-clear). Correlation-with-timing was repeatedly mistaken for causation.

- **Front-end vs back-end misattribution:** Several misses came from mislabeling the layer of the bug. In #84213 and #84199 the Investigator blamed data/config or an upstream Configurator when the defect was actually front-end rendering or a monolith code branch. Conversely, when it correctly identified a front-end/CSS cause (#85496) or an upstream file-linking break (#85479), it scored well.

- **Types of issues the Investigator handled well:** Clean, data-model-grounded diagnoses were consistently accurate — inventory/variant data corrections (#85432 core diagnosis, #84153), BOM Builder missing-SKU/catalog-gap cases (#85474), redemption/points rollbacks (#84195), and CSS/template rendering issues (#85496). Feature/dev-request triage (#85424, #85425, #85427) scored well because the AI's schema and feasibility analysis was thorough and directly actionable for Jira intake.

- **Recurring gaps in analysis:** (1) Backorder/multi-job quantity logic — in #85432 it recommended leaving backorder at 2 when the human-confirmed answer was 3 and a second job needed a backend flag. (2) It rarely accounted for permission/role configuration as a cause of "spinning"/save failures, defaulting instead to infra or code. (3) It often stopped at the first plausible cause and did not always verify whether a merged fix actually deployed (#85479) or whether a self-service refresh would resolve the symptom (#85478).

- **Notable patterns in actual resolutions vs AI recommendations:** A large share of tickets resolved through simple human actions — role grants, logout/cache-clear, manual proof uploads, or manual BOM re-triggers — rather than the deeper engineering fixes the AI proposed. When developers did act on the AI's lead (e.g., #85352 → PR #7421, #85471 findings shared with dev, #85496 CSS fix), the AI's direction was usually in the right area even if the exact remedy differed. Recurring "spinning uploads" tickets (#84842/#84843/#84847) were transient async-backlog issues that self-resolved, which the AI's specific theories did not capture, landing them at Partially Accurate.
