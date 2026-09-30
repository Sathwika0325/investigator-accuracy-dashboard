# TE Investigator Accuracy Audit — August 31 (carry-over) + September 2026

Source: `#investigator-findings` (C0AKY9ABMKP), Aug 31 00:00 – Sep 30 23:59 2026. Investigator = FreshService user 10002980302 (`[AI Comment]`).
Aug 31 carry-over tickets: **#85496 only**. All others are September 1–30.

==
1. Ticket #85496 — Custom Quote Appearance on Smartpress Dashboard **[AUG 31 CARRY-OVER]**

Investigator's Conclusion: Diagnosed the "huge font" on custom quote orders as a front-end CSS/heading rendering difference — custom quotes render the project-name in a larger heading than standard orders. Called it a cosmetic UI bug in the orderlist template, recommended a targeted CSS specificity fix and a Jira TTI ticket.

Actual Outcome: Agents reproduced it, confirmed it only affects custom quote orders (project-name heading vs. the smaller `.c-order-item-names-preview`), and shipped a CSS fix (`.orders-page h3:not(.c-order-project-name)`) live to production the same day.

Accuracy: Accurate (90%)

Notes: Correctly identified it as a CSS/heading specificity issue on the exact element; the applied fix matched the investigator's diagnosis and recommendation.

==
2. Ticket #85546 — [Can't Bulk Upload to Collaterate — inaccessible]

Investigator's Conclusion: Not assessable — the ticket returned HTTP 403 "access_denied" and could not be fetched.

Actual Outcome: Not assessable — ticket inaccessible.

Accuracy: NOT ASSESSABLE (ticket returned 403 access_denied; not re-fetched per rules)

Notes: Flagged and skipped. Excluded from statistics.

==
3. Ticket #85556 — Rhodes: Inventory Adjustment needed - Due 9/2/26

Investigator's Conclusion: Identified SKU 100439815 variant had `reserved_inventory = -21` (negative), inflating available-to-order to 21 despite 0 actual inventory; recommended setting reserved_inventory to 0 on variant id 39972 and notifying WMS.

Actual Outcome: The agent adjusted the reserved quantity within minutes; requester confirmed "Looks great, thanks." Resolution matched the diagnosis exactly.

Accuracy: Accurate (95%)

Notes: Precise root cause (negative reserved inventory) and the fix applied matched the recommendation.

==
4. Ticket #85558 — Jira automated order placing glitch

Investigator's Conclusion: Backordered item shipped instead of going to Processing; offered ranked hypotheses — primary: missing "JIRA #" metadata causing a silent skip; secondary: `stockBackorderQuantity` not set at event time (timing gap); tertiary: Aug 20 deploy regression.

Actual Outcome: Dev found the item had inventory at order time, then went backordered after a DC inventory "true up"; Collaterate sends no event on that later change, so the seconds-after-placement check couldn't catch it — a timing gap.

Accuracy: Partially Accurate (65%)

Notes: The investigator's secondary hypothesis (backorder qty not known at event time) matched the true cause, but it was not the primary hypothesis and the metadata theory was wrong.

==
5. Ticket #85576 — Can't Bulk Upload to Collaterate

Investigator's Conclusion: Bulk upload Lambdas silent since Aug 28; hypothesized the Aug 31 CloudFormation update to `bulk-data-service-prod` broke the S3 event notification/trigger; recommended reviewing/rolling back that change.

Actual Outcome: Dev confirmed "I did some maintenance on the bulk-data-service and it caused the issue," reverted the changes, and verified files processed again. Requester confirmed success.

Accuracy: Accurate (90%)

Notes: Correctly pinpointed the bulk-data-service change as the cause; the revert matched the recommendation.

==
6. Ticket #85335 — Add Juan Sanchez to email lists

Investigator's Conclusion: NO `[AI Comment]` present from user 10002980302.

Actual Outcome: IT removed a former employee and added Juan to the Diamond/Thomasville distro groups; later handled as a MOD/Collaterate config question.

Accuracy: NO AI COMMENT (flagged)

Notes: No investigator conclusion exists; excluded from accuracy statistics.

==
7. Ticket #85602 — Tax Tools jamming

Investigator's Conclusion: Diagnosed intermittent Pace API `ConnectionError` (RemoteDisconnected) as the reason Tax Tools "jams" mid-run, with no retry logic; recommended retries/backoff and user-facing errors.

Actual Outcome: Dev found the primary jam cause was CSV whitespace ("US " vs "US") hanging a comparison; fixing those rows processed the file. A secondary connection issue was also addressed with a code change.

Accuracy: Partially Accurate (60%)

Notes: Missed the actual primary cause (whitespace/data parsing) but correctly identified the connection issue as a real secondary problem that was also fixed.

==
8. Ticket #85614 — Collaterate Feature Request - OLF - Producer Ganging

Investigator's Conclusion: Classified as a feature request for a "Do Not Print"/test-order flag; provided schema analysis (order_items flags, gang_status), noted no existing flag, recommended reclassify + TTI story + a `gang_status='NOT_GANG_READY'` interim workaround.

Actual Outcome: Tracked as TTI-21188; still open — product owner (Nick) pushing back on dev effort and asking for a simpler/manual approach and clearer requirements.

Accuracy: Accurate (88%)

Notes: Correct classification, sound schema analysis, and appropriate routing; final business decision still pending but investigator's framing was right.

==
9. Ticket #85618 — 2060139 - Configuration error with Brochure Product page

Investigator's Conclusion: "Printing on the Back: None" overridden to Full Color because Brochures PJC 5 has no "None" side-2 ink option; recommended adding a None ink option OR removing None from the UI.

Actual Outcome: Config team explicitly said a "None" ink should NEVER be added (reads wrong in production) — config is correct. Dev traced the real cause to the product-configuration-api Lambda sending `side2InkId: 0` instead of null; fix needed at the Lambda level. Resolved.

Accuracy: Partially Accurate (60%)

Notes: Correctly identified the symptom and that None isn't honored, but the recommended fix (add None to PJC) was contradicted; true root cause was a 0-vs-null bug in the Lambda.

==
10. Ticket #84465 — Saddle Stitch Dimensions on SPDC

Investigator's Conclusion: Confirmed in source an orientation-agnostic size clamp (long/short vs. width/height) lets 14w×12h pass; pinpointed two files in smartpress-apps and a step '0,5' typo; recommended a two-file front-end fix, no backend change.

Actual Outcome: Tracked as TTI-21181 for the dev team; investigation matched the code and was accepted as the basis for the fix.

Accuracy: Accurate (92%)

Notes: Detailed, source-verified root cause with a precise fix; routed to Jira.

==
11. Ticket #85639 — Collaterate (can't upload/save nonprofit files)

Investigator's Conclusion: Diagnosed a permissions gap — missing "Artwork Manager" role (id 37); recommended adding that role to the requester and the two Jamies.

Actual Outcome: Confirmed permissions issue; config team granted "User & Division manager" permission and the user was told to re-login. The user clarified the real symptom was "can upload but won't save."

Accuracy: Partially Accurate (65%)

Notes: Correctly identified it as a permissions problem, but the specific role granted differed from the "Artwork Manager" role recommended.

==
12. Ticket #85687 — Collaterate (Prepress queue showing 0s)

Investigator's Conclusion: Claimed system healthy and hypothesized the user is missing a Prepress Queue role (queue role gap affecting 42/78 techs); recommended assigning role 76.

Actual Outcome: Agent reproduced it in Prod with console error "Bulk data stream failed: 403"; Cameron "restored the queue" — a transient server-side/caching/stream issue, not a per-user role gap.

Accuracy: Inaccurate (35%)

Notes: The role-assignment hypothesis was wrong; the real cause was a 403 bulk-data-stream/caching failure resolved server-side.

==
13. Ticket #85711 — Access Shipping Notes

Investigator's Conclusion: Classified as a feature request for a site-wide default shipping note; confirmed no site-level note field exists, cited the reference-number defaulting pattern as precedent; recommended TEM story + schema/UI/logic changes.

