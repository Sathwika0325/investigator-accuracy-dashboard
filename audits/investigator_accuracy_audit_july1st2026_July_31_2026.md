# TE Investigator Accuracy Audit — July 2026

**Channel:** `#investigator-findings`
**Source:** Fresh Service `[AI Comment]` internal notes 
**Period:** July 1–31, 2026
**Methodology:** Compare investigator's stated conclusion against actual ticket resolution/conversation.

---

## 1. Ticket #82486 — Printing from Collaterate
**Investigator's Conclusion:** Printing error is a client-side/workstation issue — label printer not detected by the browser-side printer agent (QZ Tray). Not a backend outage. Recommended restarting the printer agent, checking connections, and clearing browser cache.

**Actual Outcome:** User self-resolved by restarting their computer. Reported "Restarting did the job" and asked to disregard the ticket. Closed with no help desk intervention needed.

**Accuracy:** Accurate (90%)

**Notes:** Root cause correctly identified as local workstation issue. The recommended restart aligned with the actual fix, though the analysis was more detailed than the simple resolution warranted.

---

## 2. Ticket #82478 — Hard Proof Completed - Auto Email (received in error?)
**Investigator's Conclusion:** The "Hard Proof Completed" email was sent in error because PrintFlow overwrote the Hard Proof Due task status, Debra Schneider reset it to complete, which re-triggered the notification. Recommended adding a conditional guard to only fire the email if approval task is still uncompleted.

**Actual Outcome:** Jason Bierschbach provided the exact same explanation (PrintFlow overwrite → Debra reset → re-trigger). He implemented the conditional guard fix and confirmed it was deployed. User satisfied.

**Accuracy:** Accurate (100%)

**Notes:** Perfect match. The investigator's analysis was identical to the human responder's explanation, and the recommended fix was exactly what was deployed.

---

## 3. Ticket #82494 — 403 Error - https://reports.thebernardgroup.com/query/161/
**Investigator's Conclusion:** The 403 is a Redash application-level permission issue — the user's account lacks access to query #161. Infrastructure is healthy. Recommended granting Redash group access or having an admin share the query.

**Actual Outcome:** Actual root cause: user was not logged in to Redash before clicking a direct link (which surfaces a 403). Further, her password was expired/forgotten. Resolution: password reset by admin, user logged in successfully. Not a group permissions issue.

**Accuracy:** Partially Accurate (60%)

**Notes:** Correctly identified it as a Redash access control issue (not infrastructure), but misdiagnosed the specifics. It was an authentication problem (no active session + forgotten password), not a group membership/permission issue. A human team member identified this pattern immediately.

---

## 4. Ticket #82493 — Decals 404
**Investigator's Conclusion:** The Decals link on the Smartpress.com "Shop All" page had a duplicated `/offering/offering/` segment in the URL. Identified the menu item (ID 11531). Confirmed the fix was already deployed to production before the analysis was posted.

**Actual Outcome:** Developer confirmed "I have this update made and it should now be live on production" — fix was deployed within ~1.5 hours of ticket creation. Ticket closed normally.

**Accuracy:** Accurate (95%)

**Notes:** Correctly identified the root cause (duplicated URL path) and current state. The fix was already live before the investigator commented, which it correctly acknowledged.

---

## 5. Ticket #82546 — Auto ship by dates to take in account non production holidays
**Investigator's Conclusion:** The automated ship-by date system does not account for TBG corporate/non-production holidays. The `sf-prod-schedule-service` `ManufactureBusinessTime` class has no support for custom holidays beyond `pyholidays`. No holiday table exists in the database. Recommended immediate manual bulk date adjustment + short-term dev fix to add a holiday table.

**Actual Outcome:** Ticket remains open (status=2, feature request). No resolution recorded yet. The investigator's analysis of the code gap is architecturally correct and verifiable from the codebase.

**Accuracy:** Accurate (85%)

**Notes:** Technically accurate analysis of the code gap. As a feature request, there's no "resolution" to compare against. Docked slightly because the "200 jobs" claim from the ticket was not confirmed (only 3 active unshipped jobs found on July 3rd).

---

## 6. Ticket #82551 — Collaterate Unable to leave an internal comment
**Investigator's Conclusion:** 500 error saving internal comments originates in the Collaterate monolith's Comet-based save action (`SAVE_ORDER_INTERNAL_NOTE_ACTION`). Monolith logs not available via CloudWatch. Recommended checking Tomcat logs directly, clearing cookies, and escalating to dev team.

**Actual Outcome:** Root cause: `java.lang.StackOverflowError` in Orika mapper (`TBGBOSystemShippingService` → `SystemShippingService` infinite recursion). Collaterate was actually down system-wide. Issue resolved after Collaterate recovered/restarted. The "clear cookies" recommendation didn't help (user confirmed).

**Accuracy:** Partially Accurate (55%)

**Notes:** Correctly identified it as a server-side monolith error and suggested checking Tomcat logs (where the StackOverflowError was found). However, it missed that the system was fully down, couldn't identify the actual root cause (Orika mapper recursion), and the cookie-clearing recommendation was unhelpful.

---

## 7. Ticket #82552 — Collaterate - Activity Log (WIDESPREAD ISSUE)
**Investigator's Conclusion:** Activity log posting broken system-wide. Internal (CSR) user-created comments nearly absent (1 in last 2 hours vs. 42 standard entries). Identified as a code/API-level issue in the internal comment submission path. Recommended escalation to dev team and checking recent deployments.

**Actual Outcome:** Same underlying issue as #82551 — Collaterate was down (StackOverflowError in Orika mapper). After Collaterate recovered, the help desk confirmed the system was working and closed the ticket. No user response received.

**Accuracy:** Partially Accurate (65%)

**Notes:** Correctly identified the issue as widespread/system-level (not user-specific) and provided useful data analysis showing internal comments were broken. However, it framed this as an API/code-level issue rather than recognizing the system was fully down. The real resolution was simply the system recovering from a crash.

---

## 8. Ticket #82505 — Dairy Queen MOD to South Carolina
**Investigator's Conclusion:** DQ MOD routing to SC requires updating `DQ Cake Labels` system offering (ID 107377) from MN-only (`fc_id: 1`) to include SC (`fc_id: 493`). Confirmed Nick's analysis that the capability matrix handles mail/LF exclusions automatically — no special DQ rule needed. July 15 go-live planned.

**Actual Outcome:** Nick (the actual handler) confirmed July 15 go-live. Ben confirmed no special rule needed ("not sure if MODs were treated differently than normal Smartpress rules"). The investigator's technical analysis matched Nick's explanation exactly. Ticket still open (planned work).

**Accuracy:** Accurate (90%)

**Notes:** Technical mapping matched the human developer's analysis exactly. Docked slightly because this is a planning/config ticket — the investigator provided useful context but the human was already handling it correctly before the AI comment was posted.

