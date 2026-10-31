# TE Investigator Accuracy Audit — October 2026

**Period:** October 1–31, 2026

This audit scores each `[AI Comment]` posted by the TE Investigator (user 10002980302) on Freshservice tickets created in October 2026 against what the team actually found, confirmed and fixed.

---

## 1. Ticket #86876 — Printing packing slips from shipments page on producer is not working.

**Investigator's Conclusion:** Packing-slip printing from the Producer 2 shipments page was broken because the monolith's `GET /packingSlipPdfByShipmentId/{id}` endpoint returned a non-PDF response (Lambda relay throws 502 `legacy_bad_response`). It attributed this to a known engineering issue tied to the PDF Generator decommission project (TEM-10135) and a prior security remediation.

**Actual Outcome:** The developer found the real cause was a WAF allow-list outage (Sep 30 18:35 – Oct 1 08:43 CDT) after an InfrastructureLegacy CDK deploy emptied the trusted-IP list, so the printable pages returned a CloudFront 403. Re-running the IP sync fixed it and the requester confirmed. The requester reported it again on Oct 5, support said it was a known issue and then resolved it the same morning, and the requester acknowledged.

**Accuracy:** Inaccurate (30%)

**Notes:** The AI traced the right request chain (Producer 2 → monolith PDF endpoint) but blamed a decommission/remediation project instead of the WAF block, so the stated root cause was wrong.

---

## 2. Ticket #86882 — Delta Print Portal - unable to un-assign a pick and pack fee

**Investigator's Conclusion:** Most pick-and-pack fees on the Delta Print Portal (site 194) had already been cleared in the database that morning, but 28 shared-offering rows in `system_offering_site_shares` still carried a fee and were the likely reason the fee still showed. It could not reproduce or explain why the products-page wheel would not un-assign the fee and recommended a dev data fix plus a bug ticket.

**Actual Outcome:** A developer identified a code bug: the `ProductV2Provider` bulk patch always looks up the fee group, so a null (clear) value fails with "pick and pack fee could not be found". The developer also corrected that the 28 remaining share rows are all retired products and need no data fix. The code fix was approved on Oct 21.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI correctly flagged the UI inability to clear the fee as a bug needing a ticket, but its leading explanation (the 28 shared rows) was a red herring and it missed the null-handling root cause.

---

## 3. Ticket #86869 — Kohler Professional Channel - orders cannot be marked as shipped

**Investigator's Conclusion:** The error is accurate: each order still has unshipped jobs with no rows in `order_shipment_item_allocations`, so `canStatusBeShipped()` correctly refuses the change. It judged this a data problem on the orders rather than a code bug.

**Actual Outcome:** Support and dev found the orders contained hidden child product-set sub-jobs (created roughly Jul 7–21, 2026) saved as not visible to admins, so the admin could not mark them shipped. A DB fix was assigned after the triage call and the ticket was resolved on Oct 7, with about ten other orders affected.

**Accuracy:** Partially Accurate (65%)

**Notes:** The AI correctly called it a data problem on the orders (fixed by DB update) but did not identify the hidden/invisible sub-jobs or the wider set of affected orders.

---

## 4. Ticket #86905 — Norton Sku 101453310-0001

**Investigator's Conclusion:** Actual (0) and Backordered (0) were correct, but Reserved was -7, which made Available show 7. It traced the -7 to a warehouse pick on 2026-09-17 that released reserved units never recorded as reserved, and recommended setting `reserved_inventory` to 0 on variant 78864.

**Actual Outcome:** The support agent adjusted the inventory and sent a screenshot of the corrected quantities. The requester replied "Thank you!" and the ticket was closed.

**Accuracy:** Accurate (92%)

**Notes:** The recommended fix matched what the team did; the requester's expected quantities (all 0) agree with the AI's target values.

---

## 5. Ticket #86908 — Collaterate Reporting is showing stock allocation for a large job that has printed Job # 4701745

**Investigator's Conclusion:** It could not confirm the root cause. It suggested the 26,000-sheet allocation was an open planned-material line on a matching Pace job (L2077289) with nothing pulled, possibly counted by Redash report 713. It also noted the Collaterate order item was not shipped and still in `production_status_id = 4`.

**Actual Outcome:** The data engineer found the job's Collaterate production status was never advanced after printing (still "Queued For Print"), and report 713 counts jobs in that state as not yet printed. Production changed the status to printed and the requester confirmed it was fixed.

**Accuracy:** Partially Accurate (50%)

**Notes:** The primary Pace-planned-material theory was wrong, but the AI's last recommendation to check the Collaterate production status on the order item pointed at the real cause.

---

## 6. Ticket #86914 — Collaterate communication bug fix - Chat setting return to default

**Investigator's Conclusion:** The activity-log filter is deliberately persisted in browser `localStorage` (key `showActivityOptions`, shared by the legacy JSP page and the React order-details UI), so it carries over between orders by design. A follow-up comment found the change already tracked as TTI-24196 and noted it scopes out the legacy JSP page.

**Actual Outcome:** The team linked the ticket to TTI-24196 and assigned it to Jon Heer; the ticket remained open. No fix had been delivered or confirmed by the end of the ticket's activity.

**Accuracy:** Accurate (90%)

**Notes:** Nobody explicitly confirmed the cause, but the team's linking to TTI-24196 matches the AI's finding that this is existing sticky-filter behavior needing a story rather than a defect.

---

## 7. Ticket #86918 — MOD SITES - Homepage feature Menu- category images are now gone- due aSAP

**Investigator's Conclusion:** It could not see the screenshot and could not confirm a cause, but the evidence suggested the category-image move from EFS to S3 was only partly rolled out in prod: prod S3 nearly empty, no CloudFront route for `/resources/category_images/*`, and no prod copy recorded. It recommended running the copy, adding the CloudFront behavior, or rolling back.

**Actual Outcome:** The support agent first saw the images displaying on the affected sites, and within about fifteen minutes the requester said it "appears to have been fixed". No team member stated a cause or what was changed.

**Accuracy:** Partially Accurate (65%)

**Notes:** No root cause was confirmed; the hedged EFS-to-S3 migration hypothesis is plausible (a prod S3 object had been written about 20 minutes before the ticket) but unverified.

---

## 8. Ticket #86940 — Fairview MY Products update

**Investigator's Conclusion:** It could not find the "Fairview White EPVC - CMYK (First Surface)" product in the prod database. It explained the acrylic product's "Color Note" box comes from the offering's special-instructions headline and recommended setting that headline (and the job-ticket display flag) on the EPVC offering.

**Actual Outcome:** The support agent found the product was hidden, and the config team (after clarification) added the field by changing the "Color Critical - please indicate job # below" operation to "Allow User to Change This Operation". The ticket was then closed.

**Accuracy:** Inaccurate (40%)

**Notes:** The AI correctly framed it as a config change but could not locate the product and proposed a different mechanism (special-instructions headline) than the one the team used.

---

## 9. Ticket #86952 — 2086070

**Investigator's Conclusion:** It could not confirm a cause but argued the data showed no account-specific bug or server-side error. It concluded the dead Post button and reversed message order point to a front-end/browser problem, and recommended engineering reproduce it and check the console and network tab.

**Actual Outcome:** The developer could not reproduce it in staging, and support asked the requester to log out and back in to Collaterate. The requester confirmed the issue was fixed. The AI's own later comment on ticket 86970 ties these Oct 2 symptoms (reversed activity log, 403 on posting) to the server-side REST Admin Pilot role regression (TTI-24213).

**Accuracy:** Inaccurate (35%)

**Notes:** The AI concluded there was no server-side error and no account-specific problem, but the symptom was a per-user server-side role rollout (403s), fixed by re-login; its front-end guess missed that.

---

## 10. Ticket #86953 — Collerate Proof files are spinning - Widespread.

**Investigator's Conclusion:** It could not find a root cause: proof records looked normal, the instant-proof ECS service was healthy and no proof-related alarms fired. It noted a 5-hour gap in new proof records and recommended checking the proof viewer/download path and S3/CDN permissions.

**Actual Outcome:** The developer reproduced that both proof and customer print files spun on the order page, and support told the requester to log out and back in. The same fix was used for the activity-log problem reported the same morning (ticket 86952), and the ticket was resolved.

**Accuracy:** Inaccurate (30%)

**Notes:** The AI was honest that it found no cause, but its leads (S3/CDN permissions, upload gap) did not match the session-related fix; same Oct 2 REST Admin Pilot role regression cluster as 86952, 86956, 86960, 86963, 86970.

---

## 11. Ticket #86956 — unable to mark a planned shipment as shipped

**Investigator's Conclusion:** It could not find the root cause and said so. The "Save does nothing" symptom matched a known silent-failure pattern in the new Shipments UI (TTI-24155), so a rejected 4xx on the PATCH could be swallowed by the UI, but it had no evidence this was the blocker. It asked for order numbers and a DevTools network capture.

**Actual Outcome:** The requester added that the general notes section was missing and a shipment showed "site is in demo mode", though she was on the live site and everything worked earlier that morning. Support asked for cache clear and re-login; the ticket closed about two hours later with no stated resolution.

**Accuracy:** Inaccurate (40%)

**Notes:** No cause was confirmed on this ticket; it matches the Oct 2 REST Admin Pilot role cluster (all started that morning, same "demo mode" 403 symptom), which the AI did not connect here.

---

## 12. Ticket #86960 — Unable to Edit Collaterate Addresses

**Investigator's Conclusion:** It could not confirm a root cause. It judged the missing State and Zip rows in the legacy "Edit Ship To Address" dialog most likely a front-end or payload problem (country flags `hasRegions`/`hasPostalCodes` absent), since the countries table was correct. It recommended a Jira bug, a hard refresh and a support-side address correction.

**Actual Outcome:** Support asked the requester to log out and back in, which did not help. A developer then said it "should be resolved now" and asked for a cache clear, after which the requester confirmed it works. The requester had also reported a ship error.

**Accuracy:** Inaccurate (40%)

**Notes:** The AI's payload-gap guess and hard-refresh advice were in the right area but it missed the server-side rollout fix; part of the Oct 2 REST Admin Pilot cluster.

---

## 13. Ticket #86963 — Collaterate - 'Post Action' button issue

**Investigator's Conclusion:** It could not confirm a root cause, but code review showed the "Post Action" button disables itself and is only re-enabled in the server callback. It concluded the problem was most likely a client-side JavaScript error in the internal-action form and found no server-side error.

**Actual Outcome:** The requester added that the notification log was in reverse order and files were spinning. Support replied only to log out and back in, which is the fix used for all the other Oct 2 tickets.

**Accuracy:** Inaccurate (35%)

**Notes:** Nobody explicitly confirmed a cause here, but the AI's "no server-side error, client-side JS" call conflicts with the pilot-role 403s later documented in TTI-24213/24216.

---

## 14. Ticket #86967 — Text Issue - Cards in The Hub

**Investigator's Conclusion:** It could not determine the cause because the description was cut off and the screenshot was not visible, so the repeated "Application" text was unknown. It guessed duplicated option-label data and asked for a screenshot, the exact text and the product name.

**Actual Outcome:** A support agent replied about an hour and a half later that the issue was resolved and asked the requester to log out and back in. No cause or product was named and the ticket closed.

**Accuracy:** Inaccurate (30%)

**Notes:** The AI was honest about the missing information, but its data-issue guess did not match a resolution that came from a platform fix plus re-login.

---

## 15. Ticket #86970 — Collaterate not processing normal on my end.

**Investigator's Conclusion:** It identified this as very likely the known REST Admin Pilot role regression (TTI-24213): reversed activity-log order, 403s on activity-log posts and lost PP Assigned saves all fit, and it is not the user's Mac or browser. It recommended linking to TTI-24213, un-enrolling the user from the pilot role and re-login.

**Actual Outcome:** Support told the requester and her team to log out and back in, and said that would fix it. The ticket closed about 40 minutes later.

**Accuracy:** Accurate (90%)

**Notes:** The only investigator comment of the cluster that named the pilot-role rollout; the team's re-login fix is consistent with that, though no one stated the cause on the ticket.

---

## 16. Ticket #86972 — Can't log anything in Collaterate

**Investigator's Conclusion:** It could not confirm a system-wide failure, since the Activity Log was writing about 10,000 entries a day and staff and customers were posting normally. It suspected something specific to this user (account, permissions or front-end) and asked for details and a role check.

**Actual Outcome:** Support said the issue was resolved and asked her to log out and in, but she reported it still failed. Support then asked for a cache clear and a developer tested for her in test-b and found no issue. The ticket was closed on Oct 6 after an unanswered follow-up.

**Accuracy:** Partially Accurate (50%)

