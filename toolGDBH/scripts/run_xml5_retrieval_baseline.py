from __future__ import annotations

import json
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared" / "types"))
sys.path.insert(0, str(ROOT / "shared"))
sys.path.insert(0, str(ROOT / "modules" / "evidence-service" / "src"))

from evidence_service import EvidenceRetrievalService


def resolve_path_from_env(env_name: str, fallback_candidates: list[Path]) -> Path | None:
    raw_value = os.getenv(env_name, "").strip()
    if raw_value:
        return Path(raw_value)
    for candidate in fallback_candidates:
        if candidate.exists():
            return candidate
    return None


def main() -> int:
    default_query_file = resolve_path_from_env(
        "TOOLGDBH_QUERY_JSONL",
        [ROOT / "runtime" / "knowledge-base" / "queries" / "xml5_note_records.queries.jsonl"],
    )
    default_chunks_file = resolve_path_from_env(
        "TOOLGDBH_CHUNKS_JSONL",
        [ROOT / "runtime" / "knowledge-base" / "chunks" / "xml5_note_records.chunks.jsonl"],
    )
    default_output_file = ROOT / "runtime" / "knowledge-base" / "retrieval" / "xml5_note_records.retrieval.jsonl"

    query_file = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else default_query_file
    chunks_file = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else default_chunks_file
    output_file = Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else default_output_file.resolve()

    if query_file is None or not query_file.exists():
        print("Query jsonl not found.")
        return 1
    if chunks_file is None or not chunks_file.exists():
        print("Chunks jsonl not found.")
        return 1

    service = EvidenceRetrievalService()
    results = service.export_results(query_file, chunks_file, output_file, top_k=5)
    print(
        json.dumps(
            {
                "query_file": str(query_file),
                "chunks_file": str(chunks_file),
                "output_file": str(output_file),
                "query_count": len(results),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