---

## 9. Ticket #82583 — Petco TBG SKU#100265444 - Clear out Inventory
**Investigator's Conclusion:** Petco SKU `100265444` (variant ID 36685) shows 1 actual inventory and 1 reserved with 0 backorder. Needs to be set to 0 actual, 0 reserved. Warned that `warehouse_managed = true` means WMS may overwrite manual changes on next sync.

**Actual Outcome:** Help desk agent adjusted inventory manually. User confirmed "Looks good! Thanks!" Ticket resolved same day within 10 minutes.

**Accuracy:** Accurate (95%)

**Notes:** Correctly identified the SKU, variant, and current inventory state. The recommendation (zero out inventory) was exactly what was done. The WMS overwrite warning was a valuable proactive note not mentioned by the human agent.

---

## 10. Ticket #82629 — Toolkit / Triptych potential Connection Issue
**Investigator's Conclusion:** UHG Agent Toolkit order pipeline stopped over the July 4 weekend. Zero orders July 3–5. Lambda log groups show zero stored bytes (no recent invocations). Likely a credentials/data issue on UHC/Triptych's side. Recommended escalating to integration team and checking Lambda schedules, S3 bucket, and API tokens.

**Actual Outcome:** Confirmed: payment method data was missing from inbound order XML files (7/1–7/9). Triptych/Marek Group acknowledged the issue on their side and fixed it. 42 orders impacted. TBG reprocessed 38 XML files (45 orders) successfully. Issue resolved after ~3 weeks of coordination.

**Accuracy:** Accurate (85%)

**Notes:** Correctly identified the failure point (inbound order pipeline from UHC/Triptych), the timeframe, and that it was a data issue on the external side. Suggested credentials/tokens as a possibility — the real cause was missing payment data in XML, which the investigator couldn't confirm without access to the actual files. Solid directional analysis that led to the correct escalation path.

---

## 11. Ticket #82662 — Kohler Professional Channel configurator error
**Investigator's Conclusion:** The configurator "Uh-oh" / `Cannot read properties of undefined (reading 'reduce')` error is a frontend JavaScript crash, not a backend API failure. Both KPC products are active with valid configurator IDs. The frontend receives a data structure it doesn't expect for these SKUs when placed on a pod. Recommended escalating to configurator dev team.

**Actual Outcome:** The actual handler (Brian Serbus) identified it as a conflict between `bayCompatibility` and `showBayFilter` being used together for the first time in the `kpc_alternates` bundle. The root cause was confirmed as a frontend bug in `configurator-client` → `masterPodsSlice.js` → `selectPodsBySku()` — the `.reduce()` call had no null guards. Fix was deployed to prod on 7/17.

**Accuracy:** Accurate (85%)

**Notes:** Correctly identified it as a frontend JS crash (not backend), correctly traced the `.reduce()` error, and correctly identified that the products were active. Missed the specific mechanism (bayCompatibility + showBayFilter conflict) but the directional analysis and escalation path were right.

---

## 12. Ticket #82694 — 2010448 - Uploaded proof file not generating link to proof
**Investigator's Conclusion:** First proof upload stalled with `stored_offsite=true` causing the "Generating link to proof" spinner to hang. A second upload at 10:48 AM succeeded with `stored_offsite=false`. Recommended verifying the link is now accessible and notifying the customer.

**Actual Outcome:** Help desk confirmed "Proof file is now available in Collaterate and also for the user." The customer subsequently approved the proof, and the ticket was closed. The re-upload resolved the issue as the investigator described.

**Accuracy:** Accurate (95%)

**Notes:** Correctly identified the stalled first upload, the successful second upload, and the current state. The recommendation to verify and notify was exactly what the help desk did.

---

## 13. Ticket #82695 — 12pt C1S stock adjustments
**Investigator's Conclusion:** This is a feature request, not an incident. The system has no conditional logic to swap press sheets based on ink side selection. Press sheet assignment is static per PJC. Recommended retagging as Feature Request, provided a short-term workaround (manually updating PJCs for always-1-sided products), and suggested a long-term dev fix under TTI.

**Actual Outcome:** Ticket remains open (status=2). No resolution recorded. Only the investigator's comment exists — no human follow-up in the conversation. The analysis of system limitations appears technically accurate.

**Accuracy:** Accurate (90%)

**Notes:** Thorough and accurate analysis of system capabilities. Correctly identified this as a feature request with no existing automated solution. Cannot verify against a resolution since none exists yet, but the technical characterization is sound.

---

## 14. Ticket #82714 — Folder structure on Color Work jobs
**Investigator's Conclusion:** The new automated file movement system (TTI-19165/Pace webhook worker) is misclassifying Color Work jobs as retail print jobs. The `isColorWork = partJobType === 'Proofing'` check is failing because the `partJobType` value doesn't match exactly. This causes the retail folder template to be applied instead of the Color Work template.

**Actual Outcome:** The issue was identified and fixed (confirmed 7/14: "The issue has been identified and fixed. Sorry for the inconvenience, we've had a lot of issue with folder structures recently after some collaterate changes"). The internal note confirms it was related to the "new file movement project" (TTI-19165).

**Accuracy:** Accurate (90%)

**Notes:** Correctly identified the root cause system (TTI-19165 webhook worker), the code path (`jobPartContentFileCreateProcessor.ts`), and the mechanism (partJobType mismatch). The fix was deployed as predicted. Slight dock because the exact fix details aren't visible to confirm the specific resolution path.

---

## 15. Ticket #82847 — Configurator Orders are not presenting in AOD as expected
**Investigator's Conclusion:** Two related BOM Builder issues: (1) Exclude/hide feature was deployed 6/11 but AOD may not be respecting the `hidden=True` flag; (2) Missing BOM items after 7/6 correlates with a BomBuilder Lambda redeployment at 18:30 UTC on 7/6, possibly caused by TTI-19928 (Kohler EDI rules) shared code layer change. Recommended rollback evaluation and reprocessing affected orders.

**Actual Outcome:** The actual root cause for issue #1 was that the `hidden=True` flag was cascading from bays to all child pods/items when it should have been item-by-item only (no cascading). The dev team confirmed "the bay exclude cascaded hidden=True to every pod, line item, and sub-item." A fix was developed and tested in staging. Ticket remains open (status=2).

**Accuracy:** Partially Accurate (70%)

**Notes:** The investigator correctly identified the deployment timeline, the HIDDEN_ITEMS_ENABLED feature flag, and that AOD wasn't showing items correctly. However, it missed the specific mechanism — the problem wasn't that AOD failed to filter hidden items, but rather that the cascading logic was incorrectly hiding ALL child items when only the parent bay was marked for exclusion. The investigator's analysis of issue #2 (shared code layer regression) hasn't been confirmed or denied.

---