**Notes:** The AI correctly pointed to a per-user cause rather than an outage and flagged role/permissions; it did not tie it to the pilot-role rollout and no final confirmation appeared.

---

## 17. Ticket #86974 — Collaterate "demo mode"

**Investigator's Conclusion:** It concluded the "demo mode" message is a site-level setting and that the Crocs site was in demo mode when the user tried to ship, though the site is now live (updated 2026-09-29), so retrying should work. It admitted it could not prove the timing.

**Actual Outcome:** Support told the requester to log out and back in, saying that would fix it. No flag change or other cause was mentioned and the ticket closed within an hour.

**Accuracy:** Inaccurate (40%)

**Notes:** The "retry now" advice effectively matched the fix, but the site flag was last changed Sep 29, so the demo-mode explanation looks wrong; the same "demo mode" error appears in ticket 86956 on the same morning.

---

## 18. Ticket #86976 — Collaterate Activity Log - Order Information is backwards

**Investigator's Conclusion:** It said the most likely cause was the REST Admin Pilot rollout (TTI-24216): the REST Order Detail path shows the log oldest-first while the classic page shows newest-first, which explains why only some users see it. It recommended linking to TTI-24216, sorting newest-first, or un-enrolling the pilot batch.

**Actual Outcome:** Support replied within a minute that the issue was resolved and asked the requester to log out and back in. The ticket closed the same day.

**Accuracy:** Accurate (92%)

**Notes:** The resolution (mitigation applied, then re-login) fits the AI's pilot-role diagnosis, although support did not state the cause.

---

## 19. Ticket #86984 — Collaterate won't let me add another shipment

**Investigator's Conclusion:** It could not determine why Add Shipment from the Distribution Center failed to load, and found no matching error or bug. It judged it specific to the Distribution Center destination (configuration, data or UI code), not an outage or a browser/session problem.

**Actual Outcome:** Support replied that the issue had been resolved and asked her to log out and in. The requester confirmed it was working again.

**Accuracy:** Inaccurate (25%)

**Notes:** The AI explicitly ruled out a session problem and pointed at destination configuration, but the fix was a platform-side resolution plus re-login (the Oct 2 pilot-role cluster).

---

## 20. Ticket #86987 — Print Points Balance

**Investigator's Conclusion:** It found a 440-point gap between the storefront (-4,854) and Loyalty Admin (-4,414) and traced it to a stale PENDING -440 redemption (coupon UiR2yfd5) dated 2025-10-31, probably counted by one view and not the other. It attributed the negative balance to clawback adjustments and recommended cancelling the stale redemption.

**Actual Outcome:** A support agent's internal note reached the same conclusion, naming the same stale PENDING redemption as the entire 440 gap, and added the decisive -50,762 admin adjustment on 2026-08-27. It was assigned to the loyalty developer and still open with a follow-up on Oct 6.

**Accuracy:** Accurate (95%)

**Notes:** The team's analysis mirrors the AI's, though no adjustment or customer confirmation is recorded.

---

## 21. Ticket #86991 — Integration Issues for Job 2080195

**Investigator's Conclusion:** It found no system fault: Pace integration checks and queues were clean and the order log had no errors. It said the Part 4 and Part 10 holds kept returning because the condition behind them was not cleared, and guessed Part 17's "no preflight laser" message came from entering the path under the "file path" category instead of "preflight laser".

**Actual Outcome:** The ERP administrator triggered a resync, and Pace staff found a scheduling problem (start date later than end date on the job plans). They unscheduled and rescheduled the job, integration then succeeded, and the repeating holds were due to the same problem. The requester thanked them.

**Accuracy:** Partially Accurate (65%)

**Notes:** The AI correctly called it a Pace data/workflow condition rather than an outage and explained why the holds recurred, but it did not find the schedule-date cause and its Part 17 explanation was not confirmed.

---

## 22. Ticket #86992 — Collaterate Admin Bugs

**Investigator's Conclusion:** The symptoms (new Menus UI for only some CIMs, Users page not saving, State/Zip missing in the shipment address dialog) matched the REST Admin Pilot role incident TTI-24216. It noted the bulk role batch had already been removed in prod and recommended signing out and back in to retest.

**Actual Outcome:** Support said the issue should be resolved and asked for log out, log in and cache clear. The requester did so and confirmed everything that had been wrong was fixed.

**Accuracy:** Accurate (95%)

**Notes:** The AI's identification of the pilot rollout and its log-out/log-in recommendation matched the successful fix; it correctly flagged the Users-page link as inferred.

---

## 23. Ticket #87007 — Cannot open tickets on network.

**Investigator's Conclusion:** The 403 on the sessionless `printableWorkTicket` URL was a CloudFront/WAF block, because the requester's IP was probably not on the printables allow-list rule (`BlockPrintablesOutsideAllowedIps`). It could not confirm this because it could not read the IP set or sampled requests, and recommended checking the requester's IP and recent IP-set changes.

**Actual Outcome:** Support called it a known issue being worked with the team and asked whether the user was remote or on VPN. The user was on site on a work computer; later the team said "please try now" and the requester confirmed the tickets open again.

**Accuracy:** Accurate (85%)

**Notes:** The team did not state the cause on this ticket, but the fix timing and handling match the WAF allow-list explanation, which was confirmed as the root cause of the earlier Sept 30–Oct 1 outage on ticket 86876.

---

## 24. Ticket #87010 — Pace Tickets not opening

**Investigator's Conclusion:** The 403 was almost certainly a CloudFront WAF block, since the rule limiting the printable work-ticket URL to TBG IPs was rejecting requests. It suspected a recent IP-set change (a CloudFormation `UpdateIPSet` at 2026-10-04 23:52 UTC) and could not read the IP set or block logs to confirm.

**Actual Outcome:** Support called it a known issue and suggested the VPN, which the requester said did not apply because she was in the office. About three and a half hours later the team said "please try now" and the requester confirmed Pace tickets open again.

**Accuracy:** Accurate (85%)

**Notes:** The cause was not stated on the ticket, but it is the same incident as 87007, 87015, 87016 and 87009, and the AI's WAF/IP-set diagnosis fits.

---

## 25. Ticket #87015 — Access the job ticket through collaterate since the WSR won't launch the ticket

**Investigator's Conclusion:** It could not determine why the WSR (Work Station Report) would not launch the job ticket and had no root cause; its searches turned up nothing on "WSR". It suggested opening the ticket directly in Collaterate as a workaround, getting a screenshot and testing on VPN.

**Actual Outcome:** Support called it a known issue, got a screenshot over chat, and later said it was resolved and to try again, then closed the ticket. This was the same Oct 5 work-ticket 403 incident as 87007, 87010 and 87016.

**Accuracy:** Inaccurate (30%)

**Notes:** The AI gave no diagnosis and did not link this to the other same-morning 403 tickets, although its Collaterate-lookup workaround was valid.

---

## 26. Ticket #87009 — printing icon not working , not responding

**Investigator's Conclusion:** It could not find a root cause. Pace logs showed no print errors, so it judged the problem most likely on the workstation, printer or Producer client side, and recommended testing on the affected PC and checking for a common cause such as a driver or PDF viewer change.

**Actual Outcome:** Support said it was a known issue the team was working on, and later told the requester to try again. The requester confirmed printing worked, with no workstation change reported.

**Accuracy:** Inaccurate (25%)

**Notes:** The fix was server-side (same Oct 5 printable-page block as 87007, 87010 and 87016), so the AI's workstation/printer theory was wrong.

---

## 27. Ticket #87021 — unable to print out of collaterate

**Investigator's Conclusion:** The "error finding your label printer" message is raised in the browser when it cannot reach the local Zebra Browser Print agent or find a default Zebra printer. It said this is a workstation problem and not a Collaterate server fault, and gave steps to check the agent and printer.

**Actual Outcome:** The requester wrote that it started printing again on its own ("disregard") but that this seems to be happening a lot lately, then agreed to close the ticket. No cause was identified by the team.

**Accuracy:** Partially Accurate (70%)

**Notes:** Nobody confirmed a cause; the AI's code-based explanation of what triggers that exact message is sound, and the intermittent self-recovery is consistent with a local agent issue.

---

## 28. Ticket #87038 — Toolkit Inventory adjustment

**Investigator's Conclusion:** It could not find SKU 101873753-0001 (product P2036425) in any database it could query, so it could not confirm why Available showed -34 against 52 inventory. It suggested stale or over-reserved quantities and recommended checking the ledger and releasing stale reservations.

**Actual Outcome:** Support found 37 backorders on the SKU and about 51 actual inventory. The requester then said he had worked with the inventory team, the numbers add up now, nothing needs adjusting, and closed the ticket.

**Accuracy:** Inaccurate (45%)

**Notes:** The AI never located the record, and its stale-reservation guess missed that backorders drove the negative Available.

---

## 29. Ticket #87016 — Can't access work tickets through pace

**Investigator's Conclusion:** The likely cause was the WAF/CloudFront printables IP allow-list added as a compensating control for a security issue (TTI-23044 / TTI-23060), blocking work-ticket URLs for users whose IP is not allow-listed. It noted Pace backend errors were zero, so the 403 was returned at the edge, and warned that the helpdesk "resolved" note had no verified fix behind it.

**Actual Outcome:** Support first called it a known issue, then said it was resolved and to try now, and closed the ticket about 20 minutes later. The team did not say what was changed.

**Accuracy:** Accurate (85%)

**Notes:** The cause was never stated on the ticket, but it is the same Oct 5 incident as 87007 and 87010; the AI's edge-block conclusion fits and it correctly questioned the unverified closure.

---

## 30. Ticket #87049 — Remove Product Type: "TBG Dye Sub Monti" from the HUB- Christi Chapin

**Investigator's Conclusion:** It could not find a "TBG Dye Sub Monti" product type in Collaterate or Redshift, and concluded the HUB product type list is a Pace setting that a Pace admin must remove. It added that nothing in Collaterate needed changing, and suggested deactivating rather than deleting.

**Actual Outcome:** The configuration team replied a week later that the product had been retired and hidden from The Hub, and the ticket closed.

**Accuracy:** Inaccurate (40%)

**Notes:** The right action (retire rather than delete) matched, but the AI could not find the product and wrongly said the change belonged in Pace rather than Collaterate/Hub configuration.

---

## 31. Ticket #87056 — LIFEWISE Skus showing incorrect backorders

**Investigator's Conclusion:** The two order lines (jobs 4680773 and 4718021) were still flagged backordered although stock now existed, because `order_items.stock_backorder_quantity` is a snapshot taken at order time that the WMS inventory sync never clears on open items. It recommended resetting both lines to 0, reconciling the SKU-level backorder count of 1, and checking other Lifewise lines.

**Actual Outcome:** Support asked a developer to remove the backorder status on the two orders. The developer ran an inventory drift update for the site (9 products had drift) and noted a Java bug that could have caused it was being worked on. The requester thanked them.

**Accuracy:** Accurate (88%)

**Notes:** The drift update confirms the AI's "stale backorder not reconciled after replenishment" finding, and the developer's mention of a known bug is consistent with its call for a sync fix.

---

## 32. Ticket #87076 — Matching Envelope operation items share cost tables with envelope press sheets

**Investigator's Conclusion:** The database matched the ticket: three active items and three inactive ones (47/48/49) in operation 9 share cost tables with press sheets. It also found six additional inactive items sharing tables and proposed a transactional script giving each operation item its own cost-table copy, leaving the press sheets untouched.

**Actual Outcome:** The developer created separate cost tables for each item in staging, the requester verified it, and the change was then applied in prod. The developer reported that 14 cost tables shared with press sheets were now split.

**Accuracy:** Accurate (97%)

**Notes:** The fix the team applied was the approach the AI recommended, and its extra findings align with the broader count of 14 tables.

---

## 33. Ticket #87091 — Unable to log into Collaterate - New Hire Mark Kadadah

**Investigator's Conclusion:** It found no Collaterate account for Mark Kadadah in prod and concluded he could not log in because his account was never created. It recommended confirming the name spelling, creating the user if missing, and checking onboarding provisioning.

**Actual Outcome:** Support asked the requester to try again, then after the new hire still failed to log in a support agent supplied the default password and confirmed they could log in that morning. The ticket was then resolved without stating whether an account had been created.

**Accuracy:** Partially Accurate (75%)

**Notes:** The reply with a default password and "I was able to log in" implies an account was created or fixed after the AI's check, which fits its "account missing" conclusion, but the team never said so explicitly.

---

## 34. Ticket #87093 — Invitations and Cards - misleading header

**Investigator's Conclusion:** It could not find where the "Mailing" heading comes from and saw it as a copy/label change request. It inferred from a knowledge-base prompt that the section is probably the matching-envelope option group, said the prod DB had no matching option-group table, and recommended re-filing as a Jira request.

