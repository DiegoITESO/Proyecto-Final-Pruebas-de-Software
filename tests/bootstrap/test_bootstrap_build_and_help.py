"""Smoke de arranque: asegura que se puede obtener ``logistic_churn`` y que ``--help`` funciona."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tests.integration._helpers import ROOT, binary_exists, cli_subprocess_env, run_cli


def _cpp_sources() -> list[Path]:
    return [ROOT / "main.cpp", *sorted(ROOT.glob("src/**/*.cpp"))]


def _binary_name() -> str:
    return "logistic_churn.exe" if sys.platform == "win32" else "logistic_churn"


def _try_make() -> bool:
    env = cli_subprocess_env()
    path = env.get("PATH")
    make = shutil.which("make", path=path) or shutil.which("mingw32-make", path=path)
    if make is None:
        return False
    try:
        subprocess.run(
            [make, "main"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
            env=cli_subprocess_env(),
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False
    return binary_exists()


def _find_gpp() -> str | None:
    env = cli_subprocess_env()
    path = env.get("PATH")
    return shutil.which("g++", path=path) or shutil.which("c++", path=path)


def _try_gpp_direct() -> bool:
    gpp = _find_gpp()
    if gpp is None:
        return False
    out = ROOT / _binary_name()
    cmd = [
        gpp,
        "-g",
        "-std=c++20",
        "-Wall",
        "-Iinclude",
        "-o",
        str(out),
        *[str(p) for p in _cpp_sources()],
    ]
    try:
        subprocess.run(
            cmd,
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
            env=cli_subprocess_env(),
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False
    return binary_exists()


def _try_powershell_build() -> bool:
    if sys.platform != "win32":
        return False
    script = ROOT / "build.ps1"
    if not script.is_file():
        return False
    ps = shutil.which("powershell") or shutil.which("pwsh")
    if ps is None:
        return False
    try:
        subprocess.run(
            [ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
            env=cli_subprocess_env(),
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False
    return binary_exists()


def _ensure_binary() -> None:
    if binary_exists():
        return
    if _try_make() or _try_powershell_build() or _try_gpp_direct():
        return
    pytest.skip(
        "No se pudo compilar: instala g++/make (Linux/macOS, WSL) o MSYS2 y ejecuta "
        "`build.ps1` / `make` en la raíz del repo, o define LOGISTIC_CHURN_PATH."
    )


def test_build_or_existing_binary_and_help_smoke() -> None:
    """Compila si falta el ejecutable y comprueba que ``--help`` termina en 0."""
    _ensure_binary()
    proc = run_cli(["--help"], "", timeout=60)
    assert proc.returncode == 0
    assert "Customer Churn Predictor" in (proc.stdout or "")