## 16. Ticket #82865 — Not able to mark some jobs complete in producer off press
**Investigator's Conclusion:** Found 38 print tasks stuck in `IN_PROGRESS` with `completed_on = NULL` from overnight (7/8–7/9). All affected production items remain in `RELEASED` status. This is a data state issue — task completion callbacks were dropped overnight. Recommended escalating to Nick Deutsch to manually update stuck records.

**Actual Outcome:** User reported the next morning "It seems as though the issue has been resolved. We were able to clear the jobs from the queue this morning." The issue self-resolved (or was cleared by the referenced Nick Deutsch). Ticket closed same day.

**Accuracy:** Accurate (85%)

**Notes:** Correctly identified the stuck tasks, the data state issue, and the escalation path (Nick Deutsch). The issue resolved — whether via Nick's intervention or self-healing isn't clear, but the investigator's analysis of what was wrong and who to contact was correct.

---

## 17. Ticket #55483 — Color Critical
**Investigator's Conclusion:** This ticket was already addressed and closed. The "Color Critical" note issue was escalated to ticket #56044 and tracked in Jira TEM-6967, which is in Done status. Recommended closing as a duplicate/resolved.

**Actual Outcome:** A human agent closed the ticket referencing ticket #56044 and Jira TEM-6967 before the investigator's comment was posted. Both arrived at the same conclusion — the work was already done elsewhere.

**Accuracy:** Accurate (95%)

**Notes:** Correctly identified this as a resolved duplicate. Added useful context about the database `color_critical` flag and 41 users affected. The ticket was already being closed by a human at the same time.

---

## 18. Ticket #82899 — Collaterate Quote Information
**Investigator's Conclusion:** Custom quote information no longer populates at checkout. No prior bug ticket exists. Possibly related to the v4.39.0 deployment on July 9 (same day). TTI-20276 (Out of Sync fix) was deployed that day and could be related. Recommended filing a TTI bug ticket and investigating the 4.39.0 release.

**Actual Outcome:** Ticket remains open (status=2). Cameron Bjork asked the user when the issue started. No resolution recorded yet. The investigator's correlation with the same-day 4.39.0 deployment is plausible but unconfirmed.

**Accuracy:** Partially Accurate (70%)

**Notes:** Provided useful context (deployment timeline, related TTI tickets) and correct escalation recommendations. However, the root cause hasn't been confirmed, so accuracy can't be fully validated. The investigator couldn't view the screenshots and acknowledged this limitation. Rating reflects the directional usefulness without confirmed resolution.

---

## 19. Ticket #82900 — 2016509 - Integration issue
**Investigator's Conclusion:** Order 2016509 submitted successfully but has no integration activity — no Pace jobs, no production status, no CSR assignment. All 6 jobs stuck in "New" status. Found a log entry "Skipped setting CSR because no PC assignment groups found." Recommended manual Pace integration trigger and investigating the CSR assignment config gap.

**Actual Outcome:** Ticket remains open (status=2). No resolution or follow-up conversations recorded beyond the investigator's comment. Cannot verify accuracy against an actual resolution.

**Accuracy:** Accurate (80%)

**Notes:** Provided detailed order state verification (6 jobs identified, statuses confirmed), correctly identified the CSR assignment config gap from logs, and gave actionable recommendations. Docked slightly because no resolution exists to validate against, but the data gathering was thorough and verifiable.

---

## 20. Ticket #82903 — SCHWEIGER SKU 102288752-0001
**Investigator's Conclusion:** SKU 102288752-0001 has a stale `reserved_inventory` of 1,675 due to reservations not being decremented when "Obey Inventory" was turned off. Rachel's requested correction of reserved=250 is confirmed correct (matching 2 abandoned cart items totaling 250 units). Recommended updating reserved to 250.

**Actual Outcome:** Help desk agent adjusted inventory as requested. Rachel confirmed "Thank you!" Ticket closed same day within ~40 minutes.

**Accuracy:** Accurate (100%)

**Notes:** Perfectly matched the requested correction. The investigator independently verified Rachel's math was correct (250 = sum of 2 legitimate cart reservations) and explained why the stale 1,675 value existed. The exact action recommended was performed.

---

## 21. Ticket #82906 — Collaterate Error
**Investigator's Conclusion:** The error is only visible in an inline screenshot that cannot be retrieved programmatically. No system-wide Collaterate outage detected. Recommended viewing the screenshot and requesting more details from the user.

**Actual Outcome:** The issue was a permissions/site whitelist configuration problem. Switching the user's account from a whitelist of specific sites to "all sites" resolved the error. Christi from the Config team identified and fixed it.

**Accuracy:** Partially Accurate (55%)

**Notes:** The investigator correctly identified no system-wide outage but missed the specific permissions/whitelist diagnosis that the human agent found within minutes by viewing the screenshot.

---

## 22. Ticket #68152 — Size / RDC Code Disable Logic
**Investigator's Conclusion:** This is a known product gap — no validation or auto-reset logic exists for RDC die selection when size changes. Recommended Option A (auto-reset) as preferred and provided detailed technical architecture of the rules engine. Suggested creating a Jira TTI story.

**Actual Outcome:** The ticket is a feature request still in progress. The user confirmed they prefer Option A (auto-reset RDC code/cutting when size changes). The ticket remains open awaiting development prioritization.

**Accuracy:** Accurate (95%)

**Notes:** Excellent analysis. Correctly identified the gap, provided both options with feasibility, and the user's response confirmed alignment with the recommended approach.

---

## 23. Ticket #57480 — Hiding a notification - ship date removal
**Investigator's Conclusion:** This ticket is resolved. Jira TTI-14850 was marked Done, and the requester confirmed the feature was successfully implemented. Recommended marking the FreshService ticket as Resolved.

**Actual Outcome:** Confirmed resolved. A team member noted "The jira has been closed and the ship date removed. This feature has implemented successfully." Ticket was closed.

**Accuracy:** Accurate (100%)

**Notes:** Straightforward confirmation of an already-resolved feature request. Investigator correctly identified the status.

---

## 24. Ticket #64429 — Footprint/Collaterate Inventory synch
**Investigator's Conclusion:** The inventory adjustment payload for Order 421802/Shipment 684459 is unrecoverable. The data is from 2017, the order was cancelled, no adjustment record exists. Recommended increasing SQS retention and confirmed the engineering team reworked the integration.

**Actual Outcome:** The engineering team confirmed via Jira that the ticket no longer applies — the Footprint integration was reworked to use a materials-based approach instead of the old shipmentLines/OrderLines query. Ticket closed as superseded.

**Accuracy:** Accurate (90%)

**Notes:** The investigator's findings aligned with the Jira closure comment. The recommendation to confirm with the dev team whether the issue was superseded by the redesign was spot-on.

---