**Actual Outcome:** A developer found the label comes from the `operation_groups` table (id 30, "SF Smartpress Mailing", label "Mailing") created by a 4.44 migration. The same group holds both envelope and real mailing operations, so a simple rename would affect other products and separate groups were recommended. Support later reported it resolved.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI's inference that the section is the envelope option group was right and its rename-to-"Envelopes" suggestion was close, but it claimed no matching DB table exists and missed the shared-group complication.

---

## 35. Ticket #87098 — HUB Tape Application Selection (Finishing) - Christi Chapin

**Investigator's Conclusion:** This is a product-configuration request, not an outage. It located the PM Ordering Portal tape-application operations (e.g. "LF Film Tape Application" operations 176–178), pointed to earlier tape changes (TEM-3854, TTI-16704) as models, and recommended reclassifying it as a service request and confirming PID 33157 exists in Pace.

**Actual Outcome:** Support forwarded the ticket to the configuration lead and left it open (status Open) as of the last update. No outcome or resolution was recorded.

**Accuracy:** Partially Accurate (70%)

**Notes:** Nobody confirmed anything, so this rates the analysis only: the classification as a config request routed to the right team is sound, but how a tape PID links to the operations was unconfirmed.

---

## 36. Ticket #87100 — 2087628 - Locatoin unable to update

**Investigator's Conclusion:** It could not find why the location change fails for jobs 4730902 and 4730905, found no errors for either job and could not read their state. It noted an unrelated message in the UpdateJobLocation dead-letter queue and said a Pace or Collaterate developer needed to review.

**Actual Outcome:** The team reproduced it in staging and a developer showed it is by design: a job in Large Format Distro (group id 9) cannot be moved to any other production group, a rule from TTI-347 in 2021. The requester said the products were quoted incorrectly, a new quote was requested, and the ticket could be closed.

**Accuracy:** Inaccurate (15%)

**Notes:** The AI gave no diagnosis and its DLQ finding was a red herring; the real explanation was a coded business rule it did not find.

---

## 37. Ticket #87111 — 2087660 un-cancel job

**Investigator's Conclusion:** Job 4730970 is cancelled and the order is already Shipped (changed by the requester minutes earlier). It could not see the exact error but judged the app does not appear to allow un-cancelling a job on a shipped order, so it probably needed a developer or DBA to fix the data.

**Actual Outcome:** A support agent reproduced it in staging and confirmed the order being in Shipped status is why the un-cancel fails. Changing the order back to an active status let the item be un-cancelled, and the requester was told to do that.

**Accuracy:** Partially Accurate (80%)

**Notes:** The AI identified the Shipped-status blocker but overreached in suggesting a data fix when reverting the order status was enough.

---

## 38. Ticket #87129 — Errors for new shipments/partial credits

**Investigator's Conclusion:** Its first comment could not identify the cause of the add-shipment, un-cancel and partial-credit errors; transaction, shipment creation and Pace looked healthy and the exception was only in application logs. A later AI comment gave the root cause: the REST Admin Pilot role added to 138 admins on 2026-10-06, whose credit endpoint needs a permission most PCs lack (403) and whose shipment endpoint rejects a facility already on the order. The pilot was switched off and a permanent fix (TTI-24321) raised.

**Actual Outcome:** Support could not reproduce it in staging, then noted the requester lacked the Accounting permission. The requester later said a developer had identified and corrected the issue, and support closed the ticket the same day.

**Accuracy:** Accurate (88%)

**Notes:** The later root-cause comment matches the team's fix (turning off the pilot); the first comment alone had no diagnosis. Same Oct 6 pilot regression as the Oct 2 cluster.

---

## 39. Ticket #87144 — Can't log into Jitbit, password reset link expired/already used

**Investigator's Conclusion:** It could not confirm a cause with its tools. It suggested an email security scanner opening the single-use reset link first, an older-token mix-up or a username typo, and recommended a Jitbit admin check the account and set a temporary password.

**Actual Outcome:** A Jitbit administrator said they fixed the login and the requester confirmed it worked; the ticket closed the same day. No cause was stated.

**Accuracy:** Partially Accurate (60%)

**Notes:** The recommended admin-side account fix was what resolved it, but the scanner theory was never confirmed.

---

## 40. Ticket #87147 — Braille Hot folder update

**Investigator's Conclusion:** The facility-number size is not a hot-folder setting but a hard-coded constant, `ROOM_NUM_FONT_SIZE = 29.3`, in the `mhealthBrailleSetup` handler in `pa-webhook-workers`. It needs a code change to 24 and a deploy, and it should be routed to development.

**Actual Outcome:** The configuration team agreed, noting that "based on the AI investigator" it is not config related, and handed it to a developer. The ticket remains open and is marked deleted in Freshservice, with no fix recorded.

**Accuracy:** Accurate (85%)

**Notes:** The team routed the ticket on the AI's finding; the fix itself was not confirmed.

---

## 41. Ticket #87155 — Custom Quote Items Missing

**Investigator's Conclusion:** Its first comment found two of the quote's three jobs gone from the database and could not say what removed them. A second AI comment, posted with engineering help, found the root cause: a bug let the custom quote's project appear as the customer's shopping cart, so the customer's "Remove" clicks on 2026-09-29 permanently deleted 7 jobs.

**Actual Outcome:** Support told the sales rep this was a system bug, the quote had to be re-created, and a fix was going out the following Wednesday; other quotes were found to be affected. The ticket was closed on Oct 29 with "the issue has been fixed".

**Accuracy:** Accurate (95%)

**Notes:** The team's explanation (a system bug, fix pending) matches the second comment's root cause; the first comment alone had no diagnosis.

---

## 42. Ticket #87175 — Lifewise Order 2069816 - cannot cancel part?

**Investigator's Conclusion:** It could not identify the cancel error but found job 4680773 still carried a stale backorder quantity set at order intake, while the SKU's backorder had since been recalculated, and a replacement job existed. It tied the stale flag to the failure to cancel.

**Actual Outcome:** Support reproduced it in staging and a developer explained the cancel fails because it tries to release a backorder that no longer exists on the variant after the drift update. The configuration developer ran SQL to clear the stale `stock_backorder_quantity`, and support asked the requester to try again.

**Accuracy:** Accurate (88%)

**Notes:** The AI's stale-backorder finding is exactly what the developers fixed; it did not name the release-of-missing-backorder mechanism.

---

## 43. Ticket #87164 — Meta user unable to checkout - PR is the country

**Investigator's Conclusion:** The saved address had postal code 987 instead of 00987, so FedEx returned no valid shipping service and the checkout showed "Selected an incorrect shipping service". It said the blank State field is not the cause for Puerto Rico but can block saving the address in stage, and recommended correcting the ZIP and making State optional for PR.

**Actual Outcome:** Support had already identified the ZIP issue and asked for 00987; the requester corrected the address, noted checkout still asked for a state, and asked to close the ticket.

**Accuracy:** Accurate (95%)

**Notes:** The AI comment arrived after support had reached the same answer, and its observation about the lingering State requirement matched the requester's last comment.

---

## 44. Ticket #87194 — Trouble with aText blurbs in Collaterate

**Investigator's Conclusion:** It found no server-side cause and hypothesised a client-side conflict between the aText app and the Collaterate browser windows (lost accessibility permission, a rich-text field swallowing keystrokes, or the expansion mode). It recommended checking the user's Mac and the field affected.

**Actual Outcome:** IT confirmed aText was installed and permissioned correctly and the failures were in the proof status and comments windows after prod release 4.45.2. Developers reproduced it on a Mac with aText but not on Windows, and told the requester it is not a Collaterate issue and happens only with aText on Mac. On Oct 15, however, a linked Jira on the proof-status area was put on hold because the planned new AOD page would cover it.

**Accuracy:** Partially Accurate (60%)

**Notes:** The client-side aText theory matches the Mac-only reproduction, but the linked Jira suggests the Collaterate window is also involved, and IT first suspected a Collaterate change.

---

## 45. Ticket #87210 — Not able to upload screenshot to customer account's

**Investigator's Conclusion:** It could not determine the cause because the ticket lacked the error text and location; the account looked normal and no logs matched. It guessed an unsupported file type or oversize file, based on an unrelated Instant Proof error, and asked for the error and file details.

**Actual Outcome:** Support could not reproduce the upload in prod, but in staging reproduced the error and found it went away once the "User & Division Manager" administrator permission was added to the requester. The requester then confirmed "Now it works!" on Oct 8.

**Accuracy:** Inaccurate (25%)

**Notes:** The cause was a permission, not file type; the AI's file-type guess was explicitly speculative and wrong, and it did not suggest checking the requester's role.

---

## 46. Ticket #87154 — CoreMedia- client not getting emails

**Investigator's Conclusion:** It could not confirm why the user was not receiving CoreMedia (DALIM ES) emails, since the cause sits inside that application. It agreed with routing to the CoreMedia owner and recommended checking the DALIM outgoing mail log and, if messages were sent, the client's spam filter.

**Actual Outcome:** The CoreMedia owner found ES was handing mail to the TBG mail server correctly but TBG's server was not delivering mail from the @smartpress.com sender, and proposed changing the sender. The requester then reported the client found the problem on Fairview's own end, and the ticket closed.

**Accuracy:** Partially Accurate (60%)

**Notes:** The AI's "if sent, check the client's spam filter" branch matched the final cause, but its analysis contained no diagnosis and the sender-domain issue was found by a human.

---

## 47. Ticket #87237 — Can't see some internal order notes

**Investigator's Conclusion:** It said this did not look like a permissions problem and the more likely cause was that the requester and her teammate were on different order screens, since only the requester had the REST Admin Pilot role (new `sls-admin-order-details` screen). It could not confirm which note was meant and recommended opening the classic view.

**Actual Outcome:** Support checked and found the teammate also had the REST Admin Pilot role, contradicting the AI's premise, and could see the notes when logged in as the requester. The requester then restarted her computer, could see the notes, and confirmed.

**Accuracy:** Inaccurate (35%)

**Notes:** The AI correctly ruled out permissions, but its different-screens theory was disproved and the real fix was a client-side restart.

---

## 48. Ticket #87239 — Override is not available in collaterate today - I cannot plan jobs

**Investigator's Conclusion:** It could not reproduce the missing Override but said the best lead was the requester being on the REST Admin Pilot version of Order Detail, which has known gaps, and recommended removing the user from the pilot role or toggling the feature flag.

**Actual Outcome:** Support confirmed the requester held the REST Admin Pilot role, then logged in as her and saw the Override. The requester said it was working again and asked to close the ticket; no cause was stated.

**Accuracy:** Partially Accurate (75%)

**Notes:** The pilot-role lead was confirmed (the user held the role), but no one confirmed it was the cause of the missing Override.

---

## 49. Ticket #87244 — Re: Collaterate Dev Request - Layout Adjustment - Save and Cancel Buttons Covered by Notification/Error Bar

**Investigator's Conclusion:** It said no technical investigation was needed because the ticket was only a "Looks good, thank you!" confirmation reply to an earlier dev request. It recommended closing it and linking it to the original request.

**Actual Outcome:** Support replied that it was a response to ticket 86675 and closed the ticket.

**Accuracy:** Accurate (97%)

**Notes:** The AI did not find the original ticket number but the handling matched its recommendation exactly.

---

## 50. Ticket #87261 — Shipping cost accurate?

**Investigator's Conclusion:** The $33.73 FedEx Home Delivery rate looked consistent with how Collaterate priced earlier shipments to the same rural Maine ZIP ($33.01–$33.12) and showed no calculation error. It suggested counter pickup as an alternative and that any dispute over the markup is a rate-adjustment setting, not a bug.

**Actual Outcome:** Support reviewed prior orders and found shipments to that ZIP consistently charged $33.12 or $33.01, and the requester accepted the answer and asked to close the ticket.

**Accuracy:** Accurate (97%)

**Notes:** Support's finding matched the AI's price comparison.

---

## 51. Ticket #87286 — Issue with color on reorder being changed to Black ink only

**Investigator's Conclusion:** The reorder picked up a new "Matching Envelope Printing Ink Type" operation (created Dec 2025) that the original 2024 order never had, and it defaulted that operation to the first item, "Black Only". It saw this as a data and default-value problem rather than an outage, inferred from comparing the two jobs' operations.

**Actual Outcome:** Support first could not reproduce it, then reproduced it in prod and stage. A developer confirmed the AI investigation was correct and the configuration team set "Full Color" as the default for that operation on the Cards PJC. Support also gave a manual workaround for the pending job.

**Accuracy:** Accurate (95%)

**Notes:** The fix, changing the operation's default, is exactly what the AI's analysis pointed to.

