from __future__ import annotations

import argparse
import os
import shutil
import tempfile
from pathlib import Path

import uvicorn

from support import BACKEND_ROOT, FIXTURES_ROOT


def prepare_isolated_runtime(temp_root: Path) -> None:
    source_data_dir = BACKEND_ROOT / "data"
    target_data_dir = temp_root / "data"
    target_fixtures_dir = temp_root / "fixtures"
    target_home_dir = temp_root / "home"

    shutil.copytree(source_data_dir, target_data_dir, dirs_exist_ok=True)
    if FIXTURES_ROOT.exists():
        shutil.copytree(FIXTURES_ROOT, target_fixtures_dir, dirs_exist_ok=True)
    target_home_dir.mkdir(parents=True, exist_ok=True)

    os.environ.update(
        {
            "LINGSHU_DATA_DIR": str(target_data_dir),
            "LINGSHU_CODEX_ROOT": str(target_fixtures_dir / "codex"),
            "LINGSHU_CLUDEA_ROOT": str(target_fixtures_dir / "cludea"),
            "LINGSHU_OPENCODE_ROOT": str(target_fixtures_dir / "opencode"),
            "HOME": str(target_home_dir),
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Start the backend for Playwright with isolated test data.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="lingshu-playwright-") as temp_dir:
        prepare_isolated_runtime(Path(temp_dir))
        uvicorn.run("app.main:app", app_dir=str(BACKEND_ROOT), host=args.host, port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
