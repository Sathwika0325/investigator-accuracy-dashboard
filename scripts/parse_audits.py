#!/usr/bin/env python3
"""
Parses investigator accuracy audit markdown files in /audits into a single
data/accuracy_data.json consumed by the dashboard (index.html).

Deterministic, regex-based — no AI/LLM calls, so this runs for free in
GitHub Actions on every push. Re-run any time; it always rebuilds the
full dataset from scratch so edits/deletions in /audits are reflected too.

Supports two section formats found across audit docs:
  FORMAT A (July 2026 style):
    ## N. Ticket #ID — Title
    **Accuracy:** Label (NN%)

  FORMAT B (August 2026 style):
    ==
    N. Ticket #ID — Title
    ...
    Accuracy: Label (NN%)
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AUDITS_DIR = REPO_ROOT / "audits"
OUTPUT_PATH = REPO_ROOT / "data" / "accuracy_data.json"

# ── Format A: ## heading style (July) ─────────────────────────────────────────
TICKET_HEADER_A_RE = re.compile(
    r"^##\s+(\d+)\.\s+Ticket\s+#(\S+)\s*(?:—|-)\s*(.+?)\s*$", re.MULTILINE
)
ACCURACY_A_RE = re.compile(
    r"\*\*Accuracy:\*\*\s*([A-Za-z ]+?)\s*\((\d+)%\)"
)
CONCLUSION_A_RE = re.compile(
    r"\*\*Investigator(?:'|')s Conclusion:\*\*\s*(.+?)(?=\n\n|\*\*Actual)", re.DOTALL
)
OUTCOME_A_RE = re.compile(
    r"\*\*Actual Outcome:\*\*\s*(.+?)(?=\n\n|\*\*Accuracy)", re.DOTALL
)
NOTES_A_RE = re.compile(
    r"\*\*Notes:\*\*\s*(.+?)(?=\n\n|\n---|\Z)", re.DOTALL
)

# ── Format B: == separator + plain text style (August) ────────────────────────
TICKET_HEADER_B_RE = re.compile(
    r"^(\d+)\.\s+Ticket\s+#(\S+)\s*(?:—|-)\s*(.+?)\s*$", re.MULTILINE
)
ACCURACY_B_RE = re.compile(
    r"(?<!\*\*)Accuracy:\s*([A-Za-z ]+?)\s*\((\d+)%\)"
)
CONCLUSION_B_RE = re.compile(
    r"Investigator(?:'|')s Conclusion:\s*(.+?)(?=\n\nActual Outcome:|\Z)", re.DOTALL
)
OUTCOME_B_RE = re.compile(
    r"Actual Outcome:\s*(.+?)(?=\n\nAccuracy:|\Z)", re.DOTALL
)
NOTES_B_RE = re.compile(
    r"Notes:\s*(.+?)(?=\n\n|\n==|\Z)", re.DOTALL
)

# ── Shared ─────────────────────────────────────────────────────────────────────
PERIOD_RE = re.compile(r"\*\*Period:\*\*\s*(.+)")
TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def _detect_format(text: str) -> str:
    """Return 'A' if the doc uses ## headings, 'B' if it uses == separators."""
    if TICKET_HEADER_A_RE.search(text):
        return "A"
    return "B"


def _split_blocks_b(text: str):
    """
    For Format B, split the document into per-ticket blocks using == separators.
    Returns a list of (seq, ticket_id, title, block_text) tuples.
    """
    # Split on lines that are exactly '=='
    raw_blocks = re.split(r"^==\s*$", text, flags=re.MULTILINE)
    results = []
    for block in raw_blocks:
        block = block.strip()
        if not block:
            continue
        header_match = TICKET_HEADER_B_RE.search(block)
        if not header_match:
            continue
        seq = int(header_match.group(1))
        ticket_id = header_match.group(2).strip()
        title = header_match.group(3).strip()
        # Body is everything after the header line
        body = block[header_match.end():].strip()
        results.append((seq, ticket_id, title, body))
    return results


def parse_doc(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")

    title_match = TITLE_RE.search(text)
    period_match = PERIOD_RE.search(text)
    fmt = _detect_format(text)

    tickets = []

    if fmt == "A":
        headers = list(TICKET_HEADER_A_RE.finditer(text))
        for i, m in enumerate(headers):
            start = m.end()
            end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
            block = text[start:end]

            acc_match = ACCURACY_A_RE.search(block)
            conclusion_match = CONCLUSION_A_RE.search(block)
            outcome_match = OUTCOME_A_RE.search(block)
            notes_match = NOTES_A_RE.search(block)

            label, pct = ("No comment", None) if not acc_match else (
                acc_match.group(1).strip(), int(acc_match.group(2))
            )
            tickets.append({
                "seq": int(m.group(1)),
                "ticket_id": m.group(2).strip(),
                "title": m.group(3).strip(),
                "accuracy_label": label,
                "accuracy_pct": pct,
                "conclusion": conclusion_match.group(1).strip() if conclusion_match else None,
                "actual_outcome": outcome_match.group(1).strip() if outcome_match else None,
                "notes": notes_match.group(1).strip() if notes_match else None,
            })

    else:  # Format B
        for seq, ticket_id, title, block in _split_blocks_b(text):
            acc_match = ACCURACY_B_RE.search(block)
            conclusion_match = CONCLUSION_B_RE.search(block)
            outcome_match = OUTCOME_B_RE.search(block)
            notes_match = NOTES_B_RE.search(block)

            label, pct = ("No comment", None) if not acc_match else (
                acc_match.group(1).strip(), int(acc_match.group(2))
            )
            tickets.append({
                "seq": seq,
                "ticket_id": ticket_id,
                "title": title,
                "accuracy_label": label,
                "accuracy_pct": pct,
                "conclusion": conclusion_match.group(1).strip() if conclusion_match else None,
                "actual_outcome": outcome_match.group(1).strip() if outcome_match else None,
                "notes": notes_match.group(1).strip() if notes_match else None,
            })

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
    print(
        f"Wrote {OUTPUT_PATH} — {dataset['summary']['total_documents']} doc(s), "
        f"{dataset['summary']['total_tickets']} ticket(s), "
        f"{dataset['summary']['rated_tickets']} rated."
    )
    # Print per-doc summary for CI log visibility
    for doc in dataset["documents"]:
        rated_count = sum(1 for t in doc["tickets"] if t["accuracy_pct"] is not None)
        print(f"  {doc['file']}: {doc['ticket_count']} tickets, {rated_count} rated")


if __name__ == "__main__":
    main()