---

## 52. Ticket #87289 — Split shipment not available in activity log? Order 2089844

**Investigator's Conclusion:** The second shipment was added manually on 2026-10-07 10:33 UTC by a named user, not created by the Sephora import, and nothing was written to the activity log when it was created, which is why the requester could not see it there.

**Actual Outcome:** Support relayed the AI finding, and a developer confirmed from the code that neither the classic admin shipping screen nor the newer shipment API writes an activity-log entry when a shipment is added. The requester said that told her what she needed and the ticket could close.

**Accuracy:** Accurate (95%)

**Notes:** Code review matched the AI's data-based conclusion.

---

## 53. Ticket #87294 — Character Limit for "I Will Describe Delivery Method" Shipping?

**Investigator's Conclusion:** No 64-character limit exists today: the text lands in `order_shipments.shipping_service_notes`, a `text` column, with no validation, and about 10% of recent shipments (1,663 of 17,053) exceed 64 characters. It recommended a TTI ticket adding both UI maxlength and server-side validation.

**Actual Outcome:** A developer proposed exactly that UI plus server-side limit with no database change. After clarification from the requester and the warehouse team, they confirmed they would enforce 64 characters on all sites and leave existing orders unchanged.

**Accuracy:** Accurate (95%)

**Notes:** The ticket remained open for the implementation, but the agreed approach matches the AI's recommendation.

---

## 54. Ticket #87326 — Producer PID 22782 needed

**Investigator's Conclusion:** It could not find a cause. PID 22782 is active in Pace with stock on hand and not in the Collaterate material specification table, so it was likely excluded from the New Gang picker because it is sheet stock while the picker offers roll stock. It said this was unconfirmed and a dev should check how the picker builds the material list.

**Actual Outcome:** The configuration team lead replied the same day that the requester was "all set" and the requester confirmed the PID is now there. The fix was not described.

**Accuracy:** Partially Accurate (55%)

**Notes:** The outcome shows a configuration change, which fits the AI's pointer to product material mapping, but the sheet-versus-roll theory was not verified.

---

## 55. Ticket #87315 — Storefront closing out and shipping jobs

**Investigator's Conclusion:** It did not find the root cause and could not verify the line-item statuses. It found that the manual per-line "Ship" action sends an email by design (`sendNotificationEmail` is hardcoded true), so the duplicate emails are expected, and suggested developers check whether shipping the job still cascades "Shipped" to line items.

**Actual Outcome:** Support found the example order was a BOM Builder order and linked it to ticket 86869 (hidden sub-jobs preventing shipped status). It was passed to the developers; by Oct 23 a list of non-shippable orders had been produced for review, the requester confirmed the KOHLER Professional Channel shipments on it could be shipped, and the lines were being marked shipped manually while developers explored longer-term improvements. The ticket was still open.

**Accuracy:** Inaccurate (40%)

**Notes:** Nobody confirmed the cause; the AI's by-design email finding looks valid but it missed that this is a BOM Builder / hidden-sub-job order like 86869.

---

## 56. Ticket #87334 — Fix for current printing

**Investigator's Conclusion:** Collaterate already had job 4741628 set to 2-sided, but the edit was made after the job went to production, so D2P likely still carried the original single-sided setup. It recommended re-triggering the job update to Pace/D2P and re-releasing the job.

**Actual Outcome:** A developer reached the same conclusion: the job changed to 2-sided at 8:14 AM CT but the print file had been requested at 7:08 AM CT, and production was told to re-request the print file. On Oct 15 support added that D2P's default retry had used the stale notification, a fresh print-file request would pull current data, and a Jitbit ticket should be raised if it recurs. The reporter said a new D2P error appeared on Oct 13, and no final confirmation was recorded.

**Accuracy:** Accurate (88%)

**Notes:** The diagnosis matched; the follow-up D2P error afterward was a separate unresolved problem.

---

## 57. Ticket #87336 — Sticker Pricing on Smartpress Website Down

**Investigator's Conclusion:** It could not determine why Instant Quote was unavailable on Custom Die-Cut Stickers and found no outage or error. Its strongest lead was that the product had been updated about 18 hours earlier by a named e-commerce user, so it recommended asking them what changed and checking pricing inputs.

**Actual Outcome:** Support reproduced a "pricing engine could not be reached" error and passed the AI's suggestion to the e-commerce team member. Support said it was resolved about 40 minutes after the ticket opened and the requester thanked them; the fix was not described.

**Accuracy:** Partially Accurate (65%)

**Notes:** The AI's change-on-Oct-8 lead was the one the team acted on, but the actual cause and fix were never recorded.

---

## 58. Ticket #87340 — Collaterate notifications

**Investigator's Conclusion:** The requester already has access to Collaterate Notifications and it found no permission gap. It guessed she wanted to see her teammates' notifications and said no role setting for notifications was found.

**Actual Outcome:** Support tested in staging and found the Notifications view only worked after the "Internal Notifications" role was added. The configuration team added that role in prod.

**Accuracy:** Inaccurate (15%)

**Notes:** The AI explicitly concluded there was no permission gap and that no permission table controls notifications, when a missing role was the whole problem.

---

## 59. Ticket #87350 — 2027 Saddle Stitch Calendar IDML Layout Guides Need Adjustment

**Investigator's Conclusion:** The 2027 IDML files were present in S3 and look intact, but were uploaded without a Content-Type, which would make a browser treat them as unknown files. It recommended re-uploading the seven files with Content-Type `application/octet-stream`, and said it could not check the layout guides.

**Actual Outcome:** Support suggested a Safari download setting or Chrome, and the requester could not open an IDML to check. A support agent noted the 2027 Layout Guide URL points to an `.idml` file and that changing it to `.pdf` opened the file. On Oct 13 the requester reported the customer said the initial browser troubleshooting had resolved the problems, and the ticket closed.

**Accuracy:** Partially Accurate (55%)

**Notes:** The browser-handling-of-an-unrecognized-file theory is consistent with the browser troubleshooting that fixed it, but the Content-Type cause was never confirmed.

---

## 60. Ticket #87343 — Re: Turn off PID 8311

**Investigator's Conclusion:** No investigation was needed: the ticket is just an email reply ("Thanks all!") to the "Turn off PID 8311" thread, with no incident or request. It recommended closing it as a follow-up to ticket 87245 and handling any remaining work there.

**Actual Outcome:** Support noted before the AI comment that it is a response to ticket 87245 and closed it.

**Accuracy:** Accurate (97%)

**Notes:** The AI comment was posted after the closing note and repeated the same conclusion, adding stock-flag details from the thread.

---

## 61. Ticket #87374 — Auto-follow PM Outsourcing

**Investigator's Conclusion:** This is a feature request, not an incident: the behaviour does not exist, and it can be added in the order-created handler (`event-handler-order-created.js` in `sls-event-handler`) by inserting active `order_item_followers` rows after the PC is assigned. It suggested a per-assignment-group flag and noted orders that already have a CSR are skipped.

**Actual Outcome:** Support delivered a checkbox for each PC Assignment Group in the Event Handler app, "Auto-follow matching jobs", disabled by default. The requester thanked them and the ticket was closed on Oct 29.

**Accuracy:** Accurate (97%)

**Notes:** The shipped design is the per-group flag the AI recommended.

---

## 62. Ticket #87376 — CQ history: when copying, add item to history in both quotes

**Investigator's Conclusion:** This is a feature request. `CustomQuotesRepository.createQuote` writes the "Duplicate Quote" history entry only into the new quote, and the fix is to load the source quote after duplicating and append a matching entry to it, with a test and a TTI story.

**Actual Outcome:** Support reproduced it in staging, then a developer made a quick fix the same day so the original quote's history shows the number of the quote it was duplicated into. The ticket was closed.

**Accuracy:** Accurate (95%)

**Notes:** The change made is the one the AI described.

---

## 63. Ticket #87378 — Delta Print Portal SKU 101899829-0001 adjustment

**Investigator's Conclusion:** Actual (33) already matched, but Reserved was 0 (expected 2) and Backordered was 8 (expected 0), after a warehouse pick event and a "true up" earlier that day. It recommended a developer correct the variant to reserved 2, backordered 0, with an adjustment row for audit.

**Actual Outcome:** Support adjusted the inventory and posted a screenshot, and the requester thanked them. The ticket closed within about ten minutes.

**Accuracy:** Accurate (95%)

**Notes:** The expected final values the AI stated match what was set.

---

## 64. Ticket #87387 — add a sales rep filter to the PC queue

**Investigator's Conclusion:** This is a feature request, not an incident. The PC queue (`sls-pc-queue`) has no sales-rep field or filter, there is no existing Jira work, and it recommended a TTI story covering the queue payload, filter parameter and UI control.

**Actual Outcome:** Support confirmed only the PC filter exists in the queue, and the requester supplied the queue link. The ticket is still open with no delivery recorded.

**Accuracy:** Accurate (85%)

**Notes:** Nothing contradicted the AI's finding and no fix was confirmed.

---

## 65. Ticket #87383 — Facebook Pixel

**Investigator's Conclusion:** It could not determine why the Facebook catalog shows only 4 products. It found the theme sends only a hard-coded Purchase event without product IDs and said the cause may be missing or mismatched `content_ids`, with the Pixel and catalog settings sitting in Meta and GTM that it could not read.

**Actual Outcome:** Engineering fixed the pixel on Oct 15 so it sends product IDs in the format Meta's catalog expects. The catalog still held few products because Meta's catalog crawler was being blocked by site security, which engineers asked to allow; the requester accepted the update and the ticket stayed open.

**Accuracy:** Partially Accurate (65%)

**Notes:** The ID-format theory matched the first fix, but the AI missed the crawler block that kept the catalog small.

---

## 66. Ticket #87399 — Collaterate JitBit access issues

**Investigator's Conclusion:** It could not confirm the cause because its tools cannot see JitBit. It thought the one-time reset links were most likely being consumed by an email security scanner, and listed an inactive or locked account as another possibility, recommending a JitBit admin check the account.

**Actual Outcome:** The JitBit administrator explained that a licensing change to per-technician fees deactivated accounts that had not been used recently. They reactivated her account as a standard user, and she logged in and filed a ticket.

**Accuracy:** Partially Accurate (50%)

**Notes:** The AI's top theory (link scanner) was wrong, but its recommendation to have an admin check the account's active status found the real cause.

---

## 67. Ticket #87408 — No front lam required for Printed Summa cut jobs - UV Roll Product Type - Christi Chapin

**Investigator's Conclusion:** It could not make the change or tell which Hub product the ticket meant. It showed front laminate is controlled per print job classification (`show_front_laminate`) and listed the UV Roll and Summa classifications that currently show it, recommending the configuration owner turn it off for the correct one.

**Actual Outcome:** The configuration lead is assigned but no reply or resolution was posted; the ticket remains open.

**Accuracy:** Partially Accurate (70%)

**Notes:** Nobody confirmed anything, so the rating reflects the analysis: the mechanism is correct and Hub-config-based, but the specific classification was not identified.

---

## 68. Ticket #87424 — Collaterate Log Out Issue

**Investigator's Conclusion:** It could not confirm the cause. It found the same @smartpress.com address exists as both a staff login and storefront customer accounts, a plausible source of session conflicts during assisted sales, and said it had no evidence of any domain-based logout logic.

**Actual Outcome:** A developer found the reporter's @smartpress.com email was attached to other Smartpress customer accounts and that her staff username used that domain instead of the usual TBG address, and logs showed her session being destroyed. The email was removed from the other accounts and the ticket was kept open to watch for recurrence.

**Accuracy:** Partially Accurate (80%)

**Notes:** The AI's hypothesis of an email shared between staff and customer records matched what the team found, though whether it fully fixed the logouts was not yet confirmed.

---

## 69. Ticket #87428 — Lifewise sku 100778143-0001 adjustment

**Investigator's Conclusion:** The variant showed Actual 14, Reserved 14 and Backordered 14, and the 14 backordered units came from one of two items on order 2089801 flagged backordered even though stock was on hand. It recommended zeroing the variant backorder and correcting the order item.

**Actual Outcome:** A developer adjusted the backorder on the product page, and the configuration developer made the order-level correction. The requester then realised the customer had put 28 of the same part on the order across two jobs, so one job (4735596) was cancelled and the SKU adjusted.

**Accuracy:** Partially Accurate (60%)

**Notes:** The data fix the AI described was what was done, but it treated the backorder as a false flag when it came from duplicate quantities on the order.

---

## 70. Ticket #87446 — Jitbit #105187021

**Investigator's Conclusion:** It could not identify the order or the cause. The ticket named no order and the cited Jitbit tickets were unreachable, so it asked for the order number, page and error text.