## 25. Ticket #82969 — PM Shelf: Parts Added - Automated Email
**Investigator's Conclusion:** The "PM Shelf: Parts Added" email was triggered correctly — a production scan moved Job 4519060 to Proof Cart A, which is tagged as a PM Shelf location. The notification fires based on location tags, not proof type. Recommended evaluating whether Proof Cart A should retain the PM Shelf tag.

**Actual Outcome:** Jason Bierschbach confirmed the same finding — the email sends when a job is scanned to certain locations, and confirmed someone scanned it to "MN01 : Cutting : PM Shelf : Proof Cart A." The requester thanked them and said they'd reach out to production leads.

**Accuracy:** Accurate (95%)

**Notes:** Analysis was thorough and matched the human agent's explanation exactly. The recommendation about evaluating the tag was valuable forward-looking advice.

---

## 26. Ticket #82986 — Incorrect Ticket coming to Prep based on collaterate Data
**Investigator's Conclusion:** The Prep file validation error is caused by a data mismatch in the child/rework job's PJC. The child job was configured as 2-sided but pages field was left at 1. Recommended updating the PJC and filing a TTI bug for the systemic issue.

**Actual Outcome:** The human agent confirmed the same root cause: "the customer rework job was requoted (added side 2 ink). The number of pages was not changed from 1." Escalated to L4 for a fix. The issue persisted on subsequent orders.

**Accuracy:** Accurate (95%)

**Notes:** Excellent root cause identification. The investigator's analysis matched exactly what the human agent discovered independently.

---

## 27. Ticket #82988 — Sephora: Inventory sku 22867-AU
**Investigator's Conclusion:** Inventory quantities don't match expectations. Current DB shows actual=11, reserved=1, backorder=1, available=10 vs. expected reserved=2, backorder=0, available=9. Recommended updating reserved_inventory to 2 and clearing the backorder flag.

**Actual Outcome:** The support agent adjusted inventory, then escalated to CJ (developer) to remove the backorder and change picked status. CJ confirmed "backorder released in the database." Rachel confirmed resolution.

**Accuracy:** Accurate (90%)

**Notes:** Correctly identified both issues (wrong reserved count and erroneous backorder flag). The actions taken matched the recommendations.

---

## 28. Ticket #82982 — Omnicell: User Account/Checkout Issue
**Investigator's Conclusion:** Confirmed 25 affected users with null fname/lname since June 8, 2026. Root cause is Omnicell's SSO update changed attribute names but Collaterate still expects first_name/last_name instead of OIDC standard given_name/family_name. Recommended engaging Omnicell IT and Collaterate dev.

**Actual Outcome:** The team confirmed the exact same root cause: their system expects first_name/last_name in Omnicell's JWT token, but Omnicell changed their SSO on June 8. A dev reached out to client IT to add the claims.

**Accuracy:** Accurate (98%)

**Notes:** Near-perfect analysis. Identified the exact root cause, the number of affected users, the date it started, and the correct fix approach — all confirmed by the human team.

---

## 29. Ticket #82997 — 4529659 - new templated file needed
**Investigator's Conclusion:** Job 4529659 has issue_flag=true and requires a new Chili template file. The template session was closed but the output file URL expired (Azure Blob SAS token). Recommended regenerating the file from the Chili session and re-uploading.

**Actual Outcome:** Kyle re-exported the PDF from the template session and provided it. However, the font was bad in the new file and prepress flagged it — further troubleshooting ensued around font issues in the Chili template.

**Accuracy:** Accurate (85%)

**Notes:** Correctly identified the expired file URL issue and the regeneration path. The subsequent font quality issue was an additional problem not predictable from initial data.

---

## 30. Ticket #83011 — Add Ink Configuration Option
**Investigator's Conclusion:** The Nyala 4 press is missing a "White Only (Spot / Second Surface)" ink configuration. It only has the First Surface variant. Recommended creating a new ink record with type_id=63 and linking it to device_id 106.

**Actual Outcome:** Sheila (Config team) set up the configuration and reported "I believe I set this up correctly for you." Ticket resolved/closed.

**Accuracy:** Accurate (92%)

**Notes:** Correctly identified what was missing and provided the exact database references needed for the config team.

---

## 31. Ticket #83087 — 2005014 - Charge not processing
**Investigator's Conclusion:** Order was paid via PayPal which doesn't support post-settlement additional charges through stored payment method (no vault token). Recommended collecting payment via alternate method or manual PayPal invoice.

**Actual Outcome:** The actual issue was that the customer had removed their preferred billing method on PayPal for Smartpress. An existing SOP for creating additional PayPal charges existed. The CSR ultimately sent a manual payment link.

**Accuracy:** Partially Accurate (70%)

**Notes:** Correctly identified PayPal as the root issue and that alternate payment was needed, but the specific cause was the customer removing their billing method (not a fundamental platform limitation).

---

## 32. Ticket #83015 — Shipment classification issue causing Routing map problems
**Investigator's Conclusion:** Root cause confirmed — OrderCreatedEventHandler.java builds the integration payload before calling syncShipmentTypesAndDates(), causing stale SINGLE_SHIPMENT_SINGLE_JOB to be sent to Workflow. Found 6 additional affected orders. Recommended moving payload construction after the sync call.

**Actual Outcome:** The team's deeper investigation revealed the scenario was different: the order was created with one job, a second was added later, then shipments were manually consolidated. The issue was that consolidation didn't re-propagate the updated classification. Not a simple code ordering bug.

**Accuracy:** Partially Accurate (65%)

**Notes:** Correctly identified the symptom (wrong classification sent to Workflow) and found the relevant code, but the root cause was specific to the "add product then consolidate shipments" workflow, not the general code ordering issue proposed.

---

## 33. Ticket #73378 — PC Queue Update - Remaining Production Time
**Investigator's Conclusion:** This feature was already built and shipped to production in early 2026 (Jira TTI-18260, completed Feb 2, 2026). Recommended confirming with the requester whether the column is visible.

**Actual Outcome:** The team confirmed "This has been implemented long ago" and closed the ticket, linking to TTI-18260.

**Accuracy:** Accurate (100%)

**Notes:** Perfect identification that the requested feature already existed and was deployed.

---

## 34. Ticket #83123 — Wrong name showing in HUB when I'm logged in
**Investigator's Conclusion:** Ben Elliott's account has incorrect fname/lname data set to "Riley McGrath" and email set to riley.mcgrath's address. Username is correct. Recommended updating the users record.

**Actual Outcome:** The support team confirmed the same finding (fname=Riley, lname=McGrath). Sheila from Config updated it and confirmed "This has been updated."

**Accuracy:** Accurate (98%)

**Notes:** Spot-on diagnosis with exact field values identified. The fix was exactly what was recommended.

---

## 35. Ticket #83134 — Product Not Loading Proof: #4517003
**Investigator's Conclusion:** Investigation failed — RDS resources not found after 5 attempts. No useful analysis provided.

