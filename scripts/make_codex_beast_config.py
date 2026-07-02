from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Config root must be a mapping: {path}")
    return data


def enable_codex_beast(data: dict[str, Any]) -> dict[str, Any]:
    experiment = data.setdefault("experiment", {})
    if not isinstance(experiment, dict):
        raise ValueError("experiment must be a mapping")

    opencode = experiment.setdefault("opencode", {})
    if not isinstance(opencode, dict):
        raise ValueError("experiment.opencode must be a mapping")

    opencode["enabled"] = True
    opencode["auto"] = True
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            "Usage: python scripts/make_codex_beast_config.py "
            "<input_config> <output_config>",
            file=sys.stderr,
        )
        return 2

    input_path = Path(argv[0]).expanduser().resolve()
    output_path = Path(argv[1]).expanduser().resolve()

    try:
        data = enable_codex_beast(load_yaml(input_path))
        write_yaml(output_path, data)
    except (FileNotFoundError, OSError, ValueError, yaml.YAMLError) as exc:
        print(f"Failed to write Codex Beast config: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