**Actual Outcome:** The requester explained that new Jitbit alerts keep saying the proof file has the wrong number of pages although it matches the Collaterate ticket, and tied it to ticket 87334 (the D2P stale-data issue). The ticket was still open at the last update.

**Accuracy:** Inaccurate (25%)

**Notes:** The AI offered no diagnosis and did not connect the alert to the same-week D2P/print-file request issue in 87334.

---

## 71. Ticket #87454 — Assisted Sale - Order Placed Notification, No Order

**Investigator's Conclusion:** Inconclusive: the ticket did not identify the custom quote, so it could not trace it. It found no errors in the quote-update Lambda, said a silent missed status update was possible, and noted the custom-quotes service had been deployed the day before (PRs #156 and #158) as an unreviewed timing coincidence.

**Actual Outcome:** The developer found a race condition: the customer ordered from a stale quote page while the admin had the quote in Requote and clicked "Submit to Customer" two seconds later, which overwrote the Ordered status without checking. The developer corrected the quote's data (Ordered and linked to the order) and planned two guards; the ticket closed on Oct 29.

**Accuracy:** Inaccurate (30%)

**Notes:** The AI's suspected missed status update was a symptom, but it offered no cause and its deploy-timing lead was not the cause. Its manual-fix workaround matched the data fix applied.

---

## 72. Ticket #87478 — Sephora 2.0 ID 27032-UBF not triggering backorder

**Investigator's Conclusion:** The backorder was not being persisted: the variant's counters were stuck at 0 even though 46 open items for 47 units existed, and the variant was last updated by `anonymous` eight seconds after the new job was created. It judged this a defect or data drift, recommended running the inventory reconciliation script and avoiding cancel-and-re-add.

**Actual Outcome:** Support adjusted the backorder to 1, but re-adding the job did not trigger it, so the configuration developer made a further fix ("all set"). The job then showed as Backordered and the requester confirmed.

**Accuracy:** Partially Accurate (75%)

**Notes:** The counter-drift finding was borne out by the manual adjustments needed, though the AI's suggested root cause (the sync resetting values) and the reconciliation script were not confirmed.

---

## 73. Ticket #87489 — Collaterate order total calculating incorrectly 2091274

**Investigator's Conclusion:** The line items correctly sum to $7,231.74, but the order header holds an older $6,870.15, which is what is charged. It said the header was probably not recalculated after the 10/14 job-price edits and admitted it could not explain exactly how the header reached $6,870.15.

**Actual Outcome:** Support first blamed a Requote bug, then retracted that. The final finding was that Requote works as designed (it only flags a price adjustment), the jobs are priced correctly, and the header was lower because the 5% Nonprofit discount was applied a second time at checkout on 10/07, a custom-quote handling bug partly fixed on 10/14.

**Accuracy:** Inaccurate (30%)

**Notes:** The AI's observation of the $361.59 header gap was accurate, but its stale-header explanation was wrong; the double-applied discount was the cause.

---

## 74. Ticket #87524 — Unable to adjust shipping speed

**Investigator's Conclusion:** It could not find the cause. The order data showed her teammate Karl's change from Direct Mail Services to FedEx Home Delivery succeeded, and nothing pointed to a problem with the order. It recommended comparing the two users' roles, capturing the network response and escalating if it recurs.

**Actual Outcome:** Support compared roles and tried it in staging with her credentials, where the change worked. The requester noted her screen showed FedEx Ground instead of Home Delivery, and support confirmed the Home Delivery option was not visible for her. The ticket was closed the same day without a stated cause.

**Accuracy:** Inaccurate (45%)

**Notes:** The AI's user-specific lead was right and the role comparison it proposed was done, but it gave no cause; this lines up with the Oct 15 REST Admin Pilot screen gaps (see 87541, 87556, 87562).

---

## 75. Ticket #87432 — Logic needed for Interchangeable Retractable Banners (New SPDC Product)

**Investigator's Conclusion:** The operation and choice IDs in the request are valid (operation 10 is Banner Stands; operation 122 is TBG Velcro Application, choice 4329). It agreed with earlier triage that this needs a developer-configured logic rule because the system has no cross-operation rule engine, and suggested splitting the product into two variants as a workaround.

**Actual Outcome:** Support's first reply called it a feature request, then a developer posted that the logic was now up on Prod. The ticket closed on Oct 29.

**Accuracy:** Accurate (85%)

**Notes:** The AI's feature-request classification and ID validation were consistent with the outcome; the method used to implement it was not recorded.

---

## 76. Ticket #87536 — Printing Collaterate packing slips now have blank page

**Investigator's Conclusion:** After two earlier comments (a returns-QR block theory that it then retracted), its final comment found the root cause: the packing slip page forces a page break after the slip and the admin layout then adds an empty footer `div`, so Chrome prints a blank second page on every slip. It named the fix (TTI-24713) and a print-dialog workaround.

**Actual Outcome:** A developer confirmed the fix under TTI-24713 for hotfix 4.46.1, support gave the workaround, and the fix went live in prod on Oct 15 with the blank page gone.

**Accuracy:** Accurate (88%)

**Notes:** The final AI root cause matched the shipped fix, but the first comment blamed the wrong feature and needed two corrections.

---

## 77. Ticket #87541 — Can't Override/Change Descriptions in Collaterate

**Investigator's Conclusion:** It could not confirm the root cause. The backend save code for site-share descriptions looked correct, so the fault was probably in the UI request or how a blank description is persisted. It suggested capturing the network call and entering a space as a workaround.

**Actual Outcome:** Support found the problem disappeared in staging when the REST Admin role was removed from the user, and a developer fixed it in release 4.46.1, which went live the same day.

**Accuracy:** Partially Accurate (50%)

**Notes:** The AI pointed at the UI request rather than backend code, which fits a REST-pilot-screen defect, but it did not identify the pilot role.

---

## 78. Ticket #87556 — Error occurred. Contact support for help if the problem persists

**Investigator's Conclusion:** It could not find the cause: the logs and Sentry showed nothing. It noted two of the four orders were already In Process and the others were in different states, and asked for the exact action, time and username.

**Actual Outcome:** The requester said the error appears on "Ship It". A developer explained the REST pilot screen was hiding the real refusal reasons (insufficient inventory on 2088513, a FedEx "Shipper Postal-State Mismatch" on 2089015), fixed in hotfix 4.46.1. Support later gave the backorder-split instruction for 2088513 and closed the ticket.

**Accuracy:** Inaccurate (30%)

**Notes:** The AI's observation that two orders were already In Process was right, but it missed the pilot-screen error masking and the individual shipment refusals.

---

## 79. Ticket #87560 — Custom Quote - Cards Dimensions Issue

**Investigator's Conclusion:** It could not confirm the root cause but concluded custom quote products should not accept open-ended dimensions, so a maximum width and height capped at the press sheet should be enforced server-side. It found no existing Jira or max-size check in the code snippets it saw.

**Actual Outcome:** A developer found the custom quote tool skipped its maximum-size check when "Pieces On Sheet" was overridden (96), so a mistyped 9494" width saved and ordered. The fix, rejecting any size larger than the press sheet even with the override, is scheduled for the Nov 11 release.

**Accuracy:** Partially Accurate (70%)

**Notes:** The AI's recommended server-side size limit matches the fix, but it believed no check existed when the real defect was a bypass of an existing check.

---

## 80. Ticket #87562 — Collarerate Shipping Widget issue

**Investigator's Conclusion:** It could not determine the root cause. It found shipment S-2535770 had no shipping vendor or service assigned, which could explain empty rows, and called the problem a UI rendering issue or bad data, recommending a console check, dev review and assigning a vendor and service.

**Actual Outcome:** A developer confirmed it as a REST Admin Pilot issue, reproduced on a test environment, with the classic screen working. It was fixed in 4.46.1, which went live Oct 15, and the shipping options reappeared.

**Accuracy:** Inaccurate (40%)

**Notes:** The AI's "UI rendering" instinct was close, but it pointed to missing vendor/service data on the shipment as the trigger, which was not the cause.

---

## 81. Ticket #87563 — Saddle Stich Booklet Ordering Page

**Investigator's Conclusion:** It could not find a root cause: no outage, alarm or matching Sentry error. It read the screenshot as an existing cart item in edit mode, pointed to possible but unconfirmed contributors (the TTI-23994 storefront bootstrap migration and the TTI-24223 cart JavaScript crash), and asked a developer to reproduce it with the browser console open.

**Actual Outcome:** Support could not reproduce it in prod for the reporter's own account (impersonated, which also holds the REST Admin Pilot role), another user or three customers. After the reporter pushed back, support said on Oct 16 that the issue had been resolved and asked her to log out and back in, and the ticket closed.

**Accuracy:** Inaccurate (30%)

**Notes:** The AI's leads (bootstrap migration, cart JS crash) were not what resolved it; the log-out/log-in fix matches the Oct 15 REST pilot hotfix pattern, but no cause was stated.

---

## 82. Ticket #87595 — Adding Online Special shipping

**Investigator's Conclusion:** It could not determine why the option was missing. It ruled out a missing Collaterate carrier service (`system_shipping_services` and `shipping_vendors` had nothing named "Special" or "Online") and said it might be a Pace shipping method or a site-specific shipping option that the configuration team would need to create or enable.

**Actual Outcome:** Support reproduced it in prod and stage: the Special Shipping operation in Production Plan Details offered only three choices, without "Online Special Shipping". The configuration team added it as an option on the product's PJC on Oct 19 and the ticket closed.

**Accuracy:** Partially Accurate (50%)

**Notes:** The AI correctly said a configuration change would be needed and ruled out carrier services, but it looked in the wrong place and did not identify the operation choice.

---

## 83. Ticket #87598 — OLF labels not printing when in the gang window

**Investigator's Conclusion:** It could not find the cause. It guessed the OLF gang job built by `impose.ts` in `retail-gang-phoenix-api` might not carry the member jobs' label tasks, and recommended getting a gang number and checking logs and Sentry; printing from each individual job works as a workaround.

**Actual Outcome:** Support reproduced it in stage and prod: on the Producer gang page the Labels button shows a raw template or a count of 0 and does nothing, with a console error in `getSelectedJobLabels` because `items` is undefined. It was assigned to a developer and closed as resolved on Oct 20.

**Accuracy:** Inaccurate (35%)

**Notes:** The real fault was in the Producer gang page's front-end label-count code, not in the gang-creation task flattening the AI suspected.

---

## 84. Ticket #87602 — Meta MOD Site - product was allowed to backorder

**Investigator's Conclusion:** It could not confirm a root cause. The Meta site's `backorder_enabled = false` was correct and no order showed a backorder, but three orders had reserved stock that did not exist, pushing available inventory to -3, which behaves like a backorder though it is not one. It noted the code guard only flags such items rather than blocking checkout.

**Actual Outcome:** Support could not reproduce it and escalated to the dev team. A developer later found the three single-unit orders were accepted correctly with 16 on hand, then a warehouse cycle count of -16 took on-hand to 0 after the orders were placed, and nobody was alerted. A PR (7800) was in review to alert users and the warehouse team, and the ticket remained open.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI correctly separated this from a true backorder and found available at -3, but it said the reservations had no stock behind them rather than identifying the post-order warehouse cycle count.

---

## 85. Ticket #87601 — Kohler Signature Stores - 11 products 1212305

**Investigator's Conclusion:** The most likely cause is that the site 531 product JSP template no longer compiles because the generated method exceeds the JVM's 64KB limit, which would break every product page on that template. It based this on a log excerpt already posted in the ticket and recommended splitting the JSP or reverting the last template or product change, and treated the "visible to segments" setting as unrelated.

**Actual Outcome:** A developer posted that it had been fixed, without describing the change, and support closed the ticket after confirming it was resolved. The log excerpt on the ticket, posted by support before the AI comment, showed the same JSP compile error.

**Accuracy:** Accurate (85%)

**Notes:** The fix details were not recorded, but the AI's compile-limit reading of the logged error is the only technical explanation on the ticket.

---

## 86. Ticket #87614 — Sephora Inventory ID 27432 Incorrect reserved quantity?

**Investigator's Conclusion:** The reserved quantity of 5 was wrong: it found no active placed order holding stock, and the 5 appeared left over from 8 cancelled order items (cancelled Oct 19) whose `stock_reserved_released_quantity` stayed 0, so no release was written. It recommended resetting `reserved_inventory` to the correct value (likely 0) and filing a bug for cancellations not releasing reservations.

**Actual Outcome:** Support saw that every order for the SKU had been cancelled, offered to set reserved to 0, and the requester agreed. Reserved inventory was set to 0 and the requester placed the store punchlist order before the deadline.

**Accuracy:** Accurate (95%)