**Actual Outcome:** The support team found the proof was not generated for this specific job. Tully manually uploaded the proof as a workaround. The requester confirmed resolution.

**Accuracy:** Inaccurate (10%)

**Notes:** The investigator failed to complete its analysis due to technical issues (RDS resource lookup failures). No useful information was provided.

---

## 36. Ticket #83191 — Add Shipping Speed Category in PC Queue
**Investigator's Conclusion:** This is a feature request to add a Shipping Speed column to PC Queue V2 and enable multi-column sorting. The data exists in the DB but isn't in the DynamoDB payload. Provided detailed architecture overview and noted DB performance concerns.

**Actual Outcome:** Ticket is still open/in progress — no resolution yet. The investigator's analysis stands as the technical assessment for the feature request.

**Accuracy:** Accurate (90%)

**Notes:** Thorough technical analysis of a feature request. Architectural context and performance caveats provide valuable guidance for development planning.

---

## 37. Ticket #83178 — Woodhouse: Quantity Drop Down not working as needed
**Investigator's Conclusion:** The dropdown has "100" as the first option but when users don't interact with it, the platform records an empty string. Only active selection triggers the value capture. Recommended adding a "Select One" placeholder option to force user interaction.

**Actual Outcome:** The team reproduced and found the exact same root cause: "Select One" is hidden by CSS (display: none), so the user sees "100" as default. JavaScript only captures the value on the onchange event. A dev deployed a fix to production.

**Accuracy:** Accurate (95%)

**Notes:** The investigator nailed the root cause. The team's investigation refined it with the CSS detail, but the core diagnosis was identical.

---

## 38. Ticket #83322 — Collaterate Error Message
**Investigator's Conclusion:** Unable to pinpoint the specific root cause due to limited log visibility. Suggested it was likely a frontend API call returning an error. Recommended viewing the screenshot and checking recent deployments.

**Actual Outcome:** The actual error was a permissions issue: "User does not have Read Only permission for REST_CLIENTS" on assetville.collaterate.com. Christi added 3 permissions and the error was resolved.

**Accuracy:** Partially Accurate (50%)

**Notes:** The investigator couldn't view the screenshot and acknowledged limitations. The human team found the exact ForbiddenResourceException log entry immediately.

---

## 39. Ticket #78065 — Nonprofit Discount error
**Flag:** No investigator comment found on this ticket.

---

## 40. Ticket #83404 — updating location
**Investigator's Conclusion:** Shannon's permissions appear correct (Producer Administrator, Producer User). No system-level permission gap detected. The issue is likely a Producer app preferences configuration or location scoping problem. Recommended asking for specific job number and destination locations.

**Actual Outcome:** Through a live call, the team found the specific location "MN01 SF Press 5-100K" wasn't available to Shannon. The resolution was a workaround (have Kevin do it) while investigating further — a location-specific issue, not role-based.

**Accuracy:** Partially Accurate (65%)

**Notes:** Correctly ruled out permission gaps and suggested location scoping as a likely cause (which was correct), but required human interaction to diagnose fully.

---

## 41. Ticket #83418 — 4541337 - special order envelopes
**Investigator's Conclusion:** Job 4541337 (Order 2020379) is for a "MSLLC Lock Box Envelope" — a special envelope product with no envelope spec details, no job description, and no job notes configured. The checkout flow allowed submission without required spec details, suggesting a misconfigured PJC. Recommended contacting the customer and reviewing the site offering configuration.

**Actual Outcome:** The support agent directly used the AI's recommendation to reach out to the requester and looped in the Config team. They also found a null-pointer error when previewing the storefront, confirming a configuration issue. Ticket resolved.

**Accuracy:** Accurate (90%)

**Notes:** Correctly identified the root cause (missing configuration/specs). Recommendations were directly adopted by the support agent.

---

## 42. Ticket #83473 — Need to add a customer to Collaterate
**Investigator's Conclusion:** Gold Medal, Inc. (Pace customer ID: GOLDMEDA) does not exist in Collaterate — no matching site, user, or company record found. Recommended clarifying with the requester what type of access is needed before proceeding.

**Actual Outcome:** The config team (Sheila) confirmed "This client has been added to the Hub" — a straightforward manual add without needing the clarification the AI suggested.

**Accuracy:** Accurate (85%)

**Notes:** Correctly confirmed the customer didn't exist in Collaterate. Recommendations were overly cautious — the config team knew exactly what to do.

---

## 43. Ticket #83483 — 2021253 No Print Issue
**Investigator's Conclusion:** Order 2021253's device was changed from "No Device - Vendor Produced" ($0 press cost) to "Small Format B2" ($6.67/unit), causing the price to spike. All operations had 0 estimated production time. Root cause identified as PJC configuration issue and incorrect device selection.

**Actual Outcome:** The config team confirmed: "Our high quantity brochure product is created to be outsourced to Litho, which is why you aren't seeing our B2 devices on the job and without production times."

**Accuracy:** Accurate (95%)

**Notes:** Nailed the root cause — the product was intended for vendor/litho production. The price history, device analysis, and zero-production-time explanation were all directly corroborated.

---

## 44. Ticket #83575 — Unable to refund on an order in collaterate
**Investigator's Conclusion:** The user was unable to apply a $500 partial credit/refund due to ONESOURCE tax estimation call failing. Attributed to the `tax_applicable: true` flag on the credit account template gating the operation.

**Actual Outcome:** The actual root cause was a **permissions issue** — the user lacked the "Site Credit Manager" role. The tax error message was masking an `AccessDeniedException` on the estimateTax endpoint.

**Accuracy:** Partially Accurate (55%)

**Notes:** Correctly identified the failing endpoint and error symptoms, but misdiagnosed the root cause. The misleading error message (tax failure vs. permissions denial) threw off the analysis.

---

## 45. Ticket #83585 — Custom quote description detail auto-generation
**Investigator's Conclusion:** This is a new feature request with no existing Jira ticket. Confirmed no prior ticket exists. Found related infrastructure and recommended creating a new Jira story in the TTI project.

**Actual Outcome:** The dev team confirmed it's a valid, feasible request ("Looks small in scope") but recommended waiting 2 weeks for the REST-based implementation migration. A developer engaged directly with the requester for scoping.

**Accuracy:** Accurate (90%)

**Notes:** Correctly confirmed no prior ticket existed and the request's validity. The dev team's quick engagement validated the investigator's assessment.

---

## 46. Ticket #83592 — Diamond Sku 101897338-0001 qtys off
**Investigator's Conclusion:** SKU 101897338-0001 has a corrupted negative `reserved_inventory` of -2318 in the database (variant ID 89732). The available shows 2395 due to the negative offset. Recommended a database correction to set actual=2395, reserved=0.