Actual Outcome: Tracked as TTI-21189; dev built it — technical implementation doc and site-settings shipping-note UI attached, testing underway.

Accuracy: Accurate (90%)

Notes: Correct classification and design direction; the delivered implementation followed the recommended approach.

==
14. Ticket #85689 — Customer can't get past check out

Investigator's Conclusion: Posted after agents found the `users_site_id_email_unique_key` violation; added that `ma_pvt` (457804) still had a mismatched `email_unique` and gave the exact corrective UPDATE; noted other ma_* accounts also mismatched.

Actual Outcome: Cameron ran the DB correction; confirmed resolved and asked the customer to retry.

Accuracy: Accurate (90%)

Notes: Accurate, actionable, and matched the applied DB fix; added value beyond the agents' earlier notes.

==
15. Ticket #85725 — Collaterate: Product Set Side Nav - Not Showing Data

Investigator's Conclusion: Blank Product Sets page caused by the lean/skinny JWT rollout (missing `perms` claim → TypeError, no error boundary); TTI-20982 fix in develop but PR #74 unmerged to main; recommended merge + deploy.

Actual Outcome: Cameron confirmed "this has been fixed" and that a hard refresh/cache clear may be needed — consistent with a deployed fix.

Accuracy: Accurate (92%)

Notes: Correct root cause (lean-token perms) and repo; fix deployed as recommended.

==
16. Ticket #85252 — MOD Bulk add error message

Investigator's Conclusion: Traced the generic "status 500" text to `comet.js` and the backend `TBGStoreBulkAddCometHandler`; confirmed theme cannot fix it; recommended a Collaterate change to return a distinguishable error + preserve staged cart, plus optional front-end pre-validation. TTI ticket suggested.

Actual Outcome: Agents reproduced the 500 (JpaSystemException / transaction rollback) in Prod and Stage; consistent with the investigator's source analysis. No fix shipped within the ticket window.

Accuracy: Accurate (88%)

Notes: Thorough, source-verified analysis matching the reproduced error; correctly scoped as a Collaterate (not theme) change.

==
17. Ticket #85754 — Acrylic Board Printing with Primer - Order Item Weight Issue

Investigator's Conclusion: "Order item total weight of '0 lb'" caused by missing LF Print Job Classification link (NULL) and a missing/inactive substrate weight; recommended reactivating/linking the LF PJC and adding the substrate's square_foot_weight.

Actual Outcome: Config team confirmed "the substrate is missing some configuration," assigned weight to the board, and told the user the order could be placed. Resolved.

Accuracy: Accurate (90%)

Notes: Correct root cause (missing weight/substrate config); the applied fix matched the recommendation.

==
18. Ticket #85756 — Tile Shop 100558821-0001 Adjustment

Investigator's Conclusion: SKU shows 0 backorder despite an open unshipped qty-2 order; flagged `reserved_inventory = -1` anomaly; recommended setting `backorder_inventory = 2` on the variant.

Actual Outcome: Requester realized "backordering is disabled for this site," cancelled the item, and asked to zero the quantities; agent adjusted accordingly.

Accuracy: Partially Accurate (55%)

Notes: Data findings (0 backorder, negative reserved) were accurate, but the recommended action (set backorder=2) ran contrary to the actual resolution since backordering was disabled for the site.

==
19. Ticket #85776 — Lifewise skus not showing backordered - Drift update needed?

Investigator's Conclusion: WMS sync updates actual/reserved inventory but isn't computing `backorder_inventory`/`stock_backorder_quantity`; recommended running the drift-correction process and a dev review of the inventory sync Lambda.

Actual Outcome: CJ ran the drift script, found/fixed 50 drifted SKUs, and forwarded the inventory-sync issue the investigator surfaced to a developer. Requester satisfied.

Accuracy: Accurate (90%)

Notes: Correctly identified drift + a real inventory-sync gap; the drift-script resolution matched the recommendation.

==
20. Ticket #85785 — Collaterate Error (version count update)

Investigator's Conclusion: Hypothesized a version-config mismatch (VERSIONNAMEEF false, only 1 of "4v" versions) and/or a post-shipped/reopened-state restriction blocking version updates; asked for the error text.

Actual Outcome: Root cause was a permissions gap — Angela lacked the "Override Quotes" permission. Granting it (verified in staging) resolved the requote/version update.

Accuracy: Inaccurate (35%)

Notes: The version-config and order-state hypotheses were wrong; the real cause was a missing Override Quotes permission.

==
21. Ticket #85717 — Google OAuth Setup

Investigator's Conclusion: Mapped to TEM-10125/TEM-10106 owned by Reilly Melville; said the CDK AuthStack is ready and blocked on a Google Cloud admin creating a new OAuth app; recommended routing to Reilly + a GCP admin.

Actual Outcome: Dan Reicher replied that the plumbing already exists — just create a Cognito group on an existing pool, no new Google OIDC project needed; set up a walkthrough.

Accuracy: Partially Accurate (60%)

Notes: Correct on ownership/context and Jira mapping, but the recommended path (new Google OAuth app) was unnecessary; existing infrastructure could be reused.

==
22. Ticket #85872 — Bulk Load Data (add fields to stock template)

Investigator's Conclusion: Feature request; confirmed all 4 fields already exist on `site_offerings` but not in the bulk-load staging table/script; found overlapping TTI-12696; gave a concrete implementation plan and interim SQL workaround.

Actual Outcome: Routed internally (Curt to Brian Lureen) as a dev/enhancement request; still open, consistent with the investigator's routing.

Accuracy: Accurate (90%)

Notes: Thorough, correct schema analysis and identification of the overlapping backlog story; appropriate routing.

==
23. Ticket #85878 — 2064722 - Unable to edit tickets

Investigator's Conclusion: Hypothesized that 3 jobs with "Approved" proof status were locking edits; recommended resetting proof status to allow removing File-Prep operations.

Actual Outcome: Agents pulled CloudWatch logs and confirmed the real cause was "Printing configuration not compatible with PJC" (a config mismatch on requote), routed to the config team; a turnaround-time/pricing-weights config gap was also surfaced.

Accuracy: Inaccurate (35%)

Notes: The approved-proof-lock hypothesis was not the cause; logs showed a PJC/printing-configuration incompatibility.

==
24. Ticket #85835 — Incorrect Jira ticket status (status-fighting loop)

Investigator's Conclusion: ServiceChannel bot looped Processing↔Shipping on a back-ordered work order due to non-idempotent status transitions + duplicate webhooks; recommended a fix to check current status before transitioning and protect back-order state.

Actual Outcome: Dev (Parin) confirmed the cause, wrote and released the fix; statuses now hold instead of flipping, and a second reported case was covered by the same fix.

Accuracy: Accurate (92%)

Notes: Root cause (status transition idempotency + back-order interaction) confirmed and fixed as described.

==
25. Ticket #85877 — Order 2064114 - Laminate on Large Posters Issue

Investigator's Conclusion: Diagnosed a systemic misconfiguration — the "Laminating Run" slot on Large Posters PJC 14 mapped to the wrong operation (op 145 "Cut down 10k sheets for JPress") with wrong operation items, surfacing a blank costing-only laminate task; recommended remapping the operation/items.

Actual Outcome: Agents found it did NOT reproduce on other Large Poster orders; it occurred only when a "Cold Lam Run" value was passed, and the agent concluded "the Laminate is coming from the Gang" (ganged with laminated jobs).

Accuracy: Partially Accurate (60%)

Notes: Correctly localized the issue to the Large Posters laminate operation and its costing-only/blank behavior, but the actual explanation (gang-inherited laminate / value passed per order) differed from the "op 145 mismapping affects every order" conclusion.


==
26. Ticket #85892 — I need to remove the adhesive and cannot given system settings

Investigator's Conclusion: Job 4647726 (UV Roll Printing, PJC 337) has adhesive dropdown with only 2 adhesive options and no "None" adhesive-type laminate in the system; job also locked; recommended adding a None adhesive laminate to the PJC or nulling `adhesive_laminate_a_id`.

Actual Outcome: Agent confirmed "the Buy-out Print Substrate is not Self-Adhesive, so there is currently no 'None' option available"; the Pace item showed HIGH TACK ADHESIVE, and the ticket was routed to the Pace team for further investigation.