**Notes:** The data fix applied is exactly what the AI recommended; the underlying cancellation-release bug was not discussed.

---

## 87. Ticket #87619 — Unable to Allocate

**Investigator's Conclusion:** Its first comment found no root cause and suspected a browser-side hang. A second comment, written after support reproduced it in prod, found the root cause: the Allocate panel throws a JavaScript error on orders with customer rework production runs for users in the REST Admin Pilot role, because the REST run DTO omits job and offering names. It named the fix commit under TTI-20177 and the hotfix 4.46.3, with a classic-screen workaround.

**Actual Outcome:** Support reproduced the greyed-out Allocate screen in prod on order 2047266 and said the issue was resolved that afternoon. The requester acknowledged and the ticket was closed.

**Accuracy:** Accurate (90%)

**Notes:** The second comment's pilot-role diagnosis fits the Oct 19 hotfix cluster; the first comment alone was inconclusive but correctly suspected a client-side hang.

---

## 88. Ticket #87620 — HealthMarkets - Trying to Add Additional information fields on new products and getting error message - due ASAP

**Investigator's Conclusion:** Its first comment could not find the cause and noted the "This is a required field" error is a backend validation. A second comment confirmed the root cause: for users in the REST Admin Pilot role, a JSON-parsing change meant drop-down values and Admin Display choices were dropped, so the backend rejected the field. It cited a fix commit under TTI-20177 for hotfix 4.46.3 and a classic-screen workaround.

**Actual Outcome:** Support escalated to the dev team and reproduced it in staging, then said the issue had been fixed within about seven hours. The requester confirmed it was working and the ticket was closed.

**Accuracy:** Accurate (90%)

**Notes:** The final diagnosis matches the confirmed fix; the first comment correctly identified the validation message but not the cause.

---

## 89. Ticket #87627 — Permission to change Sales in Collaterate

**Investigator's Conclusion:** It could not identify the exact permission that controls editing the Sales Rep on an order. It treated the request as an access request and recommended a System Admin compare the user's roles with a colleague who can edit the field, grant the missing role, and confirm site access.

**Actual Outcome:** Support assigned the "Order Sales Rep Manager" role to the requester, verified by logging in as her, and the configuration team confirmed the update. The requester confirmed it worked and a second user was updated the same way.

**Accuracy:** Accurate (85%)

**Notes:** The AI did not name the role but its role-comparison-and-grant recommendation is what resolved it.

---

## 90. Ticket #87659 — Date Picker additional info fields won't save the "show on order" checkboxes

**Investigator's Conclusion:** Its first comment found the three Date Picker fields saved with an empty `admin_display_options` list, a defect in the Date Picker save path rather than user error. A second comment said it was fixed in 4.46.3: the REST pilot save was dropping the Admin Display choices, the same defect as ticket 87620, and the affected fields need their checkboxes re-set.

**Actual Outcome:** Support said the issue was resolved and gave the re-save instruction, and the requester confirmed "This is working now" on Oct 20.

**Accuracy:** Accurate (92%)

**Notes:** The data finding was correct and the second comment's root cause and re-save instruction matched what the requester did.

---

## 91. Ticket #87660 — Smartpress Site Order Pricing Discrepancy - 2047266

**Investigator's Conclusion:** Its first comment confirmed the split (six of eight items saved at $23.08, the item's production cost) but found no root cause. A second comment, posted by the developer using the AI account, found it was bug TT-367: duplicating an item in the cart priced the copy at production cost; the order was placed 2026-08-18 and the fix went live 08-19. The customer was undercharged and the reorder price of $161.47 is correct.

**Actual Outcome:** The developer told support that the reply above was theirs and that the customer was undercharged because of a bug on the first order. The requester thanked them and the ticket was closed on Oct 29.

**Accuracy:** Accurate (90%)

**Notes:** The final explanation is the confirmed answer, but it came from a developer-assisted follow-up; the first AI comment alone could not explain the pattern.

---

## 92. Ticket #87661 — Job Configuration Defaults: side2InkType: 0 is ignored by the new quote engine, so single-sided products quote as 4/4

**Investigator's Conclusion:** The code in `sls-pdp-product-configuration` confirmed the reported root cause: `getDefaultId()` treats an explicit 0 as falsy, so `side2InkType: 0` falls through to the PJC's default ink. It recommended checking raw values before calling `getDefaultId`, adding tests, and avoiding ink 6 ("None") as a workaround.

**Actual Outcome:** A developer wrote a matching root-cause analysis (same file and functions, same fix) and asked the platform developers on Oct 23 to implement it in the serverless repo. The ticket was still open.

**Accuracy:** Accurate (95%)

**Notes:** The requester's own write-up already contained the cause, and the AI and developer agreed with it; no fix had been delivered yet.

---

## 93. Ticket #87666 — Jobs Not in Producer "Planning" Section

**Investigator's Conclusion:** It did not find a definite cause, but both jobs were valid, not cancelled and Production Ready, yet missing from the production queue, and both parent orders were already marked Shipped even though the jobs were not. It hypothesised that this mismatch kept them out of Planning, and recommended resetting the order status through the admin tool rather than placing more reworks.

**Actual Outcome:** A developer advised changing the order status back to In Process, then switching each job's production status to Planning and back to Production Ready to re-sync it in Producer. The requester said "This solution worked!"

**Accuracy:** Accurate (92%)

**Notes:** The AI's shipped-order diagnosis and "reopen the order, not more reworks" advice matched the fix.

---

## 94. Ticket #87668 — DQ - unable to set "Ordered As" to EA from Pack SKU102543482

**Investigator's Conclusion:** The symptom is real: "Ordered As" is stored as Pack (`PA`) at the system level and the edit does not save. It could not find why, suspected a blank selection being ignored in the admin save path, and suggested a developer set `stock_unit_of_measure` to NULL as a stopgap.

**Actual Outcome:** Support reproduced it in prod and stage, then found it did not happen without the REST Admin Pilot role and that a separate pilot fix was still in progress. A developer updated the field for the SKU as a workaround and the ticket was closed on Oct 21 as fixed.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI's data-level stopgap matched what was done, but it missed that the edit failed only under the REST Admin Pilot screen.

---

## 95. Ticket #87706 — AAP Sku 102276805 not showing backordered

**Investigator's Conclusion:** It could not confirm a cause: order line 4749033 had 8 units ordered and 0 backordered while the variant held 5 on hand and 5 reserved, so a shortfall existed that was not recorded. It suggested the warehouse sync overwrites reserved and backorder values, and recommended a developer set `stock_backorder_quantity` and the variant backorder through the application.

**Actual Outcome:** A developer calculated 13 units open across two orders against 5 available, so 8 should be backordered, and asked the configuration developer to adjust prod. He replied "you are all set" on Oct 22 and the requester thanked him.

**Accuracy:** Partially Accurate (75%)

**Notes:** The AI correctly found the unrecorded shortfall and recommended a data fix, but its warehouse-sync theory was not confirmed and the team computed the backorder across both open orders.

---

## 96. Ticket #87726 — Turnaround time shows “undefined Max Quantity” on new master product

**Investigator's Conclusion:** The AI saw DB `max_qty=0` for master product 109465 and could not reproduce the issue. It suggested the value was probably missing at first and filled in by a later save.

**Actual Outcome:** A developer reproduced the issue in staging and traced it to the REST Admin Pilot role (TTI-24894). It was fixed and the ticket was closed Oct 21.

**Accuracy:** Inaccurate (35%)

**Notes:** The AI did not identify the pilot-role root cause and offered a "stale value" explanation instead.

---

## 97. Ticket #87731 — Lucid - Variant cannot be disabled

**Investigator's Conclusion:** The AI found `enabled=true` still set on the variants and called it a product bug in the disable DELETE path (`removeSiteOfferingVariant`).

**Actual Outcome:** A developer reproduced the issue and tied it to the REST Admin Pilot role. It was fixed with PR 7779 and closed Oct 21.

**Accuracy:** Partially Accurate (75%)

**Notes:** The AI correctly identified a product defect but not the pilot-role cause.

---

## 98. Ticket #87732 — Fjallraven MOD - Approval in Site Settings error

**Investigator's Conclusion:** The AI could not reproduce the error or confirm a cause, and asked for the exact error text.

**Actual Outcome:** A developer reproduced the error only with the REST Admin Pilot role and fixed it in PR 7780. The ticket was closed Oct 21.

**Accuracy:** Inaccurate (30%)

**Notes:** No root cause was offered. This is part of the second pilot cluster.

---

## 99. Ticket #87740 — Customer Login Not Working - Julie Jacobsen

**Investigator's Conclusion:** The AI found a curly apostrophe (’) in the stored username while a straight apostrophe was being typed.

**Actual Outcome:** Support confirmed the same cause and gave the copy/paste workaround. The customer logged in and the ticket was closed Oct 22.

**Accuracy:** Accurate (97%)

**Notes:** Correct and specific diagnosis.

---

## 100. Ticket #87757 — MOD Sites - Links to Category Pages now say NULL

**Investigator's Conclusion:** The AI identified a known REST-pilot display bug (TTI-24530, PR #7784) that was not yet in prod.

**Actual Outcome:** The issue was reproduced with the pilot role and fixed in hotfix 4.46.5 on Oct 21. The requester confirmed.

**Accuracy:** Accurate (92%)

**Notes:** The AI tied the issue to the right known defect.

---

## 101. Ticket #87653 — True Commery Foundry

**Investigator's Conclusion:** The AI could not find why Kohler never received an EHDI for the three orders, and it could not see the True Commerce side. It confirmed that the orders were approved in Collaterate on 9/30 (not 10/1) with blank PO fields and no outbound EDI log entries. It recommended checking the True Commerce Integration Service and the editools owner.

**Actual Outcome:** Support found that the orders were approved before the configurator's "BOM builder" had completed. The fix was to move the orders from In Process to On Hold and back to In Process, which re-triggers the EDI 850. The requester acknowledged.

**Accuracy:** Inaccurate (40%)

**Notes:** The AI's Collaterate-side facts were correct (approved, no PO, no EDI send logged). It did not find the BOM-builder timing root cause, and its True Commerce investigation steps were not what resolved it.

---

## 102. Ticket #87771 — Collaterate Customer Name Business Classification Update

**Investigator's Conclusion:** The AI explained the existing rules-based business/personal classification. No rule uses star rating, and the personal-email-domain rule can override a business name. It found that 11 five-star customers are classified personal, all through the email-domain rule. It said this needs a development change and recommended a star-rating rule, reordering the rules and changing the default.

**Actual Outcome:** An engineer confirmed the rules live in the monolith but the auto-classification engine runs in a separate process. The engineer also agreed the ask is a broader rework (default to business, reprioritize rules, add star rating and purchase history). The ticket was escalated to L3 and linked to the existing epic TTI-24056. No fix had been delivered.

**Accuracy:** Accurate (85%)

**Notes:** No confirmed outcome yet. The AI's analysis matched the engineer's scoping. The AI did not locate the engine, which it flagged as unverified.

---

## 103. Ticket #87778 — Collaterate issue

**Investigator's Conclusion:** The AI could not find the root cause because the ticket had no order number. It suggested a possible link to the recent removal of the Archive action (TTI-24188/TTI-24779), labelled as a hypothesis.

**Actual Outcome:** Support found a permissions problem caused by the REST Admin Pilot role. Removing the role from the user, re-login and cancelling the job worked, and the ticket was closed Oct 21.

**Accuracy:** Inaccurate (25%)

**Notes:** The AI's archive-removal hypothesis was wrong, and it did not suspect the pilot role. It was honest about having no evidence. Part of the second pilot cluster.

---

## 104. Ticket #87789 — Supplier Reference in MOD sites

**Investigator's Conclusion:** The AI could not confirm the cause. Its most likely explanation was a missing `SUPPLIER_REFERENCE` edit permission, which makes the code skip the save silently. It confirmed that the value was never stored and that the problem was not platform-wide.

**Actual Outcome:** Support reproduced the issue in staging and tied it to the Rest Admin Pilot role. Removing the role let the user save the value, and the requester confirmed the workaround worked. The dev team was working on a permanent fix.

**Accuracy:** Partially Accurate (70%)

**Notes:** The AI correctly pointed to a permission-related silent drop of the field, but it missed the pilot role as the trigger.

---

## 105. Ticket #87840 — Bulk Load Stock Products tool doesn’t save Replacement Cost

**Investigator's Conclusion:** The AI confirmed the requester's diagnosis in code. The bulk tool sends `replacementCost`, but the create DTO only accepts `stockReplacementCost`, so the value is dropped silently. It recommended renaming or aliasing the field, adding tests, and checking the Expiration Date requirement.

