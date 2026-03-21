from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any
from urllib import error, request


BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent
FIXTURES_ROOT = Path(__file__).resolve().parent / "fixtures"
DEFAULT_DATA_FILES = sorted((BACKEND_ROOT / "data").rglob("*.json"))


def choose_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return int(sock.getsockname()[1])


def snapshot_default_data() -> dict[str, str]:
    return {str(path.relative_to(REPO_ROOT)): path.read_text(encoding="utf-8") for path in DEFAULT_DATA_FILES}


class BackendServerHarness:
    def __init__(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="lingshu-api-regression-"))
        self.data_dir = self.temp_dir / "data"
        self.fixtures_dir = self.temp_dir / "fixtures"
        self.port = choose_free_port()
        self.process: subprocess.Popen[str] | None = None
        self.default_data_snapshot = snapshot_default_data()
        self._seed_default_data()
        self._seed_fixture_roots()

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.port}/api"

    def start(self) -> None:
        command = [
            str(BACKEND_ROOT / ".venv" / "bin" / "python"),
            "-m",
            "uvicorn",
            "app.main:app",
            "--app-dir",
            str(BACKEND_ROOT),
            "--host",
            "127.0.0.1",
            "--port",
            str(self.port),
        ]
        self.process = subprocess.Popen(
            command,
            cwd=str(REPO_ROOT),
            env=self._server_env(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self._wait_for_server()

    def stop(self) -> None:
        if self.process is not None:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=5)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def request_json(self, method: str, path: str, payload: dict[str, Any] | None = None) -> tuple[int, Any]:
        body: bytes | None = None
        headers = {"Accept": "application/json"}
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=True).encode("utf-8")
            headers["Content-Type"] = "application/json"

        http_request = request.Request(
            url=f"{self.base_url}{path}",
            data=body,
            headers=headers,
            method=method,
        )
        try:
            with request.urlopen(http_request, timeout=5) as response:
                raw = response.read().decode("utf-8")
                return response.status, json.loads(raw) if raw else {}
        except error.HTTPError as exc:
            raw = exc.read().decode("utf-8")
            return exc.code, json.loads(raw) if raw else {}

    def assert_default_data_unchanged(self) -> None:
        current_snapshot = snapshot_default_data()
        if current_snapshot != self.default_data_snapshot:
            raise AssertionError("Official backend/data JSON files were modified by tests")

    def _seed_default_data(self) -> None:
        for source in DEFAULT_DATA_FILES:
            relative_path = source.relative_to(BACKEND_ROOT / "data")
            target = self.data_dir / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    def _seed_fixture_roots(self) -> None:
        if FIXTURES_ROOT.exists():
            shutil.copytree(FIXTURES_ROOT, self.fixtures_dir, dirs_exist_ok=True)

    def _server_env(self) -> dict[str, str]:
        env = os.environ.copy()
        env.update(
            {
                "LINGSHU_DATA_DIR": str(self.data_dir),
                "LINGSHU_CODEX_ROOT": str(self.fixtures_dir / "codex"),
                "LINGSHU_CLUDEA_ROOT": str(self.fixtures_dir / "cludea"),
                "LINGSHU_OPENCODE_ROOT": str(self.fixtures_dir / "opencode"),
                "HOME": str(self.temp_dir / "home"),
            }
        )
        return env

    def _wait_for_server(self) -> None:
        deadline = time.time() + 20
        last_error = ""
        while time.time() < deadline:
            if self.process is not None and self.process.poll() is not None:
                stderr = self.process.stderr.read() if self.process.stderr else ""
                stdout = self.process.stdout.read() if self.process.stdout else ""
                raise RuntimeError(f"uvicorn exited early\nstdout:\n{stdout}\nstderr:\n{stderr}")
            try:
                status, payload = self.request_json("GET", "/health")
                if status == 200 and payload.get("status") == "ok":
                    return
            except Exception as exc:  # pragma: no cover
                last_error = str(exc)
            time.sleep(0.2)
        raise RuntimeError(f"Timed out waiting for test server: {last_error}")