Accuracy: Accurate (85%)

Notes: Correctly identified the missing "None" adhesive-option root cause and the locked-job constraint, matching the config team's finding; final resolution moved to Pace but the diagnosis held.

==
27. Ticket #85906 — Board Printing override to PID# 33003

Investigator's Conclusion: Order 2063846 has 8 Board Printing jobs on the Agfa Tauro 3300; PID# 33003 isn't a Collaterate device/press-sheet reference so it's likely a Pace MIS printer ID; recommended clarifying which 3 jobs and routing to Planning to override in Pace, unlocking locked jobs first.

Actual Outcome: Config (Christi) added the material into Collaterate as an override on the board product, resolving it so the jobs could proceed. It was handled as a Collaterate material/config override, not a Pace-side device change.

Accuracy: Partially Accurate (60%)

Notes: Correct that PID 33003 wasn't in Collaterate and needed an override, but the framing (Pace-side device override, unlock locked jobs) diverged from the actual fix (adding a material override in Collaterate).

==
28. Ticket #85909 — HUB ISSUE: Pricing Engine on Hub not Working when 100# uncoated cover is picked

Investigator's Conclusion: Diagnosed the "could not be priced" error as a product-config issue — the Cards product's PJC likely maps to an inactive press sheet for 100# Uncoated Cover; recommended reactivating or remapping to active press sheet IDs 360/2768.

Actual Outcome: Dev (Ryan) said he was "re-initializing weights in the value-based pricing engine" and set the product back to the legacy pricing engine so it could quote — the cause was uninitialized value-based pricing-engine weights, not an inactive press sheet.

Accuracy: Partially Accurate (55%)

Notes: Correctly scoped it to pricing configuration (not an outage), but the specific root cause (missing value-based pricing weights) differed from the inactive-press-sheet hypothesis.

==
29. Ticket #85928 — Shipping Cost incorrect?

Investigator's Conclusion: Concluded the $52.25 FedEx quote was "functioning as designed" — dimensional weight on a large rigid sign + 40% markup + long-haul; recommended no engineering escalation and advising the customer the cost is legitimate.

Actual Outcome: After a deeper analysis, the team found "the box size that was provided to FedEx was indeed wrong for this order," committed to fixing it and refunding the customer after shipment.

Accuracy: Inaccurate (35%)

Notes: The investigator's "no bug, price is accurate" conclusion was overturned — there was a real box-size/dimensional data error causing an inflated quote.

==
30. Ticket #85918 — Print Information in Job Choices & Properties does not match Collaterate ticket

Investigator's Conclusion: The printable work ticket omits "(First Surface)" because jobs use ink id 116 ("Inca X2 - CMYK Backlit") while the correct ink is id 74 ("... (First Surface)"); the admin panel and work ticket source the label differently. Recommended reassigning ink, auditing id 116, and a template fix.

Actual Outcome: Dev confirmed the PWT shows the raw ink name and that surfacing "(First Surface)" requires a Collaterate change; the chosen fix was to change the ink's Production name to include "(First Surface)", tested in stage and greenlit for prod.

Accuracy: Accurate (88%)