**Actual Outcome:** The ticket was still open, with the work routed to a developer. No fix was reported in the ticket by the audit date.

**Accuracy:** Accurate (90%)

**Notes:** Nobody has confirmed a fix, so this rating reflects the strength of the analysis. It matched the requester's diagnosis and added evidence from other repos.

---

## 106. Ticket #87925 — B1 measurement

**Investigator's Conclusion:** The AI found nothing to investigate. The ticket describes itself as a measurement ticket for a reconciler feasibility build with "No action needed", and the notes look like test payloads. It recommended closing the ticket as a test artifact.

**Actual Outcome:** The ticket was closed (status 5) the same day with no action taken.

**Accuracy:** Accurate (95%)

**Notes:** The AI correctly recognized a synthetic test ticket and did not run needless queries.

---

## 107. Ticket #87947 — Error Loading Orders from DC for Team Cogan in Collaterate

**Investigator's Conclusion:** The AI could not determine the cause of the generic "Error occurred" banner on the Team Cogan orders page. It found no account, role or permission problem for the new requester. It suggested the new account's lack of orders or division mapping, or a recent error-handling change (TTI-24741), as candidates.

**Actual Outcome:** Support found the order had been placed by another user. A Collaterate order can only be opened by the person who placed it, and the page shows a generic error instead of an access message. The requester accepted the explanation and the ticket was closed.

**Accuracy:** Inaccurate (35%)

**Notes:** The AI correctly ruled out an account problem. It did not identify the order-ownership restriction. The ticket gave no order number, so the AI could not check ownership.

---

## 108. Ticket #87954 — FedEx Authenticated Delivery

**Investigator's Conclusion:** The AI said the platform already supports a direct "signature on delivery" option for FedEx and UPS, but it is disabled on every site. It found no support for FedEx Authenticated Delivery, which would need new development. It recommended enabling the existing option per site and opening a TTI to scope Authenticated Delivery.

**Actual Outcome:** Engineers confirmed the signature feature is implemented end to end and only needs to be enabled per site. TTI-24829 is a separate bugfix and does not block it. The requester said they want it for Smartpress customers only when requested, and support planned to enable it after a quick test.

**Accuracy:** Accurate (95%)

**Notes:** The AI's reading of the code and feature state was borne out. The ticket was still open at the time of the audit.

---

## 109. Ticket #87975 — Laminating estimated times

**Investigator's Conclusion:** The AI traced the 1h26m estimate to the formula on operation item 272 (600 s setup plus 3.27 s per press sheet, last edited in 2022). It noted that this implies about 1,100 sheets/hour against the real 250, and that there is no sides multiplier. It recommended confirming real rates and updating the formulas as a data change.

**Actual Outcome:** The config team updated the laminate time formulas, which apply to new jobs. The requester then corrected the target rates to 4 s per sheet, or 8 s if double-sided, and the config team applied them. The ticket was closed.

**Accuracy:** Accurate (95%)

**Notes:** The diagnosis and the recommended fix (a data change to the formulas) matched what was done.

---

## 110. Ticket #87977 — Temp Badges

**Investigator's Conclusion:** The AI found no record of where badge stock is kept at SPSC. It summarised the temp-badge types and the Genea print steps from Confluence. It recommended bringing blank cards and printing from the SPSC printer.

**Actual Outcome:** The IT technician offered to bring blank cards and print the badges on Monday, and the requester agreed. The ticket was still open.

**Accuracy:** Accurate (90%)

**Notes:** The AI's practical step matched the plan the team settled on. The ticket was an informational request, so there was no root cause to find.

---

## 111. Ticket #87986 — Jira tickets stuck in placing.

**Investigator's Conclusion:** The AI found no bug in Collaterate. The orders matched the Auto Order Intake Python (AOIP) behaviour described in the ticket: order 2103720 already existed, and order 2102104 already existed so the ticket was treated as a duplicate. It said the root cause is in AOIP's resend handling, which it could not inspect, and recommended AOIP fixes plus manual ticket moves.

**Actual Outcome:** The responder said code changes were being made to help with this and to surface when it occurs. The ticket was marked complete, with future work orders handled by the code update.

**Accuracy:** Accurate (90%)

**Notes:** The AI's Collaterate-side data supported the requester's explanation, and its recommended AOIP fixes match the direction of the code change. It could not see the Jira SCWO tickets.

---

## 112. Ticket #87990 — 2076433 - Unable to cancel hards proofs or reworks

**Investigator's Conclusion:** The AI found the rework saved as cancelled but still holding a shipment allocation (9 of 9 recent child items). It treated this as a likely application bug in the cancel or allocation cleanup and left the root cause unconfirmed. It recommended a TK bug and a manual cleanup of the allocations.

**Actual Outcome:** Support reproduced the issue in production and tied it to the REST Admin Pilot role. The cancel saves and Producer shows the job as cancelled, but the order page does not receive the cancelled status for pilot-role users. PR #7815 fixed it for the Oct 28 release.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI correctly established that the cancel itself saved and that it was a product bug rather than user error. It pointed at shipment allocation cleanup rather than the pilot role, and the manual-delete workaround it suggested was not needed.

---

## 113. Ticket #87995 — update PID

**Investigator's Conclusion:** The AI could not tell what "PID 4402" refers to. It found offering records matching 4402 and 32874 but could not link them to a requested change. It asked the requester to say which system the PID appears in.

**Actual Outcome:** The config team said the Aberdeen Soft Knit 4.5oz fabric in Collaterate now points to Pace ID 32874 instead of 4402, and that new jobs pick up the new ID. Existing jobs still show 4402.

**Accuracy:** Inaccurate (40%)

**Notes:** The AI's clarifying questions were reasonable, as the ticket was ambiguous. It did not reach the fabric/Pace ID interpretation, and the offering records it matched were not the relevant ones.

---

## 114. Ticket #87999 — Failure to Call to Press - 4750465-1

**Investigator's Conclusion:** The AI found that job 4750465-1 has no ship or finish date in Collaterate (all four date fields NULL). It concluded that the date was never written for this rework and recommended setting the dates manually, as the sibling jobs have them.

**Actual Outcome:** Support saw the job as Printed and asked the requester to clear the cache. The requester then confirmed it was showing Printed, and the ticket was closed.

**Accuracy:** Inaccurate (25%)

**Notes:** The ticket was resolved as a stale display in the requester's view. The AI's conclusion that the date was missing led to a manual-edit recommendation that was not needed.

---

## 115. Ticket #88014 — Collaterail - permissions

**Investigator's Conclusion:** The AI said this is not a bug. The requester's roles on the stage environment were never copied from prod, since her stage admin account has only Order Viewer and no Shipping role. It recommended an admin add the roles in stage and check whether stage resets would wipe them.

**Actual Outcome:** The config team confirmed the prod roles did not carry over to stage, restored them, and added Shipping in prod. The requester confirmed it looked good, and the team judged it was an accidental adjustment that should survive stage resets.

**Accuracy:** Accurate (97%)

**Notes:** The AI's diagnosis and fix matched exactly, and it correctly flagged the stage-refresh risk.

---

## 116. Ticket #88054 — HealthMarkets - New Agent Kit Order 2106217

**Investigator's Conclusion:** The AI found no system error. The eight child template jobs had no personalized file (null session code and file URL) while the kit parent job did. It treated the ticket as a manual art-creation request for prepress and suggested the dev team look at why the template output did not generate for the child jobs.

**Actual Outcome:** Support reproduced the issue in staging. An engineer explained that nothing in the system personalizes the kit's child CHILI jobs, because the kit answers are stored only on the parent job. A designer was added to build the art manually, and templated print files were then generated for all POD jobs. A developer later said the PDF failure was probably a temporary CHILI problem and that the kit process is a known manual workflow.

**Accuracy:** Partially Accurate (80%)

**Notes:** The AI's reading of the data and its recommendation to produce the art manually matched what happened. It did not identify the missing parent-to-child data copy or the CHILI instability.

---

## 117. Ticket #88087 — Collaterate - more oddities

**Investigator's Conclusion:** The AI said this is not a display bug. A one-time image-migration job (`MigrateOfferingImageFilesToS3-prod`) wrote its own name into `site_offerings.updated_by` on about 31,900 products, which overwrote the real last editor. It recommended a TTI bug and restoring the values.

**Actual Outcome:** Support reproduced the issue in prod. The responder confirmed to the requester that the system job's name shows on about 31,900 products because it moved images and wrote its own name as editor, and that a person did not edit them. The requester accepted this and the ticket was closed.

**Accuracy:** Accurate (97%)

**Notes:** The cause, the product count and the explanation to the requester all matched. The restoration of original editor values was not done.

---

## 118. Ticket #88088 — Presbyterian Foundation URL Name Request

**Investigator's Conclusion:** The AI found that the site already exists in prod and is not live, and that its `subdomain_prefix` was cut off at 20 characters. The requested prefix is 23 characters. It could not find where the limit is enforced and recommended a developer change or a data fix.

**Actual Outcome:** Support tried the admin fields and confirmed that Short Name and Subdomain Name both accept only 20 characters. The request stayed open and escalated for a dev change.

**Accuracy:** Accurate (88%)

**Notes:** Nobody had resolved the request at the time of the audit. The AI's finding of a 20-character limit, rather than the 22 the requester said, matched support's test.

---

## 119. Ticket #88098 — #2100456 - Packing Task

**Investigator's Conclusion:** The AI found no root cause. It called the freeze a client-side or UI problem that it could not reproduce, and it noted that Pace, Sentry and task data showed no related errors. It suggested a hard refresh, a browser console capture and a review of that day's merged PRs.

**Actual Outcome:** Support reproduced the issue in staging and tied it to the Rest Admin Role. With that role, the Special Packaging and Special Shipping choices show incorrectly and cannot be saved, while without it they work. The issue was passed to the dev team.

**Accuracy:** Inaccurate (25%)

**Notes:** The AI's pointers to a client-side cause and a recent deploy were wrong, and it missed the pilot-role cause. Part of the second pilot cluster.

---

## 120. Ticket #88101 — No longer a spot to add the cost when doing "I will describe delivery method."

**Investigator's Conclusion:** The AI judged this to be a regression in the new order-details UI. It said the actual-cost field is only drawn when the shipment has third-party billing data, which a describe-delivery shipment normally lacks, and that it is not editable after shipping. It recommended a TTI bug.

**Actual Outcome:** Support reproduced the missing field, but another order in staging showed the cost field. A developer said the page needed a refresh after changing the shipping service, then found it only affected REST Pilot users. A fix was deployed and the requester was told the issue was fixed.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI correctly identified a UI defect in the cost editor but described it as general behaviour for every describe-delivery shipment. The actual trigger was the REST pilot rollout.

---

## 121. Ticket #88109 — Chili Required Fields Prompt Adjustment Request

**Investigator's Conclusion:** The AI confirmed the code behind the request. `validateChiliDocument()` in `personalizeController.js` returns on the first empty required variable, which explains why only one field is reported. It also uses the internal `name` rather than a display name. It outlined a small change and noted the ticket is really an enhancement.

**Actual Outcome:** A developer asked for an example product with multiple required fields and was given the Fairview Appointment Card. The ticket was still open and the change had not been delivered.

**Accuracy:** Accurate (90%)

**Notes:** No fix was confirmed, so this rating reflects the strength of the analysis. The requester had already named the same function, and the AI confirmed it in code. The AI flagged that the display-name property name was unverified.

---

## 122. Ticket #88111 — Can't login into JITBIT

**Investigator's Conclusion:** The AI found nothing in TBG's infrastructure that explains the issue. It judged Jitbit to be an external SaaS product, so the login and password-reset errors were most likely on the Jitbit side or in the account. It recommended asking for the exact errors and having a Jitbit admin check the account.

**Actual Outcome:** Support asked the requester to try again, and the requester then confirmed it was fixed. The ticket does not say what was changed.

**Accuracy:** Partially Accurate (65%)

**Notes:** The AI's pointer to a Jitbit-side account issue is consistent with a quick fix by support, but the ticket does not confirm the cause. It did not offer a specific root cause.

---

## 123. Ticket #88068 — Meta MOD - stock products sales tax category

**Investigator's Conclusion:** The AI did not find the cause. It said the data showed no clear failure and suspected the offering save path changed by TTI-21192 might null `salesTaxCategory`. It recommended that a developer reproduce the problem.

**Actual Outcome:** Support reproduced it in staging. Support said the data is saved in the database and only the UI does not show it, and that removing the Rest Admin Pilot role is a workaround. A fix was deployed and the requester was told on Oct 29 that it was fixed.

**Accuracy:** Inaccurate (30%)

