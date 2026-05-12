"""Shared helpers for Python integration tests against the ``logistic_churn`` binary."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _find_binary() -> Path | None:
    """Resolve the CLI executable (env override, then common names at repo root)."""
    env_path = os.environ.get("LOGISTIC_CHURN_PATH", "").strip()
    if env_path:
        p = Path(env_path).expanduser()
        if p.is_file():
            return p
    for name in ("logistic_churn.exe", "logistic_churn"):
        candidate = ROOT / name
        if candidate.is_file():
            return candidate
    return None


def binary_exists() -> bool:
    return _find_binary() is not None


def binary_path() -> Path:
    """Path to the CLI; only call when ``binary_exists()`` is true."""
    found = _find_binary()
    if found is None:
        raise RuntimeError(
            "logistic_churn not found at repo root; build with make, build.ps1, or build.sh"
        )
    return found


def cli_subprocess_env() -> dict[str, str]:
    """Environment for subprocesses (MSYS2 ``bin`` on PATH on Windows so MinGW DLLs load)."""
    env = os.environ.copy()
    if sys.platform == "win32":
        drive = os.environ.get("SYSTEMDRIVE", "C:")
        for bindir in (
            Path(r"C:\msys64\ucrt64\bin"),
            Path(r"C:\msys64\mingw64\bin"),
            Path(drive) / "msys64" / "ucrt64" / "bin",
        ):
            if (bindir / "g++.exe").is_file():
                env["PATH"] = str(bindir) + os.pathsep + env.get("PATH", "")
                break
    return env


def run_cli(argv: list[str], stdin: str, *, cwd: Path | None = None, timeout: float = 120.0):
    """Run the CLI with given argv (after executable) and scripted stdin."""
    cmd = [str(binary_path()), *argv]
    return subprocess.run(
        cmd,
        input=stdin,
        text=True,
        capture_output=True,
        cwd=str(cwd or ROOT),
        timeout=timeout,
        env=cli_subprocess_env(),
    )


def churn_labeled_csv(rows: int = 36) -> str:
    """Build a CSV with header f1,f2,churn and yes/no labels (churn column index 2)."""
    lines = ["f1,f2,churn"]
    for i in range(rows):
        f1 = (i % 4) * 0.25
        f2 = ((i * 3) % 5) * 0.2
        churn = "yes" if (i + int(f1 * 10)) % 4 == 0 else "no"
        lines.append(f"{f1},{f2},{churn}")
    return "\n".join(lines) + "\n"


def features_only_csv(rows: int = 8) -> str:
    """CSV for prediction: same numeric features, no churn column."""
    lines = ["f1,f2"]
    for i in range(rows):
        lines.append(f"{(i % 4) * 0.25},{((i * 3) % 5) * 0.2}")
    return "\n".join(lines) + "\n"


def train_stdin(
    csv_path: str,
    out_path: str,
    *,
    header_y: bool = True,
    churn_idx: int = 2,
    drops: str = "",
    alpha: float = 0.08,
    epochs: int = 40,
) -> str:
    """Script stdin for ``collectTrainData`` (drops line uses getline after churn index)."""
    yn = "y" if header_y else "n"
    return f"{csv_path}\n{out_path}\n{yn}\n{churn_idx}\n{drops}\n{alpha}\n{epochs}\n"


def predict_stdin(
    weights: str, data_csv: str, out_csv: str, *, header_y: bool = True, drops: str = ""
) -> str:
    """Script stdin for ``collectPredictData`` (weights, dataset, output, header, drops line)."""
    yn = "y" if header_y else "n"
    return f"{weights}\n{data_csv}\n{out_csv}\n{yn}\n{drops}\n"