Notes: Correctly identified the ink-name/display-source mismatch as the root cause; the implemented fix (correcting the ink's production name) aligns with the investigator's display-fix recommendation.


==
31. Ticket #85931 — Additional tracking didn't move to Jira or Service Channel

Investigator's Conclusion: The second tracking number on order 2011030 never entered the Service Channel SQS pipeline (DLQ empty, no events after July 29); hypothesized the "order shipped" event isn't emitted for a second shipment on a multi-shipment order; recommended manual remediation on SCWO-100638 and reviewing multi-shipment event emission.

Actual Outcome: Dev (Parin) found the order was placed before the "JIRA #" reference existed / manually-placed orders lack the JIRA # the tracking automation needs to match the work order; advised manually adding the tracking number (comma-separated) to the work order's Tracking field.

Accuracy: Partially Accurate (70%)

Notes: Correctly determined the event never fired/couldn't match the work order (not a stuck queue) and the manual remediation matched the dev's advice, but the precise cause (missing JIRA # reference on manual orders) differed from the multi-shipment-emission hypothesis.

==
32. Ticket #85955 — Need to override Aqueous Prints with PID# 7964

Investigator's Conclusion: PID# 7964 not found in any Collaterate table (likely a Pace ID); "Aqueous Prints" ambiguous across multiple offerings; requested clarification on what PID#/override/product were meant before acting.

Actual Outcome: Config (Christi) added material "to mount on aqueous prints as an override only," resolving it as a Collaterate material override (same pattern as ticket #85906).

Accuracy: Partially Accurate (55%)

Notes: Correct that PID# 7964 wasn't a Collaterate ID, but the investigator punted to clarification rather than identifying the material-override resolution path the config team ultimately used.

==
33. Ticket #85956 — L2066027, L2066315 - Not Integrated

Investigator's Conclusion: Both orders exist in Collaterate but were never integrated into Pace (all 20 items null status, no src_job records, queues/DLQ empty, no Lambda errors); root cause = the Collaterate→Pace event was never fired/silently dropped; recommended manual re-integration and checking for other affected orders.

Actual Outcome: Jason (ERP Admin) synced the two jobs, then found a third (L2067368) had also failed and re-synced it; confirmed the integration had failed and manual re-sync resolved it.

Accuracy: Accurate (90%)

Notes: Correctly diagnosed the orders as never integrated and recommended manual re-integration, which is exactly what resolved it; the "check for other affected orders" advice proved warranted (L2067368).

==
34. Ticket #85984 — Collaterate not calculating tax when doing a refund

Investigator's Conclusion: Diagnosed the "Unexpected error estimating tax" as a OneSource (external tax provider) failure with a code-level gap — `calculateSalesTaxAdjustment()` lacks the fallback that `calculateSalesTax()` has; recommended disabling OneSource / adding fallback / retry.

Actual Outcome: Agents reproduced it in staging and found it was a PERMISSIONS issue — the user lacked the "Accounting" role; config added the role and the refund/tax worked. Requester confirmed fixed.

Accuracy: Inaccurate (35%)

Notes: The elaborate OneSource/tax-provider-fallback root cause was wrong; the actual cause was a missing "Accounting" permission on the user.

==
35. Ticket #86014 — WPN 2067801 - New file needed

Investigator's Conclusion: Confirmed job 4675559 is a 1-sided WPN Clear Window Cling with an active issue flag and no production status; the submitted file appears 2-sided with white ink, incompatible with the 1-sided clear spec; recommended requesting a corrected 1-sided file without white ink.

Actual Outcome: The agent uploaded a new file to the job without the white ink — "Should be all set," resolving exactly as recommended.

Accuracy: Accurate (90%)

Notes: Correct product-spec analysis (1-sided, white-ink mismatch) and the remediation (new file without white ink) matched the applied fix.


==
36. Ticket #86027 — Re: Turn off PID 8311 (Clear BOPP discontinue)

Investigator's Conclusion: Detailed state analysis — PIDs 8311/8312 still active (8311 marked out-of-stock in description), used across 30+ PJCs/sticker-label products, White BOPP already transitioned to 31833/31834 but no Clear BOPP replacement exists; recommended not retiring until sourcing provides a replacement.

Actual Outcome: A business/sourcing thread — high minimums (3–5 yrs of stock), no off-the-shelf option; team is evaluating a clear polyester alternative with lower minimums before deciding.

Accuracy: Accurate (85%)

Notes: The technical state analysis was correct and the "don't retire without a replacement" guidance aligned with the sourcing discussion; largely a business decision rather than a system fix.

==
37. Ticket #86102 — Lifewise Skus incorrect qtys

Investigator's Conclusion: SKU 101197347-0001 has backorder_inventory=0 when it should reflect open demand; recommended setting backorder to 2 (2 open orders), noted a systemic 25-SKU issue, and correctly cautioned that Rachel's "5" estimate was likely off.

Actual Outcome: The agent adjusted inventory and reported 4 backorders for the product (LWL 032 - Character Quality Laminated Poster); requester satisfied.

Accuracy: Accurate (80%)

Notes: Correct root cause (missing backorder inventory) and correct action (adjustment); the specific count (2 vs the actual 4) was off, but the diagnosis and remediation direction matched.

==
38. Ticket #86114 — Re-orders - no customer files from previous order

Investigator's Conclusion: The reorder copied proofs but not print files (order_item_consumer_print_files empty on reorder jobs while source files are intact); called it a silent skip in the print-file copy step; recommended manual re-attach + a dev bug ticket, noting it may be intermittent.

Actual Outcome: Agents confirmed the intermittent behavior across multiple reorders, later surfaced a "File not found in source bucket" error, and escalated to the dev (Nick).

Accuracy: Accurate (88%)

Notes: Correctly identified the exact symptom (proofs copy, print files don't) and that it's intermittent; the later "file not found in source bucket" finding refined but confirmed the investigator's diagnosis.

==
39. Ticket #86125 — Inactive PJCs

Investigator's Conclusion: Confirmed inactive PJCs appear in the product-assignment dropdown; quantified 126 active products already linked to inactive PJCs; cited precedent TTI-18414 (same fix for the device dropdown); recommended an active=true filter plus a "Show Inactive" checkbox.

Actual Outcome: Dev implemented both changes (folder-name removal aside), tested locally, and raised a PR under review; the recommended two-part fix was built.

Accuracy: Accurate (92%)

Notes: Thorough data-backed analysis with a strong precedent; the delivered implementation matched the recommended active-filter + checkbox approach.

==
40. Ticket #86208 — Dev Request - Remove Main Folder Name from Chili List

Investigator's Conclusion: Pinpointed the exact code (`ChiliItemUtility.mapChiliItemListToResourceDTOList()` using `buildOriginalAllClientsBasePath()` instead of `buildOriginalClientBasePath()`); proposed threading `clientRootPath` through and swapping the method; recommended a TTI story.

Actual Outcome: A developer implemented the fix locally exactly as described (folder name removed, subfolders retained), documented it, and raised draft PR #7518 for review.

Accuracy: Accurate (95%)

Notes: Precise, source-level root cause and fix that the developer implemented essentially verbatim; correctly reclassified as a dev enhancement.


==
41. Ticket #86209 — Need cutting selection added - Finishing Only - Rolls

Investigator's Conclusion: Job 4682668 has Zund Cut selected; "Summa Fabric Laser Cutter" isn't a device in largeformat_devices (closest is "Fab Laser Cut" op item); recommended confirming the correct selection or a config change and updating the job.

Actual Outcome: An agent found the PJC already includes Summa Cutting and the user can switch from Zund to Summa Fabric Laser Cutting when ordering (it's a reorder that carried Zund); still open awaiting Christi on whether it's a one-off or a product-level change.

Accuracy: Partially Accurate (60%)

Notes: Correct that it's a cutting-selection change on a reorder, but the investigator's "no such device / may need new config" framing was partly off — the Summa/Fab Laser option already exists in the PJC.

==
42. Ticket #86234 — Lifewise Sku Quantity Adjustments

Investigator's Conclusion: Parsed the garbled request table, listed current vs. requested actual/reserved/backorder per SKU, correctly noted "available" is derived (actual−reserved−backorder), and recommended confirming target values before updating.

Actual Outcome: The agent updated the inventory per the values Rachel provided and closed the ticket.

Accuracy: Accurate (85%)

Notes: Solid data reconciliation and correct handling of the derived "available" field; the recommended update matched the resolution (the confirmation step was reasonable diligence given the garbled input).

==
43. Ticket #86246 — Can't Select Shipping Method on Smartpress

Investigator's Conclusion: Diagnosed an account-specific "Error Fetching Shipping Quotes" as a blank Company/business-name field causing FedEx to reject the rate request; recommended setting the Company field.

Actual Outcome: Agents captured the actual client error — a 404 on `/vaultedFiles/v2/byFile` (reference_files, fileId 289720) — and the issue was fixed; the resolution was not about the company name.

Accuracy: Inaccurate (35%)

Notes: The blank-company-name hypothesis was not supported by the actual error (a vaulted reference-file 404); the investigator's speculative root cause did not match the evidence agents later captured.

==
44. Ticket #86247 — Collaterate will not open up any order window

Investigator's Conclusion: Hypothesized a release 4.44.0 FedEx `returnTransitTimes`/TTI-22985 breakage crashing the order detail load (and flagged a secondary AdminSalesEstimatesPage risk); recommended checking the property and logs.

Actual Outcome: Logs showed "Unable to find entity by id" → an Orika MappingException (BigDecimal→double on `pricingDiscountPercent` for SYSTEM_OFFERING_SITE_SHARE promo offerings); the issue was resolved. This matches the TEM-9510 BigDecimal→double Orika pattern noted in the channel.

Accuracy: Inaccurate (35%)

Notes: The FedEx transit-time root cause was wrong; the actual cause was an Orika BigDecimal→double mapping failure on promo-linked orders. The investigator did correctly note the data was intact and the failure was on load, but the specific cause missed.

==
45. Ticket #86248 — DQ - BULK ADD NOT WORKING

Investigator's Conclusion: Determined the bulk-add browse endpoint (`/products/bulkadd/browse`) was returning 0 products / erroring (distinct from the TK-267 add-to-cart 500), that catalog data exists, and recommended escalating to engineering to check the browse query and recent deploys.

Actual Outcome: Agents captured "Unknown exception in REST API URI (.../products/bulkadd/browse)" confirming the browse endpoint was throwing, reproduced across users, and it was fixed.

Accuracy: Accurate (88%)

Notes: Correctly isolated the failing browse endpoint (vs. the add-to-cart step) and that it wasn't a data problem; the captured error confirmed the diagnosis.


==
46. Ticket #86211 — Add open fields for Production Plan Details within Custom Quote

Investigator's Conclusion: Classified as a feature request; identified two Custom Quote systems (retiring legacy vs. live External Custom Quote), said the ECQ has no per-line-item production notes field, recommended a new TTI story and looping in Cameron Bjork.

Actual Outcome: The implementing dev's JIRA scoping explicitly corrected the investigator: it is a per-PRODUCTION-TASK field (not per-line-item), and a per-line-item note (`estimating_notes`) already exists and carries to the order. The feature was built (PRs #7549/#162) and QA-validated.

Accuracy: Partially Accurate (50%)

Notes: Correct that it's a feature request needing Cameron/TTI, but the core technical characterization (per-line-item; "no notes field exists") was materially wrong and formally rebutted by the developer.

==
47. Ticket #86251 — 2072834 - Error when attempting to open order

Investigator's Conclusion: Explicitly hit its 32-iteration limit without identifying the cause; reported the order data as structurally intact, flagged a null job_name and null PJC ids as possibilities, and recommended manual log investigation.

Actual Outcome: Closed as a duplicate of #86247 — the real cause (found there) was an Orika BigDecimal→double mapping failure on promo-linked orders. The investigator's flagged possibilities were not the cause.

Accuracy: Inaccurate (40%)

Notes: The investigator did not reach a conclusion (correctly self-flagged as inconclusive) and its speculative leads were wrong; it did correctly establish the data was intact and the failure was on load.

==
48. Ticket #86269 — [inaccessible]

Investigator's Conclusion: Not assessable — the ticket returned HTTP 403 "access_denied" and could not be fetched.

Actual Outcome: Not assessable — ticket inaccessible.

Accuracy: NOT ASSESSABLE (403 access_denied; not re-fetched per rules)

Notes: Flagged and excluded from statistics.

==
49. Ticket #86277 — Collaterate Error Message (partial credit)

Investigator's Conclusion: Confidently framed this as a recurrence of #85984 with the same OneSource tax-provider "no fallback in calculateSalesTaxAdjustment()" root cause; recommended retry and a permanent fallback fix.

Actual Outcome: Logs showed `AccessDeniedException` ("Access is denied") — a permissions issue; adding the "Accounting" role resolved it (the same actual cause as #85984, which was also permissions, not OneSource).

Accuracy: Inaccurate (30%)

Notes: The investigator doubled down on the incorrect OneSource root cause it had asserted on #85984; the real cause was a missing "Accounting" permission, confirmed by the AccessDenied log.

==
50. Ticket #86256 — Templated artwork not populating

Investigator's Conclusion: Jobs 4688241/4688244 share the same POD template session code (26ebc5f5) with `session_closed=true` but a NULL file URL and no captured template variables; concluded the session was wrongly shared across jobs, recommended dev recreate the sessions or manually attach artwork, and a possible TTI bug.

Actual Outcome: Agents reproduced ("templated pdf not yet available" / "Unable to get template document details"), could not retrieve the PDFs from Chili, and escalated to dev — resolution path is cancel/reorder or recreate the PDF from the data, matching the investigator's remediation.

Accuracy: Accurate (85%)

Notes: The shared-session/NULL-file-URL diagnosis is specific and consistent with the reproduced Chili template failure; the recommended remediation (recreate/reorder) matched what the team pursued.


==
51. Ticket #86289 — Lifewise Sku Qtys

Investigator's Conclusion: Compared the 3 requested SKUs' current DB values (including anomalous negatives) to Rachel's garbled table, correctly flagged "available" as derived and the backorder-column ambiguity, and recommended an admin update to the three variant records.

Actual Outcome: The agent adjusted the inventories per Rachel's values and closed the ticket.

Accuracy: Accurate (85%)

Notes: Correct data reconciliation and appropriate caution on the ambiguous backorder column; the recommended admin update matched the resolution.

==
52. Ticket #86290 — 2066221 - Customer Not Receiving Activity Log Emails

Investigator's Conclusion: Concluded SES infrastructure and site config were healthy and the issue was "most likely on the recipient's end" (corporate mail filtering at westcab.org), with SES-suppression-list checks recommended.

Actual Outcome: Agents found a WARN "no recipients specified" and a dev later confirmed "a temporary SES/queue delivery failure affected the notification sent on Sep 9"; the SES suppression list was checked and the address was NOT on it — pointing to a transient send-side failure rather than recipient filtering.

Accuracy: Partially Accurate (55%)

Notes: Correct that SES account/domain config was healthy and to check the suppression list, but the "recipient-side filtering" lean was not the confirmed cause — a transient SES/queue delivery failure was identified.

==
53. Ticket #86306 — Collaterate - Packingslip issues

Investigator's Conclusion: Identified a WAF rule (`BlockPrintablesOutsideAllowedIps`) on the Collaterate CloudFront distribution blocking printable URLs from non-TBG IPs; explained it as in-office works / remote blocked and recommended VPN.

Actual Outcome: Agents reproduced the 403 in both prod and stage for all orders/users; the team confirmed "This is a firewall rule that blocks the packing slip link in the item section when you're working off the TBG network," provided the Shipments-section workaround, and put a code fix in review.

Accuracy: Accurate (80%)

Notes: Correctly pinpointed the WAF/firewall block on printable URLs (the confirmed cause); the "remote-only, use VPN" framing was slightly narrow since a code fix was ultimately needed, but the fundamental diagnosis matched.

==
54. Ticket #86315 — Updated Email in a Username

Investigator's Conclusion: Located the inactive Jacob Kinney account (`adfs|healthmarket|a62197`) still holding `jkinney@healthmarkets.com` in `email`/`email_unique`, blocking reuse; recommended tombstoning both columns; confirmed no other account holds the email.

Actual Outcome: Config resolved it ("You are all set") — the stale email on the inactive account was freed exactly as the investigator described.

Accuracy: Accurate (90%)

Notes: Precise account/data identification and a correct, actionable fix that matched the resolution.

==
55. Ticket #86325 — 2074408 - Turn time is not carried over with envelope

Investigator's Conclusion: The auto-created envelope job uses the envelope offering's default turnaround rather than inheriting the parent product's selected turnaround; confirmed the pattern across multiple recent orders; recommended a code fix so the envelope inherits the parent's turnaround_time_id.

Actual Outcome: Dev (Cameron) confirmed "I should have a fix for the turn time out in the next Collaterate release" — validating the root cause and the code-fix direction.

Accuracy: Accurate (90%)

Notes: Correct systemic root cause (default vs. inherited turnaround on companion envelope jobs) with a fix confirmed by the developer.


==
56. Ticket #86334 — Date Issue in The Hub

Investigator's Conclusion: The 'Earliest of Kit or Ship Date' picker on Small Format Hub orders doesn't persist; hypothesized a frontend regression from the recently-updated TTI-22877 ("Remove Date Meta Fields from Hub Products", Sep 14), with good historical context (Small Format was intentionally left with active date fields). Recommended investigating that story/deploys.

Actual Outcome: Agents reproduced it in prod and stage across multiple SF products; CJ "found the issue" and applied a fix, though the reporter noted several small-format items still affected afterward (work ongoing).

Accuracy: Partially Accurate (70%)

Notes: Directionally correct (a config/metadata regression around Small Format date fields, which CJ addressed) with strong historical context, but the specific TTI-22877 link was an unconfirmed hypothesis and the first fix was incomplete.

==
57. Ticket #86352 — Permissions (can't locate support tickets)

Investigator's Conclusion: Compared Shannon Wamhoff's Collaterate roles to Doug Hartman's (identical) and concluded the gap was a FreshService agent/requester permissions issue, "no Collaterate permission changes are needed."

Actual Outcome: The config team responded "Permissions have been updated. Please check and confirm" — the issue was resolved by a permissions update (for locating/updating the in-Collaterate support/job tickets), contradicting the "it's FreshService, no Collaterate change needed" conclusion.

Accuracy: Partially Accurate (50%)

Notes: The role comparison was accurate, but the conclusion that no Collaterate change was needed and that it was purely a FreshService issue appears wrong, since a permissions update is what resolved it.

==
58. Ticket #86382 — Updated Email in a Username

Investigator's Conclusion: Located the (federated/ADFS) Scott Johnson account holding `sjohnson@healthmarkets.com` in `email`/`email_unique`, blocking reuse; recommended deactivate + update email_unique (or tombstone), noting no duplicate holds the email.

Actual Outcome: Account owner confirmed to retire the user; config "updated the email," freeing it — resolved exactly as the investigator described.

Accuracy: Accurate (90%)

Notes: Precise account/data identification and a correct fix that matched the resolution.

==
59. Ticket #86421 — THD Services sku 102461173-0001 adjustment

Investigator's Conclusion: Showed current vs. requested values and correctly caught that the requested Actual 6 / Reserved 6 / Backordered 6 yields Available −6, not the stated 0; recommended clarifying before updating.

Actual Outcome: The agent surfaced the same available-math discrepancy; Rachel corrected "backordered should be 0," and the inventory was adjusted accordingly.

Accuracy: Accurate (90%)

Notes: The investigator's arithmetic catch was exactly what drove the clarification and correct resolution.

==
60. Ticket #86432 — Lifewise backorder issues

Investigator's Conclusion: Inventory was received (actual_inventory incremented) but the backorder-relief step didn't fire (`backordered_quantity_adjustment = null`), leaving items still backordered despite ample net-available stock; itemized which could/couldn't be relieved; recommended running the drift-correction and filing a dev ticket for the warehouse receiving → backorder-relief gap.

Actual Outcome: CJ ran the drift-update script (twice, refining it), reallocated backorders, and forwarded the receiving-workflow root cause to the developers (Cameron/Asif). Requester confirmed fixed.

Accuracy: Accurate (90%)

Notes: Thorough, correct root cause (receiving not relieving backorders) with the drift-script remediation matching what resolved it; the recommended dev follow-up was also pursued.


==
61. Ticket #86440 — FabrivuBacklit dropdown choice doesn't save in The Hub

Investigator's Conclusion: Confirmed via data that the Ink Configuration reverts to FabrivuFrontlit whenever Print Substrate = Buy-out on the TBG Dye Sub FabriVu product; dated the regression to ~Aug 25–26 and recommended a dev review of Hub front-end/PJC 450 changes plus an audit of affected orders.

Actual Outcome: The dev found the cause in the TBG_RollCalcLogic calc logic (it forces FabrivuFrontlit unless a Backlit substrate like Aberdeen/Berger is selected); CJ fixed it and asked for a hard refresh.

Accuracy: Accurate (80%)

Notes: Correctly identified the exact reproducible behavior/scope, but attributed it to a recent front-end regression whereas the actual cause was existing calc-logic/config; the localization to that product's ink-config was right.

==
62. Ticket #86470 — Automatic Set Creation not working on Exact Reorders

Investigator's Conclusion: Traced it in code — auto set creation's only trigger is Pace activity 21005 (File Prep Complete), which is intentionally skipped for exact reorders, so the proofPreparation queue never fires; recommended adding an alternative trigger path in pa-api-gateway.

Actual Outcome: The dev (David Platt) confirmed exactly this ("set creation has only ever had one trigger: File Prep 21005; exact reorders stopped generating a file prep record") and implemented a fix triggering on the 1-Up file arriving instead.

Accuracy: Accurate (92%)

Notes: Precise, code-level root cause confirmed verbatim by the implementing developer, with a matching fix approach.

==
63. Ticket #86479 — Order 2076725 Shipping (refund short by tax)

Investigator's Conclusion: The shipping refund credited $104.57 instead of $189.99 because tax was subtracted rather than added; called it a bug in the shipping refund logic (tax passed as negative) and recommended a dev fix plus a manual $85.42 correction.

Actual Outcome: The dev found the true cause — the ship-to address was changed MO→MN (to an internal DC) before the refund, so OneSource recalculated total tax higher ($112.81→$155.52); the $42.71 delta was correctly-owed additional tax that the system netted out. Not a code bug — an address-change-driven recalculation.

Accuracy: Partially Accurate (55%)

Notes: Correct on the exact numbers and that tax was netted against the refund, but misattributed the cause to a shipping-refund code bug; the actual cause was the pre-refund ship-to address change triggering a legitimate tax recalculation.

==
64. Ticket #86527 — Order 2077654 - shipping inaccurate?

Investigator's Conclusion: Concluded the higher final shipping is legitimate — the address was flagged residential, routing to FedEx Home Delivery ($47.67) vs. the FedEx Ground estimate ($33.33); backed by a strong historical comparison showing prior orders were non-residential. No refund warranted.

Actual Outcome: The agent reproduced the $47.67 FedEx Home Delivery quote for the same address and confirmed to the customer the charge is accurate (residential classification). Closed.

Accuracy: Accurate (90%)

Notes: Correct root cause (residential → Home Delivery surcharge) with solid supporting evidence; the reproduction matched the investigator's conclusion.

==
65. Ticket #86528 — Collaterate Archive / Close mechanism (feature/dev request)

Investigator's Conclusion: Confirmed the "Archive/Close" flag sets orders.closed=true but does NOT cancel items, release reserved/backorder inventory, or trigger accounting; quantified the 539 UHG orders bulk-closed (3,367 units still in backorder, ~$14.5K unrealized revenue, no audit log); recommended remediation and disabling/restricting the bulk action.

Actual Outcome: Ticket routed to the team ("will look into it"); the investigation directly substantiated the author's own hypothesis with concrete data.

Accuracy: Accurate (90%)

Notes: Thorough, data-backed analysis matching and extending the requester's concern; correct behavior characterization and actionable remediation, though final disposition is still pending.


==
66. Ticket #86551 — Add Hybrid ReBoard to Dropdown Media Selection

Investigator's Conclusion: Concluded the Hybrid ReBoard substrate (PID# 30795) "does NOT exist in the database" and must be created in Pace, added as a new print_substrates record, and linked to the Board Printing (530) and Finishing Only (389) classifications.

Actual Outcome: Christi Chapin replied that the material is already available — "You can find this material under Reboard Hybrid - 6MM." No creation was needed.

Accuracy: Inaccurate (35%)

Notes: The core conclusion (substrate missing) was wrong; the investigator searched by "hybrid"/PID 30795 and missed the existing "Reboard Hybrid - 6MM" material, sending it down an unnecessary create-substrate path.

==
67. Ticket #86556 — Error Message - DONE4YOU

Investigator's Conclusion: Diagnosed a spurious "QUANTITY... CANNOT EXCEED 0" cart-validation error as a front-end bug misfiring on POD products (validator wrongly checking inventory on non-tracked items); recommended a dev bug ticket.

Actual Outcome: The agents could not reproduce the issue in Prod or Stage; it resolved after the customer cleared their browser cache. It was a client-side cache/stale-state issue, not a validation-logic bug.

Accuracy: Inaccurate (40%)

Notes: Over-diagnosed a code bug (even inventing a plausible validator mechanism) where the actual cause was a stale browser cache resolved by a cache clear.

==
68. Ticket #86563 — SEPHORA INVENTORY ID 16770 - adjust backordered qty

Investigator's Conclusion: Interpreted "16770" as a site_offering_variants.id, found it belonged to the inactive Wilson Fulfill site with all-zero inventory, flagged a "mismatch," and said it could not map the ID — recommending the agent ask Rachel to clarify the ID source.

Actual Outcome: The agent simply adjusted the backordered quantity as Rachel requested (a routine inventory adjustment) and confirmed it done.

Accuracy: Inaccurate (35%)

Notes: The investigator misidentified the record and stalled on a clarification request; the actual fix was a trivial backorder-qty adjustment that required none of the investigator's suggested clarification.

==
69. Ticket #86566 — 2049820 KOHLER - Order Build Error (Missing SKU) - On Hold

Investigator's Conclusion: Concluded SKU S-1583734 "does not exist anywhere in the database" and must be created as a new variant, then revert the order to On Hold, resolve the log entry, re-trigger the build, and re-send the EDI 850.

Actual Outcome: Christi Chapin found the SKU was already in Collaterate but hidden (segment visibility) — she made it visible for segments with none assigned; Parin Patel then re-triggered the build successfully and the EDI 850 was sent as two POs.

Accuracy: Partially Accurate (50%)

Notes: Wrong on the root cause (claimed the SKU was missing when it existed but was hidden by segment visibility), but the downstream re-trigger/EDI 850 steps matched the actual resolution.

==
70. Ticket #86582 — 2070094 - Back adhesive option gone

Investigator's Conclusion: Found the PJC config is correct and identified the print substrate's self_adhesive=true flag (Metalized Poly: Mirrored Silver) as the most likely trigger suppressing the back-laminate option; recommended a dev review/bug ticket and manual workaround.

Actual Outcome: The config team confirmed exactly this — the substrate is self-adhesive so back adhesive defaults to None, an intentional change from ticket 84874. The requester then pushed back that users should still be able to add a back lam when needed; still open/under discussion.

Accuracy: Accurate (80%)

Notes: Correctly pinpointed the self_adhesive mechanism, but framed intended behavior as a likely bug; the underlying "should back lam still be selectable" question remained unresolved at last update.


==
71. Ticket #86586 — packing slips won't open again

Investigator's Conclusion: Produced an elaborate root cause — a CloudFront WAF block (BlockPrintablesOutsideAllowedIps), deployed for HackerOne-reported critical vulns TTI-23001/TTI-23044, was blocking external access to /siteadmin/printablePackingSlip; recommended VPN/internal access and prioritizing the security fix.

Actual Outcome: The agent simply directed the user to the "Shipments" section to generate the packing slip for the reopened order; the user replied "it works now."

Accuracy: Inaccurate (30%)

Notes: The WAF/security-vulnerability theory was entirely off; the real issue was the user using the wrong UI path for a shipped/reopened order, resolved in two replies.

==
72. Ticket #86597 — Shipping Estimates Add on? (FedEx Home Delivery in estimator)

Investigator's Conclusion: Concluded GROUND_HOME_DELIVERY already exists and is in the estimator's service list, but the product-page estimator can't do residential detection without a full street address and an active cart — a known limitation; recommended collecting a full address or adding a disclaimer.

Actual Outcome: The dev (MOD) confirmed exactly this — Home Delivery was recently added to the estimator modal, but "when a Cart is null... we cannot raise Home Delivery," which was likely this customer's case; the team is discussing removing the product-page modal. Closed.

Accuracy: Accurate (92%)

Notes: Root cause and the null-cart mechanism were confirmed almost verbatim by the developer; framed correctly as an enhancement/limitation, not a bug.

==
73. Ticket #86610 — Create Master Alert Buttons (feature/dev request)

Investigator's Conclusion: Scoped the feature — 5 boolean alert flags on order_items mirrored to DynamoDB via sls-prepress-queue; needs a bulk order-level endpoint + order-header UI with mixed-state handling; quantified scale (82,917 alerted rows) and flagged the page-lag as a separate bug; recommended a TTI story.

Actual Outcome: Ticket routed to the team ("looking into it") and remains open; no contradicting information surfaced.

Accuracy: Accurate (88%)

Notes: Thorough, technically credible feature scoping consistent with the request; implementation still pending so the end state is unverified but nothing contradicts it.

==
74. Ticket #86636 — CCRM Order #2060324 - Templates Not Available

Investigator's Conclusion: Diagnosed missing edoc_template_name/edoc_template_code on system_offering_site_share 135849 plus an abnormal shared ChiliPublish session as the cause of the "unable to get template document details" error; recommended populating the template config and re-personalizing the two jobs.

Actual Outcome: The dev (Kyle Hauser) couldn't access the files, logged it to an ongoing JIRA issue, and set the workaround as either cancel the orders or get template data from the customer so the team can rebuild the files. Still open awaiting customer input.

Accuracy: Partially Accurate (65%)

Notes: Detailed and plausible diagnosis, but the specific missing-config root cause was neither confirmed nor applied; the practical resolution (rebuild from customer-provided template data / cancel) only partially aligns with the investigator's re-personalization note.

==
75. Ticket #75899 — Product Sets - possible to add total weight of set? (feature/dev request)

Investigator's Conclusion: Confirmed it is a valid feature already converted to Jira TEM-10195; validated the weight data model, computed a sample total (~10.35 lbs for "Opening Kit - Canada"), flagged a NULL-weight edge case, and concluded no action needed on the FS ticket.

Actual Outcome: The ticket was closed and converted into Jira work TEM-10195 (assigned to Mohith Kannan) — exactly as the investigator stated.

Accuracy: Accurate (90%)

Notes: Correctly confirmed the triage/Jira conversion and added genuinely useful implementation detail (data model, SQL, edge case); this was an old Feb ticket reactivated only to be converted to Jira.


==
76. Ticket #86661 — Request for Ban on Images/Special Characters in Rich Text Fields (feature/dev request)

Investigator's Conclusion: Confirmed RichTextEditor.tsx has no paste sanitization; quantified the problem in the DB (1,672 order_internal_notes with base64 images, 34,478 with Unicode); proposed a handlePaste interceptor to strip images and normalize Unicode; recommended a small-scope TTI story.

Actual Outcome: Triaged and assigned to Matt Tonak for decision/approval; still open. No contradicting information.

Accuracy: Accurate (90%)

Notes: Thorough, evidence-backed feature analysis with a concrete, correctly-scoped implementation path; matches the requester's ask.

==
77. Ticket #86662 — Tracking upload (HLOL tracking not populating Jira/Service Channel)

Investigator's Conclusion: Concluded the shipment events were never enqueued (routeEventsHandler Lambda showed zero invocations); root cause is that manually setting an order to Shipped doesn't fire the event (matching prior incident TTI-21227); recommended manual tracking push and a durable engineering fix.

Actual Outcome: The agent (MOD) confirmed exactly this — the orders were placed manually, and only automatically-processed orders (with a populated "Jira #" field) write back to Jira; for manual orders the tracking must be entered manually.

Accuracy: Accurate (90%)

Notes: Root cause (manual orders don't propagate to Jira/Service Channel) matched the agent's explanation precisely; the recurring-issue framing and manual-push remedy aligned with the actual response.

==
78. Ticket #86674 — Envelope Split incorrectly

Investigator's Conclusion: Confirmed all reported split errors against the DB (wrong product ENV-STA-OOO-MKT vs Business Envelope, wrong A7 type, missing Insert task, missing mailing permit, wrong Print task); root cause = auto-split logic mis-resolving the companion envelope product; recommended immediate manual corrections plus an engineering fix.

Actual Outcome: The agent reproduced every reported point in staging, and the dev team identified a fix planned for the 10/14 release.

Accuracy: Accurate (90%)

Notes: Findings were reproduced point-for-point and a code fix was scheduled — strong corroboration of the investigator's confirmed-bug conclusion.

==
79. Ticket #86675 — Save and Cancel Buttons Covered by Notification/Error Bar (feature/UI request)

Investigator's Conclusion: Diagnosed the fixed-position "growl" notification bar overlapping the Save/Cancel buttons on the proof/turnaround colorbox panels; named the source files; proposed three fix options (reduce maxHeight, lower z-index, add padding); recommended a low-risk TTI fix.

Actual Outcome: The agent confirmed the root cause to Matt Tonak, attached a detailed investigation/implementation doc, and asked whether to extend the fix to other admin panels. Still open pending approval.

Accuracy: Accurate (90%)

Notes: Root cause was confirmed and carried directly into an implementation plan; the multi-panel scope question the agent raised mirrors the investigator's own "systemic fix" note.

==
80. Ticket #86724 — Square roll labels (work ticket reading "circle")

Investigator's Conclusion: Concluded the shared "Roll Labels: Circle/Square" classification (ID 2130) drives the work-ticket label and there is no square-only classification — a naming-convention issue, not a data bug; recommended a dedicated classification, a display-source change, or a special-instruction workaround.

Actual Outcome: The config lead could NOT reproduce — test orders in both Prod and Stage all placed correctly as "square," not circle; concluded it was a one-off (possibly two tabs open) that resolved itself.

Accuracy: Inaccurate (40%)

Notes: The shared-classification theory did not match reality; the issue was transient/non-reproducible, so the investigator's structural root cause and remediation options were unnecessary.


==
81. Ticket #86736 — API For Box (feature/integration request)

Investigator's Conclusion: Classified it as a feature/integration request (not an incident), summarized Box's guidance that automated email upload is unsupported and the Box Direct Upload API is the supported path, scoped the integration (inbox monitoring + Box API + auth), and recommended a scoping meeting and dev routing.

Actual Outcome: The agent set up an initial discussion meeting with Theresa, then placed the ticket on hold as she decided to try the email path once more.

Accuracy: Accurate (88%)

Notes: Correct classification and a sound, well-scoped integration assessment; consistent with the meeting/hold outcome, though the final approach is still undecided.

==
82. Ticket #86738 — Brochure product (4/4 → 4/0 pricing not updating)

Investigator's Conclusion: Concluded the Brochures (PJC 5) and Trifold (PJC 29) classifications are missing the "None" (ink_id 6) Side-2 ink option, so the pricing engine defaults to CMYK and keeps the 4/4 price; recommended adding ink_id 6 via admin config.

Actual Outcome: The config lead tested and found pricing DOES work in Collaterate ("Test pricing seems to be working... The UI on the front end is not grabbing it"); it was routed to the tiger team / Matt Tonak, who logged a Jira bug against the new brochures product-page app — a front-end issue, not a missing PJC ink config.

Accuracy: Inaccurate (35%)

Notes: The missing-"None"-ink root cause was contradicted by testing; backend pricing was correct and the real defect was in the new brochures front-end app not picking up the price.

==
83. Ticket #86739 — Tracking in Collaterate not populating in Jira (non-manual orders)

Investigator's Conclusion: Concluded this was "expected behavior, not a bug" — the sync only fires when the Jira tracking field changes; tracking was added later, so it synced on Sept 28 and the manual upload was unnecessary; recommended no action.

Actual Outcome: The dev found the true root cause — the Collaterate→Jira sync DID run but Jira REJECTED the update because the combined tracking list exceeded the 255-character "Tracking Number" field limit (18-20 UPS packages = 358-398 chars). A recurring issue (7 orders since late July), not expected behavior.

Accuracy: Inaccurate (30%)

Notes: The "worked as designed / delayed tracking" conclusion was wrong; this was a genuine, recurring failure caused by a Jira field-length limit that the investigator missed entirely.

==
84. Ticket #86770 — Cannot log into Collaterate

Investigator's Conclusion: Noted the ticket lacked user/site/error detail, confirmed prod infrastructure healthy, listed generic possible causes (inactive account, failed-login lockout, an active SES complaint-rate alarm possibly blocking reset emails), and recommended requesting more detail.

Actual Outcome: The config lead simply reset the user's (Nik Dainsberg) password, which got them logged in — a routine password reset.

Accuracy: Partially Accurate (50%)

Notes: The investigator couldn't identify the user and produced a broad speculative assessment; the "check account / password reset" direction was reasonable, but the analysis added little value versus the trivial password-reset fix.

==
85. Ticket #86799 — HUB - Unable to Reorder

Investigator's Conclusion: Concluded job 4167985 is blocked from self-service reorder because it is itself already a reorder (reorder_original_id set), and the HUB intentionally blocks reorders-of-reorders; recommended CSR assistance.

Actual Outcome: The agent reproduced it, but the config lead gave the real reason — on Feb 13 the job's material had been changed to a special admin-only material ("z_...MAGNUM RECYCLED MAGNET"), and jobs with admin-only special materials can't be reordered via the button. The customer accepted the explanation.

Accuracy: Partially Accurate (50%)

Notes: Correct that the block is intentional, but the specific mechanism was wrong — the actual blocker was the admin-only special material, not the reorder-of-a-reorder lineage the investigator emphasized.

==
86. Ticket #86802 — HUB Order 2083830 - Integration Issue?

Investigator's Conclusion: Confirmed the order exists in Collaterate but its 5 items were never processed into Pace (production_status null, no Step Functions execution, empty intake queue, no DLQ traces); assessed the ORDER_CREATED event was likely never published/silently dropped; recommended manually triggering the Pace integration and checking the monolith's publish logs.

Actual Outcome: Ticket still open — the agent replied "Checking" with no resolution yet at last update.

Accuracy: Accurate (85%)

Notes: Thorough, evidence-based integration diagnosis internally consistent with all gathered signals; the specific root cause and outcome remain unverified since the ticket had no resolution at capture time.


==

# Summary Statistics

Ratings are based solely on evidence contained in each FreshService ticket (the Investigator's `[AI Comment]` versus the agent/dev/customer resolution). Three tickets are excluded from all counts: #85546 (index 2) and #86269 (index 48) returned 403 access_denied and could not be assessed, and #85335 (index 6) had NO `[AI Comment]`. Accuracy bands: Accurate = 85-100%, Partially Accurate = 50-75%, Inaccurate = <50%.

## Table 1 — August 31, 2026 (carry-over day; single ticket #85496)

| Metric | Value |
|---|---|
| Total assessed | 1 |
| Accurate | 1 |
| Partially Accurate | 0 |
| Inaccurate | 0 |
| Average Accuracy | 90.0% |

## Table 2 — September 1-30, 2026

| Metric | Value |
|---|---|
| Total assessed | 82 |
| Accurate | 41 |
| Partially Accurate | 25 |
| Inaccurate | 16 |
| Average Accuracy | 70.3% |

## Table 3 — Combined (August 31 + September)

| Metric | Value |
|---|---|
| Total assessed | 83 |
| Accurate | 42 |
| Partially Accurate | 25 |
| Inaccurate | 16 |
| Average Accuracy | 70.6% |

Excluded from all tables (3): #85546 (403), #85335 (no AI Comment), #86269 (403). The file contains 86 numbered ticket entries in chronological order (oldest first); 83 of them carry an assessable accuracy score.

==

# Key Observations

## Common ACCURATE ticket types
The Investigator is consistently strong (85-100%) on:
- **Data/config lookups and adjustments**: inventory/backorder adjustments (#85556, #85496), reused email_unique lookups, and confirming whether a specific data value is correct.
- **Feature/dev-request scoping with correct routing**: it reliably recognizes enhancement requests, confirms the data model, and points to the right repo/Jira project (e.g., #86610 master alert buttons, #86661 rich-text paste sanitization, #86675 growl-bar overlap, #75899 product-set weight → TEM-10195, #86528 archive/close). Several of these matched the eventual dev plan almost verbatim.
- **Source-level root-cause pinpointing on genuine bugs** confirmed by the implementing dev: #86470 (exact-reorder 21005 trigger gap — confirmed word-for-word), #86674 (envelope auto-split — reproduced point-for-point, fix scheduled 10/14), #86597 (Home Delivery null-cart limitation — confirmed by MOD), #86662 (manual-order tracking not writing to Jira — confirmed).

## Common reasons for PARTIAL accuracy
- **Right symptom/numbers, wrong or unconfirmed root cause.** The Investigator nails the observable facts but misattributes causation — e.g., #86479 (correct math on the refund shortfall but called it a code bug when it was an address-change tax recalculation), #86636 (plausible missing-template-config theory, neither confirmed nor the actual fix).
- **Correct that a block is intentional, wrong on the mechanism** — #86566 (SKU "missing" vs. actually hidden by segment), #86799 (reorder-of-reorder vs. actual admin-only special material).
- **Broad/speculative when the ticket lacks detail** — #86770 (login) produced a wide differential where the fix was a trivial password reset.

## Common reasons for INACCURATE ratings
- **Over-confident speculative root causes, especially inventing a code/architecture bug where the real cause was transient, cache/config, or process:** #86556 (declared a front-end validation bug; actually a browser-cache issue that a cache-clear fixed), #86724 (shared-classification theory; actually a non-reproducible one-off), #86586 (elaborate WAF/security-vuln theory; actually the user was on the wrong UI path), #85687/#85984/#86277 (doubled-down speculative OneSource/permissions causes).
- **Declaring something "missing" that actually exists** because the search missed it: #86551 (Hybrid ReBoard substrate "doesn't exist" — it did, under a slightly different name), #86563 (misread the inventory ID, stalled on clarification when a routine adjustment was all that was needed).
- **Misclassifying a real failure as "expected behavior":** #86739 (called it working-as-designed; the true cause was Jira rejecting the update due to a 255-char tracking-field limit — a recurring failure).
- **Backend-confirmed-correct but blamed the wrong layer:** #86738 (blamed a missing PJC ink option; testing showed pricing worked and the defect was in the new front-end brochures app).

## Recurring gap between the Investigator's recommendation and the actual resolution
The dominant pattern is **depth without confirmation**: the Investigator frequently produces a detailed, technically fluent root-cause narrative (often naming specific tables, columns, Lambdas, or source files) that reads authoritatively but is **unverified**. When the actual cause turned out to be a permissions/visibility setting, a transient cache issue, a config/data value that already existed, an intentional business rule, or a downstream constraint (e.g., a field-length limit), the confident narrative was wrong or beside the point. It is markedly more reliable when the answer is a data lookup or a feature-scoping exercise, and least reliable when it speculates about *why* something failed without a confirming signal (logs showing the actual error, a reproduction, or dev confirmation). It also tends to frame intentional/expected behavior as a "likely bug."

## Was August 31 omitted from the prior month's audit?
August 31 carried a single ticket, #85496, which appears in this window as a carry-over. It was rated Accurate (90%) here. Its presence as a standalone carry-over day — rather than being folded into an August audit — is consistent with it having been **omitted from the prior (August) month's audit** and picked up at the start of this window. It is reported separately (Table 1) precisely so this one carry-over data point does not distort the September-only figures.

## Accuracy change: August 31 vs. September
The single August 31 data point (90%, Accurate) sits **above** the September average (70.3%). One ticket is far too small a sample to claim a trend — it simply happened to be one of the Investigator's stronger ticket types (a straightforward inventory/appearance lookup). September's larger sample (82 tickets) shows the fuller, more mixed picture: roughly half Accurate (41/82), about 30% Partially Accurate (25/82), and about 20% Inaccurate (16/82), pulled down mainly by the speculative-root-cause failures noted above.