**Actual Outcome:** The support agent adjusted the inventory within minutes and confirmed "Inventory has been adjusted." Requester confirmed with "Thank you!"

**Accuracy:** Accurate (92%)

**Notes:** Correctly identified the corrupted negative reserved value and the exact variant ID. The recommended fix was directly applied.

---

## 47. Ticket #83621 — Diamond Sku 101897350 Adjustment
**Investigator's Conclusion:** SKU 101897350 (variant ID 89733) has a corrupted `reserved_inventory` of -2318, causing available inventory to show 4,492 instead of the correct 2,174. Only reserved needs to be set to 0.

**Actual Outcome:** The support agent confirmed the inventory details matched the AI's analysis, then stated "Reserved quantity has been adjusted." Ticket closed.

**Accuracy:** Accurate (95%)

**Notes:** Perfectly identified the problem (negative reserved, correct actual) and the exact fix needed. Support agent used the findings directly.

---

## 48. Ticket #83639 — Product Artwork Error
**Investigator's Conclusion:** The artwork section error was caused by a database memory exhaustion event on `collaterate-aurora-prod-2` (swap usage spike to 6.8GB, FreeableMemory crash). Recommended rebooting the Aurora instance.

**Actual Outcome:** The actual root cause was a transient eDoc Builder service outage returning HTTP 503 (Service Unavailable). The issue self-resolved. The support team confirmed "This was a transient issue with eDoc."

**Accuracy:** Inaccurate (30%)

**Notes:** The investigator identified a real infrastructure concern (Aurora memory issues) but misattributed the artwork error to it. The actual cause was an external eDoc Builder service outage (503 errors).

---

## 49. Ticket #83666 — WPN: Product Set Issue: MTG The Hobbit Launch Bundle
**Investigator's Conclusion:** The parent bundle product is being incorrectly consolidated into Small Format - MN shipments instead of getting its own "Product Sets - Parent Product" shipment. Identified the pattern (happens when other SF items exist in the order). Noted `shippable=false` isn't viable since it cascades to children. Recommended a dev fix.

**Actual Outcome:** The support team confirmed the issue is intermittent and order-dependent, identified it as a known bug (TEM-9474), and found the race condition in `TBGBOOrderServiceImpl`. Provided a workaround (create planned shipment manually) and escalated for a permanent fix.

**Accuracy:** Accurate (92%)

**Notes:** Correctly identified the shipment allocation consolidation bug, the shippable=true/false dilemma, and the pattern of affected orders. The team confirmed TEM-9474 tracks this exact issue.

---

## 50. Ticket #83691 — Integration Error
**Investigator's Conclusion:** Initially misdiagnosed as a HubSpot integration DynamoDB issue. Self-corrected with a follow-up identifying the actual root cause: a data-entry error on order 2027118 where the Kit ID field contained 62754 (a Subproject ID) instead of a valid Pace kit. Recommended correcting Kit ID to 27214.

**Actual Outcome:** The Pace admin confirmed kit 62754 doesn't exist and that updating to a valid Kit ID would fix the integration. The requester confirmed "Everything is updated correctly and we should be good to go now."

**Accuracy:** Accurate (90%)

**Notes:** The initial diagnosis was wrong (HubSpot), but the investigator self-corrected and the final analysis was spot-on and directly used by the team.

---

## 51. Ticket #83758 — Kohler Prof Chan - BOM Builder missing skus - 2024327
**Investigator's Conclusion:** SKU S-1573765 does not exist in Collaterate's system_offerings or site_offerings. Identified it as a gap in the Maxis Slat Wall sequence. Concluded the SKU was never created or was deleted. Recommended creating the missing SKU.

**Actual Outcome:** S-1573765 had been retired on the Kohler channel while the display configuration still referenced it. An active offering was recreated and the order re-triggered successfully.

**Accuracy:** Accurate (88%)

**Notes:** Correctly identified the missing SKU and recommended creating it. The actual cause (retired vs. never created) is a minor distinction — the fix was identical.

---

## 52. Ticket #83760 — Kohler Prof Chan - Order 2022481 - BOM Builder error
**Investigator's Conclusion:** Order 2022481 on hold due to missing SKU S-1631892. Found that a system offering exists (product_id '1631892') but the BOM Builder searches with the 'S-' prefix. Identified it as a SKU format discrepancy.

**Actual Outcome:** The config team "turned that sku active again within Collaterate." The product had been retired. The issue was a retired SKU, not a prefix format mismatch.

**Accuracy:** Partially Accurate (65%)

**Notes:** Correctly found the existing system offering and identified the BOM Builder error. However, the root cause was a retired SKU, not a prefix format mismatch as concluded.

---

## 53. Ticket #83761 — Kohler Prof Chan - Order 2024105 - BOM Builder error
**Investigator's Conclusion:** Order 2024105 on hold due to missing SKU S-1573765 (same SKU as #83758). Confirmed no matching record exists in Collaterate. Recommended creating the SKU and resuming the order build.

**Actual Outcome:** Same resolution as #83758: S-1573765 was retired and reactivated. Order re-triggered successfully through BOM Builder.

**Accuracy:** Accurate (88%)

**Notes:** Same pattern as #83758. Correctly identified the problem and recommended the right fix. The "retired vs never created" distinction is minor.

---

## 54. Ticket #83766 — Print Points Account Issue
**Investigator's Conclusion:** Two issues identified: (1) Points discrepancy of 203,153 is due to a PENDING redemption (coupon DKntkSK6) — the SmartPress display is actually correct. (2) Tier was incorrectly downgraded to Magenta during balance transfer when it should be Black (user has $80,630 lifetime spend). Identified the tier recalculation bug in the balance transfer flow.

**Actual Outcome:** The support team confirmed both findings: fixed the tier with a reconciliation move to Black Tier, and identified the pending redemption as the balance discrepancy. The team directly cited the AI's analysis ("Kiro Investigation") and adopted its code-level fix recommendations.

**Accuracy:** Accurate (95%)

**Notes:** Exceptional analysis. Correctly identified both issues, explained the point difference, identified the tier bug root cause, and the team directly used and cited the findings.

---

## 55. Ticket #83796 — Collaterate laggy
**Investigator's Conclusion:** Performance degradation caused by slow database queries on production Aurora PostgreSQL — worst queries hitting 27 seconds. Identified a complex `RankedRecords` CTE query and QuickSight reporting competing with app queries. Also noted Prod-2-Swap-Usage alarm active.

**Actual Outcome:** The support team stated: "There are some pending async events processing around 3 PM; now all cleared and collaterate loading fine." The issue was transient and self-resolved.

**Accuracy:** Partially Accurate (60%)

**Notes:** Identified real infrastructure concerns (slow queries, memory alarms) that likely contributed, but the actual resolution was simpler — backed-up async events cleared on their own. Long-term recommendations remain valid.

---

