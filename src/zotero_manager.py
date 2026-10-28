#!/usr/bin/env python3
"""Simple Zotero export organizer for BibTeX and RIS files."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List

import bibtexparser


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATEGORIES = ROOT / "categories.json"
DEFAULT_OUTPUT = ROOT / "output" / "zotero_clean.csv"


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = re.sub(r"[{}]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def normalize_doi(value: str | None) -> str:
    doi = clean_text(value).lower()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
    doi = re.sub(r"^doi:\s*", "", doi)
    return doi.strip()


def normalize_title(value: str | None) -> str:
    title = clean_text(value).lower()
    title = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", title)
    return title


def parse_bib(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8") as f:
        db = bibtexparser.load(f)

    items: List[Dict[str, str]] = []
    for entry in db.entries:
        items.append(
            {
                "title": clean_text(entry.get("title")),
                "authors": clean_text(entry.get("author")),
                "year": clean_text(entry.get("year")),
                "journal": clean_text(
                    entry.get("journal")
                    or entry.get("booktitle")
                    or entry.get("publisher")
                ),
                "doi": normalize_doi(entry.get("doi")),
                "keywords": clean_text(entry.get("keywords") or entry.get("keyword")),
                "abstract": clean_text(entry.get("abstract")),
            }
        )
    return items


RIS_MAP = {
    "TI": "title",
    "T1": "title",
    "AU": "authors",
    "A1": "authors",
    "PY": "year",
    "Y1": "year",
    "JO": "journal",
    "JF": "journal",
    "T2": "journal",
    "DO": "doi",
    "KW": "keywords",
    "AB": "abstract",
    "N2": "abstract",
}


def parse_ris(path: Path) -> List[Dict[str, str]]:
    records: List[Dict[str, str]] = []
    current: Dict[str, List[str]] = {}

    def flush() -> None:
        nonlocal current
        if not current:
            return

        item = {
            "title": clean_text(" ".join(current.get("title", []))),
            "authors": clean_text("; ".join(current.get("authors", []))),
            "year": clean_text(" ".join(current.get("year", [])))[:4],
            "journal": clean_text(" ".join(current.get("journal", []))),
            "doi": normalize_doi(" ".join(current.get("doi", []))),
            "keywords": clean_text("; ".join(current.get("keywords", []))),
            "abstract": clean_text(" ".join(current.get("abstract", []))),
        }
        if item["title"] or item["doi"]:
            records.append(item)
        current = {}

    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if raw.startswith("ER  -"):
            flush()
            continue
        match = re.match(r"^([A-Z0-9]{2})\s{2}-\s?(.*)$", raw)
        if not match:
            continue
        tag, value = match.groups()
        field = RIS_MAP.get(tag)
        if field:
            current.setdefault(field, []).append(value.strip())

    flush()
    return records


def load_categories(path: Path) -> Dict[str, List[str]]:
    return json.loads(path.read_text(encoding="utf-8"))


def classify(item: Dict[str, str], rules: Dict[str, List[str]]) -> str:
    haystack = " ".join(
        [
            item.get("title", ""),
            item.get("keywords", ""),
            item.get("abstract", ""),
            item.get("journal", ""),
        ]
    ).lower()

    scored: List[tuple[int, str]] = []
    for category, terms in rules.items():
        if category == "Other":
            continue
        score = sum(1 for term in terms if term.lower() in haystack)
        if score:
            scored.append((score, category))

    if not scored:
        return "Other"

    scored.sort(reverse=True)
    return scored[0][1]


def mark_duplicates(items: List[Dict[str, str]]) -> None:
    counts: Dict[str, int] = {}
    for item in items:
        doi = normalize_doi(item.get("doi"))
        title_key = normalize_title(item.get("title"))
        key = f"doi:{doi}" if doi else f"title:{title_key}"
        item["duplicate_key"] = key
        if key not in {"doi:", "title:"}:
            counts[key] = counts.get(key, 0) + 1

    for item in items:
        key = item["duplicate_key"]
        item["possible_duplicate"] = "YES" if counts.get(key, 0) > 1 else ""


def load_items(path: Path) -> List[Dict[str, str]]:
    suffix = path.suffix.lower()
    if suffix == ".bib":
        return parse_bib(path)
    if suffix == ".ris":
        return parse_ris(path)
    raise ValueError("Only .bib and .ris files are supported.")


def write_csv(items: Iterable[Dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "title",
        "authors",
        "year",
        "journal",
        "doi",
        "keywords",
        "category",
        "duplicate_key",
        "possible_duplicate",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(items)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Organize Zotero BibTeX/RIS exports."
    )
    parser.add_argument("input", type=Path, help="Input .bib or .ris file")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output CSV (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--categories",
        type=Path,
        default=DEFAULT_CATEGORIES,
        help="JSON category rule file",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Input file not found: {args.input}")

    items = load_items(args.input)
    rules = load_categories(args.categories)

    for item in items:
        item["category"] = classify(item, rules)

    mark_duplicates(items)
    write_csv(items, args.output)

    duplicates = sum(1 for x in items if x["possible_duplicate"] == "YES")
    print(f"Processed: {len(items)} records")
    print(f"Possible duplicate records: {duplicates}")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()
