#!/usr/bin/env python3
"""
Parses investigator accuracy audit markdown files in /audits into a single
data/accuracy_data.json consumed by the dashboard (index.html).

Deterministic, regex-based — no AI/LLM calls, so this runs for free in
GitHub Actions on every push. Re-run any time; it always rebuilds the
full dataset from scratch so edits/deletions in /audits are reflected too.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AUDITS_DIR = REPO_ROOT / "audits"
OUTPUT_PATH = REPO_ROOT / "data" / "accuracy_data.json"

TICKET_HEADER_RE = re.compile(
    r"^##\s+(\d+)\.\s+Ticket\s+#(\S+)\s*(?:—|-)\s*(.+?)\s*$", re.MULTILINE
)
ACCURACY_RE = re.compile(
    r"\*\*Accuracy:\*\*\s*([A-Za-z ]+?)\s*\((\d+)%\)"
)
PERIOD_RE = re.compile(r"\*\*Period:\*\*\s*(.+)")
TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def parse_doc(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")

    title_match = TITLE_RE.search(text)
    period_match = PERIOD_RE.search(text)

    headers = list(TICKET_HEADER_RE.finditer(text))
    tickets = []
    for i, m in enumerate(headers):
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        block = text[start:end]

        acc_match = ACCURACY_RE.search(block)
        if not acc_match:
            # Ticket with no accuracy rating (e.g. no investigator comment)
            label, pct = "No comment", None
        else:
            label, pct = acc_match.group(1).strip(), int(acc_match.group(2))

        tickets.append(
            {
                "seq": int(m.group(1)),
                "ticket_id": m.group(2).strip(),
                "title": m.group(3).strip(),
                "accuracy_label": label,
                "accuracy_pct": pct,
            }
        )

    return {
        "file": path.name,
        "doc_title": title_match.group(1).strip() if title_match else path.stem,
        "period": period_match.group(1).strip() if period_match else None,
        "ticket_count": len(tickets),
        "tickets": tickets,
    }


def build_dataset() -> dict:
    if not AUDITS_DIR.exists():
        print(f"No audits directory at {AUDITS_DIR}", file=sys.stderr)
        return {"documents": [], "generated_from": []}

    doc_paths = sorted(AUDITS_DIR.glob("*.md"))
    documents = [parse_doc(p) for p in doc_paths]

    # Aggregate stats across all docs combined
    all_tickets = [t for d in documents for t in d["tickets"]]
    rated = [t for t in all_tickets if t["accuracy_pct"] is not None]

    def bucket(pct):
        if pct >= 85:
            return "accurate"
        if pct >= 50:
            return "partial"
        return "inaccurate"

    buckets = {"accurate": 0, "partial": 0, "inaccurate": 0}
    for t in rated:
        buckets[bucket(t["accuracy_pct"])] += 1

    avg = round(sum(t["accuracy_pct"] for t in rated) / len(rated), 1) if rated else None

    return {
        "documents": documents,
        "summary": {
            "total_documents": len(documents),
            "total_tickets": len(all_tickets),
            "rated_tickets": len(rated),
            "average_accuracy": avg,
            "buckets": buckets,
        },
    }


def main():
    dataset = build_dataset()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(dataset, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} — {dataset['summary']['total_documents']} doc(s), "
          f"{dataset['summary']['total_tickets']} ticket(s).")


if __name__ == "__main__":
    main()