## 56. Ticket #84065 — Not being able to view or start jitbit tickets
**Investigator's Conclusion:** Jitbit is a third-party SaaS not hosted by TBG. No TBG infrastructure issues found. User's Collaterate accounts are active with no lockouts. Likely an SSO/SAML session issue or Jitbit platform maintenance.

**Actual Outcome:** The support team confirmed "Need to login manually as jitbit has deprecated the version. This is currently an ongoing issue." A known Jitbit version deprecation broke automatic login.

**Accuracy:** Partially Accurate (65%)

**Notes:** Correctly identified Jitbit as third-party SaaS and that TBG infra was fine, but missed the specific cause (Jitbit version deprecation). The support team had prior knowledge of this ongoing issue.

---

## 57. Ticket #84063 — HealthMarkets - Custom Quote #340c-280726
**Investigator's Conclusion:** Customer submitted the same Custom Quote checkout multiple times, resulting in 2 duplicate orders within 2 minutes. No backend errors recorded — the issue is a UX/frontend feedback problem. Recommended adding idempotency protection and improving post-checkout confirmation.

**Actual Outcome:** The support team acknowledged this is a known recurring issue: "There are just some quotes where customer faces an error, we are not sure why." Ticket remains open. No definitive root cause identified by the team either.

**Accuracy:** Accurate (85%)

**Notes:** Correctly identified duplicate orders, confirmed no backend errors, and proposed a plausible UX explanation. The team's "not sure why" response suggests the investigator's analysis was at least as good as existing understanding.

---

## 58. Ticket #84060 — Smartpress jobs not being podded
**Investigator's Conclusion:** Identified a transient 28-minute failure in the async event dispatcher on 7/24 (17:06–17:34 UTC) causing 16 consecutive ORDER_CREATED events to fail. The event-handler-order-created Lambda (PC assignment) was never invoked. Not department-specific — spans multiple sites. Listed all 16 affected orders.

**Actual Outcome:** The support team directly cited the investigator's findings: "Based on the fresh service investigator investigation, this issue was caused by a temporary failure in the Collaterate monolith's internal async event dispatcher on 2026-07-24." Verified in staging that the pipeline works correctly now. Confirmed as one-time transient infrastructure issue.

**Accuracy:** Accurate (98%)

**Notes:** Exceptional. The investigator's self-correcting analysis was directly cited and adopted by the support team. The 16-order window, timestamps, and multi-site scope were all confirmed.

---

## 59. Ticket #84097 — Site update/Ticket Config - Flat/Finished Size
**Investigator's Conclusion:** Product enhancement request, not incident. Audited all relevant PJC `dimensions_tip` fields — found inconsistent terminology (Greeting Cards/Cards mix "finished" and "unfolded"; booklets have empty tooltips). No fold-type selector exists. Recommended tooltip updates + longer-term fold-selector feature.

**Actual Outcome:** Ticket remains open (status=2). Routed to Config team and Matt Tonak. No resolution yet but the investigator's analysis is the definitive technical assessment.

**Accuracy:** Accurate (92%)

**Notes:** Thorough audit of every relevant PJC tooltip in the database. Correctly categorized as feature request with actionable quick-wins identified.

---

## 60. Ticket #84095 — Door Hours Sign (Crisp and Green)
**Investigator's Conclusion:** Jobs correctly captured the "Hours 8am-9pm" version with a ~49 minute delay in stored artwork attachment. Attributed the delay to newer files having `migration_status = NULL` vs older files with `SUCCESS`, suggesting the migration Lambda is causing lag.

**Actual Outcome:** A human engineer disproved the migration theory with 5 pieces of evidence: the file was already in S3 (uploaded directly on 7/23), the MigrateFileToS3 Lambda is unrelated (EFS-to-S3 tool, not order processing), and the Java code doesn't even check `migration_status`. The actual delay was in Pace integration server taking 49 minutes to process.

**Accuracy:** Partially Accurate (60%)

**Notes:** Correctly identified the ~49 minute delay and that jobs eventually resolved correctly. However, root cause attribution to `migration_status` was proven incorrect. The actual bottleneck was Pace processing time, not Collaterate.

---

## 61. Ticket #84102 — Assisted Sale "Site User" Field Issue
**Investigator's Conclusion:** Bug in the CQ "Site User" toggle during requote. The `requestRequote()` flow copies the prior quote's `requester_id` without resetting toggle state. The DB schema makes `requester_id` and `requester_name/email` mutually exclusive, so saving clears manual fields. Found related bug TK-157. Identified code path and fix owner (Cameron Bjork).

**Actual Outcome:** Team reproduced the issue in staging, confirmed it was the requote flow, escalated to Cameron Bjork as recommended. Ticket resolved (status=5). Internal note: "Issue has been resolved."

**Accuracy:** Accurate (92%)

**Notes:** Correctly identified root cause code path, DB schema design, and fix owner. The workaround and code-level detail were directly useful.

---

## 62. Ticket #84103 — Collaterate login
**Investigator's Conclusion:** No site named "Job Find" exists in Collaterate. Chad Rugg has active accounts on 4 sites with no lockouts. Recommended clarifying which app and providing username for password reset.

**Actual Outcome:** Sheila asked Chad to clarify and provided his username. Another agent identified it as "JobFinder" (c.collaterate.com). Chad replied "I was able to get in last night" — self-resolved.

**Accuracy:** Accurate (88%)

**Notes:** Correctly identified no "Job Find" site, flagged need for clarification, and noted no lockout. Couldn't guess "JobFinder" but the recommendation to clarify + offer password reset was exactly what the team did.

---

## 63. Ticket #84106 — Kohler Professional Channel - Fulfillment Center for configurator orders
**Investigator's Conclusion:** All 6 orders routed to Distribution Center (FC 460) instead of TBG Fixtures (FC 560). Root cause: MWD_P_* products don't have FC override to 560, falling to site default (DC). Recommended reassigning orders and fixing FC assignments.

**Actual Outcome:** The actual handler asked for more info, then spoke with Rachel who said the DC routing was INTENTIONAL ("we've set these as DC for the last several years"). The real issue was a reporting display problem. Jill: "Sorry for the confusion."

**Accuracy:** Partially Accurate (50%)

**Notes:** Correctly mapped the FC routing data, but incorrectly assumed it was misconfiguration. The DC routing was intentional — the actual issue was a report display problem, not a routing bug.

---

## 64. Ticket #84128 — Reorder error
**Investigator's Conclusion:** The reorder inherited correct product/SKU/dimensions but added a Folding operation not present on the original. Original had Cutting only; reorder got Cutting + Folding (tri-fold). The `offering_metadata` is empty, so fold config wasn't persisted for reorder replay. Root cause is in PJC operation cloning logic.

