#!/usr/bin/env node
/*
 * Prints the Slack window and output filename for a monthly accuracy audit.
 *
 *   node scripts/month_window.js            -> the previous calendar month (UTC)
 *   node scripts/month_window.js 2026-08    -> a specific month
 *
 * `oldest` is the first second of the month and `latest` is the first second
 * of the next month, both in UTC. They match the table in DOCUMENTATION.md.
 */
const arg = process.argv[2];
const now = new Date();
let y = now.getUTCFullYear();
let m = now.getUTCMonth();            // 0-based, current month
if (arg) {
  const hit = /^(\d{4})-(\d{2})$/.exec(arg);
  if (!hit || +hit[2] < 1 || +hit[2] > 12) { console.error('Usage: month_window.js [YYYY-MM]'); process.exit(1); }
  y = +hit[1]; m = +hit[2] - 1;
} else {
  m -= 1;
  if (m < 0) { m = 11; y -= 1; }
}
const NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const start = Date.UTC(y, m, 1) / 1000;
const end = Date.UTC(y, m + 1, 1) / 1000;
const lastDay = new Date(Date.UTC(y, m + 1, 0)).getUTCDate();
console.log(JSON.stringify({
  month_name: NAMES[m],
  year: y,
  period: `${NAMES[m]} 1–${lastDay}, ${y}`,
  oldest: start,
  latest: end,
  file: `investigator_accuracy_audit_${NAMES[m].toLowerCase()}${y}.md`
}, null, 2));
