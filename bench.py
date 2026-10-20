"""Run the same Arabic and English prompts against a model and log the results.

Useful before a workshop or hackathon: check that the model answers in the right
language, see how long people will wait, and keep a record to compare models.

    python bench.py                 # uses prompts.json, writes results_<model>.csv
    LLM_MODEL=qwen2.5:7b python bench.py
"""
import csv
import json
import re
import sys
from pathlib import Path

from chat import MODEL, answer_text, chat

ARABIC = re.compile(r"[؀-ۿ]")


def language_of(text: str) -> str:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return "unknown"
    share = sum(1 for c in letters if ARABIC.match(c)) / len(letters)
    return "ar" if share > 0.5 else "en"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    here = Path(__file__).parent
    prompts = json.loads((here / "prompts.json").read_text(encoding="utf-8"))
    rows = []
    for item in prompts:
        data = chat(item["prompt"])
        reply = answer_text(data)
        rows.append({
            "model": MODEL,
            "id": item["id"],
            "asked_in": item["lang"],
            "answered_in": language_of(reply),
            "latency_s": data["_latency_s"],
            "output_tokens": data.get("usage", {}).get("completion_tokens", ""),
            "reply_start": reply.replace("\n", " ")[:90],
        })
        row = rows[-1]
        ok = "ok " if row["asked_in"] == row["answered_in"] else "MISMATCH"
        print(f"{ok} {row['id']:<14} {row['latency_s']:>6} s  {row['reply_start'][:60]}")

    out = here / f"results_{re.sub(r'[^A-Za-z0-9.]+', '_', MODEL)}.csv"
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    matched = sum(r["asked_in"] == r["answered_in"] for r in rows)
    avg = sum(r["latency_s"] for r in rows) / len(rows)
    print(f"\n{matched}/{len(rows)} answered in the language asked; "
          f"average latency {avg:.2f} s; saved {out.name}")


if __name__ == "__main__":
    main()