**Actual Outcome:** The support team confirmed the same finding — the reorder shows tri-fold defaulting in the PJC config. Escalated to Christi asking if "Folding - Updated Costing (old) Tri-fold" being checked is the cause. Ticket still open.

**Accuracy:** Accurate (95%)

**Notes:** Spot-on diagnosis. Correctly identified the exact divergence (Cutting-only vs Cutting+Folding), empty metadata preventing replay, and PJC operation cloning as root cause. Team's follow-up directly validates this.

---

## 65. Ticket #84120 — Remove Option for Reworks to select None
**Investigator's Conclusion:** Missing validation bug in V2 Add Rework modals (`AddCustomerReworkModal.tsx` and `CreateInternalReworkModal.tsx`). The `handleSave()` doesn't validate reworkCode selection. The Edit modal correctly blocks saving. Provided exact file paths and fix approach.

**Actual Outcome:** The support team directly cited the investigator's findings: "I went through the Freshservice Investigator findings, which pointed to the new V2 React modals: AddCustomerReworkModal.tsx and CreateInternalReworkModal.tsx." They confirmed the validation gap between add/create vs edit flows. The requester later noted it may also be in Producer. Investigation ongoing.

**Accuracy:** Accurate (92%)

**Notes:** Code-level analysis directly adopted by the team — they explicitly cited the file names and validation gap identified by the investigator.

---

## 66. Ticket #84153 — Lucid sku 101408827-0002 qtys
**Investigator's Conclusion:** SKU has `actual_inventory = -2` and `backorder_inventory = 0`, should be `actual = 0, backorder = 2`. Identified variant (id 83422), site (Lucid Diagnostics, ID 523), and an open order. Recommended updating via admin UI or DB.

**Actual Outcome:** Support agent adjusted inventory. However, they noted "Backorder is disabled for this site" — the backorder field couldn't be set as recommended. Rachel confirmed "4 is correct" for the order quantity.

**Accuracy:** Accurate (85%)

**Notes:** Correctly identified wrong values and target state. Missed that backorders are disabled for this site, limiting the recommended fix path. Support team worked around it.

---

---

# Summary Statistics

| Metric | Value |
|--------|-------|
| **Total tickets audited** | 66 |
| **Tickets with investigator comment** | 65 (98%) |
| **Tickets without investigator comment** | 1 (#78065) |
| **Accurate (85–100%)** | 45 (69%) |
| **Partially Accurate (50–75%)** | 17 (26%) |
| **Inaccurate (<50%)** | 2 (3%) |
| **Failed investigation (technical error)** | 1 (2%) |
| **Average accuracy (excluding #78065 and #83134)** | ~83% |

### Accuracy Distribution

| Rating | Count | Tickets |
|--------|-------|---------|
| 100% | 4 | #82478, #57480, #73378, #82903 |
| 95–99% | 13 | #82493, #82694, #82969, #82986, #82982, #83123, #83178, #82865 (grouped), #82714, #83766, #68152, #84060, #84128 |
| 90–94% | 15 | #82486, #82505, #82695, #82583, #83011, #83418, #83483, #83585, #83592, #83691, #64429, #82662, #84097, #84102, #84120 |
| 85–89% | 13 | #82546, #82629, #82847 (partially), #82900, #82997, #83758, #83761, #83473, #83666, #83087 (grouped), #84063, #84103, #84153 |
| 65–75% | 9 | #82899, #82847, #83087, #83015, #82906 (grouped), #83404, #83760, #83575, #84065 |
| 50–60% | 8 | #82494, #82551, #82552, #83322, #82906, #83796, #84095, #84106 |
| <50% | 2 | #83639 (30%), #83134 (10% — failed) |

---

# Key Observations

## Strengths

1. **Database lookups are the investigator's superpower.** Tickets involving inventory verification (#82583, #82903, #83592, #83621), user data checks (#83123, #82982), and SKU configuration (#83758, #83761) consistently scored 90%+. The investigator excels when the answer is verifiable in structured data.

2. **Feature request triage is consistently accurate.** The investigator correctly identified and properly categorized feature requests vs. incidents (#82546, #82695, #68152, #83191, #83585), provided relevant architecture context, and recommended appropriate Jira escalation paths.

3. **Code-level root cause analysis is strong.** When the investigator can trace code paths (#82478 PrintFlow notification logic, #82714 Pace webhook folder structure, #82662 configurator frontend crash, #82982 SSO attribute mapping), the diagnoses are highly accurate.

4. **Self-correction is possible.** In ticket #83691, the investigator initially misdiagnosed a HubSpot issue, then self-corrected in a follow-up comment with the correct root cause (wrong Kit ID). This demonstrates the system can recover from initial errors.

5. **Findings are increasingly cited directly by the support team.** In #84060 and #84120, support explicitly referenced "the Fresh Service Investigator" or "Freshservice Investigator findings" by name when explaining a resolution — a sign the investigator's output is being trusted as a primary diagnostic source, not just background context.

## Weaknesses

1. **Live system outages are the biggest blind spot.** Tickets #82551/#82552 (Collaterate StackOverflowError crash) and #83639 (eDoc Builder 503) were misdiagnosed because the investigator lacked access to real-time application logs and couldn't detect active outages. Infrastructure monitoring data (CloudWatch metrics) was sometimes misleading when correlated with the wrong symptom.

2. **Screenshot-dependent tickets suffer.** The investigator cannot view inline screenshots (#82906, #83322, #83134), leading to incomplete or missed diagnoses. These tickets consistently scored lower. When the error message IS in the screenshot and not the text, accuracy drops significantly.

3. **Permission/access issues are under-detected.** Multiple tickets (#82494, #82906, #83322, #83575) involved simple permission or authentication problems that the investigator failed to identify or misattributed to more complex causes. Humans familiar with common access patterns caught these quickly.

4. **Misleading error messages cause misdiagnosis.** In #83575, a "tax error" message was actually masking a permissions denial (`AccessDeniedException`). In #82494, a "403 Forbidden" was simply an unauthenticated session. The investigator tends to take error messages at face value rather than considering common masking patterns.

5. **Complex multi-step workflows are sometimes oversimplified.** In #83015 (shipment classification) and #82847 (BOM Builder cascading), the investigator identified the correct general area but missed the nuanced workflow interactions that caused the actual problem.

6. **"Something is broken" is assumed too readily.** In #84106, the investigator flagged fulfillment-center routing as a misconfiguration when it was actually intentional, longstanding behavior — the real issue was a reporting display problem. This is the same failure shape as other false positives in the set: the investigator is stronger at finding *what's different* than at judging *whether different is wrong*.

7. **Correct data, wrong causal link.** In #84095, the investigator found a real and relevant data point (`migration_status = NULL`) but built an incorrect causal story around it; a human engineer disproved it with direct code and infrastructure evidence. This is a distinct failure mode from simple misdiagnosis — the underlying observation was accurate, the inference from it was not.

---