**Notes:** The AI's TTI-21192 suspicion was wrong, and it missed the pilot-role UI cause. The AI also implied values might be lost, while the actual data was saved. Part of the second pilot cluster.

---

## 124. Ticket #88078 — Producer

**Investigator's Conclusion:** The AI could not pinpoint the cause because the ticket had no job number, error text or screenshot. It pointed to unrelated Producer back-end sync errors in Sentry (`_cost_obj_exists` and connection resets) and said it could not confirm they caused the problem.

**Actual Outcome:** Support found an "Access Denied" error in the logs for the requester's request to the production workstations endpoint, granted the missing permissions, and asked the requester to log out and back in. The requester confirmed it was working and the ticket was closed.

**Accuracy:** Inaccurate (20%)

**Notes:** The Sentry errors the AI cited were not related, and the true cause was a missing permission. The AI explicitly did not claim a cause. It asked for more detail, as support also did.

---

## 125. Ticket #88142 — https://collaterate.jitbit.com/ - unable to login

**Investigator's Conclusion:** The AI said it could not fix this from the available tools. It identified the site as a vendor-hosted Jitbit instance and judged this to be an account or access issue inside Jitbit. It recommended that a Jitbit admin check whether the account was disabled or removed, and reset the password.

**Actual Outcome:** A support engineer fixed the issue and told the requester she could log in. The ticket gives no details about what was changed.

**Accuracy:** Partially Accurate (70%)

**Notes:** The AI's reading that this was a Jitbit account matter was consistent with the outcome, but the cause was not recorded.

---

## 126. Ticket #88159 — 2108296 - Product Template Not Generating

**Investigator's Conclusion:** The AI found that job 4783576 has a closed template session but no output file URL, file ID or preview URLs, while the sibling jobs have them. It did not find the root cause. It recommended checking the template vendor session for an output file and re-triggering the callback, or having the customer redo the template.

**Actual Outcome:** Support reproduced the issue in prod. The preview opens as a blank document and the file could not be saved. The config team built the PDF manually from the customer's information and sent it to the requester. No root cause was recorded in the ticket.

**Accuracy:** Partially Accurate (70%)

**Notes:** The AI's data findings were correct and its "customer supplies data and the file is rebuilt" fallback matches what happened. The root cause remains unknown.

---

## 127. Ticket #88163 — Collaterate - Edit Basic Properties Error

**Investigator's Conclusion:** The AI could not identify the cause because the error text was in an unseen screenshot. It guessed that the data saves but the response or the UI handler that closes the popup fails. It recommended getting the error text and checking a possible link to the COMET-to-REST conversion tickets.

**Actual Outcome:** A developer reproduced the problem in prod only and found that the save returned a 4xx "Visibility cannot be changed when product status is not ACTIVE" for shared products. The cause was a reference comparison of `ProductStatus` objects that fails when the status comes back through the Hibernate second-level cache. The fix was in progress and the ticket was closed on Oct 29.

**Accuracy:** Inaccurate (30%)

**Notes:** The AI's observation that the data saves but the response fails was in line with the real behaviour. It did not identify the cause, and its pointers to the COMET-to-REST tickets were not relevant.

---

## 128. Ticket #88174 — Error occurred. Contact support for help if the problem persists

**Investigator's Conclusion:** The AI could not determine the root cause of the generic error when voiding a shipment. It found two live UPS shipments on the order. It suspected a UPS-side rejection, such as a label already voided or already scanned, and asked for logs.

**Actual Outcome:** A developer found the first void succeeded at UPS but the Collaterate transaction rolled back after a Hibernate `StaleStateException` on the inventory variant, caused by a stale second-level cache copy. Every later retry failed because UPS said the shipment was already voided. The developer reproduced it in staging, noted the order needed a database fix, and later reported the issue fixed.

**Accuracy:** Inaccurate (45%)

**Notes:** The AI's "label already voided" hypothesis matched the state seen on the retries, but it did not find the rollback and the stale-cache root cause. The user held the Rest Admin pilot role, but it was not the cause.

---

## 129. Ticket #88180 — adding file for non-profit

**Investigator's Conclusion:** The AI found that the requester's admin account has no system roles, while her two teammates have 9–10 roles each. It said this was the likely cause of the failed uploads and recommended granting the same role set. It could not confirm which role the upload needs.

**Actual Outcome:** Support's logs showed Access Denied errors, and in staging, granting the User & Division Manager role let the image save. The config team updated the requester's credentials and told her to log out and back in.

**Accuracy:** Accurate (92%)

**Notes:** The AI identified the missing roles and named User & Division Manager as a candidate, which proved to be correct.

---

## 130. Ticket #88179 — 3rd Party Shipping Issues

**Investigator's Conclusion:** The AI said the most likely cause is a code gap when a job is routed to the South Carolina fulfillment center. The new shipment does not copy the reference shipment's third-party billing settings, and it rebuilds billing from the site configuration, so billing falls back to the Smartpress account. It said this was a strong lead and not yet proven.

**Actual Outcome:** Support reproduced the issue in staging by adding a planned Large Format - SC shipment, which showed the Smartpress billing account instead of the customer's. The developer then reported that the fix was available in production and closed the ticket.

**Accuracy:** Accurate (90%)

**Notes:** The AI's cause matched the reproduction. The ticket does not describe the exact code change, so the match rests on the reproduction steps.

---

## 131. Ticket #88204 — 2109185 - can't set dates

**Investigator's Conclusion:** The AI could not find the cause of the "can't set dates" problem because the ticket does not say which screen or date field fails. It noted that 2109185 matches both a new order and an old, shipped 2021 job. It found blank ship dates on the new order's shipment, which it said is expected until the order is processed, and no errors in the data sources it could reach.

**Actual Outcome:** The ticket was still open at the time of the audit, with no human reply recorded and no cause confirmed.

**Accuracy:** Partially Accurate (50%)

**Notes:** Nobody has confirmed anything, so this rating reflects the strength of the analysis. It was careful about the ambiguous number and asked the right clarifying questions, but it did not offer a cause.

---

## 132. Ticket #88141 — Window Decals Product Configuration

**Investigator's Conclusion:** The AI found the cause in the code. In the removable cling (PJC 678) second-surface branch, the white-stock case sets the ink configuration to "Standard CMYK (Second Surface)", while production wants First Surface on white stock. It recommended changing that line, and checking the static path and which copy of the file is live.

**Actual Outcome:** The config team said it is not a config issue. A developer posted the same code branch and called the second-surface ink line "the bug", then assigned it to the developer working on related ticket 87970. The ticket was pending with no fix recorded.

**Accuracy:** Accurate (95%)

**Notes:** No fix was confirmed yet. The AI's finding agrees with the developer's, and it flagged real uncertainty about which file copy is loaded.

---

## 133. Ticket #88235 — thd services sku 101117985-0001 adjustment

**Investigator's Conclusion:** The AI found the SKU on the THD Home Services site with backorder at 20 and recommended setting `backorder_inventory` to 10 for a requested available of -10. It noted the variant is warehouse-managed, so the value could be overwritten.

**Actual Outcome:** Support adjusted the inventory, but the requester reported that order 2098843 still showed 20 on backorder. A developer then fixed it and found 4 other products on that site with inventory drift. The order showed 10 afterwards.

**Accuracy:** Partially Accurate (80%)

**Notes:** The AI's diagnosis of the SKU's current values and the target change was right, but it did not anticipate the extra drift between the variant and the order. Inventory data-fix family.

---

## 134. Ticket #88237 — AAP SKU 102276805-0001 adjustment

**Investigator's Conclusion:** The AI confirmed the SKU shows a backorder of 5 although actual inventory is 161 and reserved is 8. It recommended setting `backorder_inventory` to 0 and checking the warehouse sync and open order items.

**Actual Outcome:** Support adjusted the inventory within about 10 minutes, and the ticket was closed.

**Accuracy:** Accurate (92%)

**Notes:** The AI's diagnosis and requested change matched. Inventory data-fix family.

---

## 135. Ticket #88239 — Sephora Product ID 27432 Adjustment

**Investigator's Conclusion:** The AI could not find an "Inventory ID 27432" on the Sephora: Inventory site and made no change. It found that 27432 matches variants and offerings on other sites, so it recommended asking the requester to confirm the SKU or item name before anyone adjusts stock.

**Actual Outcome:** Support adjusted the inventory about four minutes after the AI comment, without asking for clarification. The ticket was closed.

**Accuracy:** Inaccurate (40%)

**Notes:** The AI's caution about the ambiguous ID was reasonable, but support identified the correct item immediately, so the AI failed to resolve a routine inventory-adjustment request. The requested quantities were not verified.

---

## 136. Ticket #88252 — Collaterate # 2103629

**Investigator's Conclusion:** The AI found job 4790505 on order 2103629, still active with 1 unit on backorder. It could not cancel it because of read-only access, and it recommended that support or an admin cancel the job through the order admin.

**Actual Outcome:** Support found that the job could not be cancelled in prod. In staging, it could be cancelled once the order status was changed to In Process, while the order was in Shipped status. Support told the requester to set the order to In Process and cancel, and the requester confirmed it was fixed.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI's reading of the data was correct, but its "cancel it through the admin" recommendation did not work as written. It missed that the order status blocked the cancel, and a REST Admin pilot comparison was part of the test.

---

## 137. Ticket #88264 — Backorder Issue with Order 2098843

**Investigator's Conclusion:** The AI found that job 4760641 shipped only its in-stock quantity of 90 and the 10-unit backorder was still recorded on it. The requester's quantity adjustment moved the units to job 4790709 but never cleared the flag on the already-shipped job. It recommended a data fix setting `stock_backorder_quantity` to 0 on job 4760641.

**Actual Outcome:** Support adjusted reserved and backorder quantities, but the job still showed as backordered. A developer then ran an UPDATE setting `stock_backorder_quantity = 0` on job 4760641, and the requester was told the backorder status was removed.

**Accuracy:** Accurate (95%)

**Notes:** The diagnosis and the data-fix recommendation matched what was done. Inventory/backorder data-fix family, related to #88235.

---

## 138. Ticket #88265 — Some IDs are not being allowed to be ordered in Collaterate

**Investigator's Conclusion:** The AI stopped without a root cause. Both SKUs (27432 and 28513) were active, visible and in stock, so it could not tie the ordering failure to the product records. It noted that both had been edited within a minute of each other on Oct 27 by one user, after their last orders, and recommended asking that user what changed.

**Actual Outcome:** Support found that minimum quantities of 100 and 20 had been set on the two products in prod, which stopped small orders from being added to the cart. A config engineer confirmed the minimums were set by that same user, and after that user changed them the requester confirmed they were fixed.

**Accuracy:** Partially Accurate (55%)

**Notes:** The AI's pointer to the Oct 27 edit by that user was the right lead, but it did not check ordering minimums and told the team the products looked correctly set up.

---

## Summary Statistics

| Metric | Value |
|---|---|
| Total tickets | 138 |
| Rated | 138 |
| Accurate (85-100%) | 56 (40.6%) |
| Partially Accurate (50-84%) | 42 (30.4%) |
| Inaccurate (<50%) | 40 (29.0%) |
| Without AI comment | 0 |
| Failed to fetch | 0 |
| Average accuracy | 65.9% |

---

## Key Observations

- **Strong on data fixes and code-grounded diagnoses.** The AI scored 85-97% on inventory and backorder data fixes (87056, 87378, 87614, 87706, 88237, 88264), on code-grounded diagnoses (87840, 88141, 88179, 87975) and on stale-state or role problems (88014, 88180, 88087, 87740).
- **Weakest on the REST Admin Pilot role regressions.** The Oct 2 cluster (86952-86992) and the later hotfix tickets (87524-87563, 87726, 87732, 88098, 88068, 88101, 87778, 87990, 88252) mostly scored 25-55%. The AI called them client-side, unreproducible or generic bugs, and support or a developer later traced them to the pilot role. The high scores in that cluster came from 86970, 86976, 86992, 87619, 87620 and 87757, where the AI named the right known defect.
- **Most common failure pattern.** "Could not confirm / no root cause" where the real cause was a platform rollout, a permission or cache/UI behaviour, for example 88163, 88174, 87999, 87947, 88078 and 88265.
- **WAF printables 403 cluster (86876, 87007-87016).** Scores ranged from 25% to 85%. The AI often described the symptoms but only some tickets identified the allow-list rule.
- **Missing detail limits diagnosis.** Tickets without an order number, error text or a readable screenshot led to good clarifying questions but no diagnosis, and the AI over-asked on 88239, where support fixed the inventory immediately.
- **Honest caveats.** The AI flagged unverified parts (unread screenshots, missing logs) and rarely claimed an unsupported cause, though it sometimes offered a plausible wrong one (87999, 88101, 88068).
