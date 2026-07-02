from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger(__name__)


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _stage05_blocks_stage06(run_dir: Path) -> bool:
    stage05_decision = _read_json(run_dir / "stage-05" / "decision.json")
    status = str(stage05_decision.get("status", "")).lower()
    decision = str(stage05_decision.get("decision", "")).lower()
    return status == "blocked_approval" or decision == "block"


def _write_stage06_guard_failure(run_dir: Path, run_id: str, result: Any) -> None:
    stage_dir = run_dir / "stage-06"
    ts = _utcnow_iso()
    decision = {
        "stage_id": "06-knowledge_extract",
        "run_id": run_id,
        "status": result.status.value,
        "decision": result.decision,
        "output_artifacts": list(result.artifacts),
        "evidence_refs": list(result.evidence_refs),
        "error": result.error,
        "ts": ts,
        "next_stage": 6,
    }
    health = {
        "stage_id": "06-knowledge_extract",
        "run_id": run_id,
        "duration_sec": 0.0,
        "status": result.status.value,
        "artifacts_count": len(result.artifacts),
        "error": result.error,
        "timestamp": ts,
    }
    _write_json(stage_dir / "decision.json", decision)
    _write_json(stage_dir / "stage_health.json", health)


def apply() -> None:
    from researchclaw.pipeline import executor
    from researchclaw.pipeline._helpers import StageResult
    from researchclaw.pipeline.stages import Stage, StageStatus

    if getattr(executor, "_arp_stage_gate_guard_applied", False):
        return

    original_execute_stage: Callable[..., Any] = executor.execute_stage

    def guarded_execute_stage(stage: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            stage_value = Stage(stage)
        except (TypeError, ValueError):
            stage_value = stage

        if stage_value == Stage.KNOWLEDGE_EXTRACT:
            run_dir_arg = kwargs.get("run_dir")
            run_id = str(kwargs.get("run_id", ""))
            if run_dir_arg is not None:
                run_dir = Path(run_dir_arg)
                if _stage05_blocks_stage06(run_dir):
                    error = (
                        "Stage 6 blocked: Stage 5 is still awaiting approval "
                        "(stage-05 decision status is blocked_approval). "
                        "Approve or rerun Stage 5 before knowledge extraction."
                    )
                    result = StageResult(
                        stage=Stage.KNOWLEDGE_EXTRACT,
                        status=StageStatus.FAILED,
                        artifacts=(),
                        error=error,
                        decision="blocked_by_stage05_approval",
                        evidence_refs=("stage-05/decision.json",),
                    )
                    _write_stage06_guard_failure(run_dir, run_id, result)
                    logger.warning(error)
                    return result

        return original_execute_stage(stage, *args, **kwargs)

    executor._arp_stage_gate_guard_original_execute_stage = original_execute_stage
    executor.execute_stage = guarded_execute_stage

    runner_mod = sys.modules.get("researchclaw.pipeline.runner")
    if runner_mod is not None:
        runner_mod.execute_stage = guarded_execute_stage

    executor._arp_stage_gate_guard_applied = True
    logger.debug("ARC Stage 5/6 gate guard applied")
