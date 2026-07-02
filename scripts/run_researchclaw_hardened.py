from __future__ import annotations

import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    repo_root = _repo_root()
    arc_root = repo_root / "external" / "AutoResearchClaw"
    if arc_root.is_dir():
        sys.path.insert(0, str(arc_root))

    from arc_literature_hardening import apply as apply_literature_hardening
    from arc_stage04_resilience import apply as apply_stage04_resilience
    from arc_stage_gate_guard import apply as apply_stage_gate_guard

    apply_literature_hardening()
    apply_stage04_resilience()
    apply_stage_gate_guard()

    from researchclaw.cli import main as researchclaw_main

    return int(researchclaw_main(argv))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
