"""
Launcher for the frozen ET Scribe desktop build (PyInstaller).
Run from source: python packaging/run_app.py
"""
from __future__ import annotations

import multiprocessing
import os
import sys
from pathlib import Path


def _prepend_bundled_ffmpeg() -> None:
    roots = []
    br = os.environ.get("ET_BUNDLE_ROOT")
    if br:
        roots.append(Path(br).resolve())
    if getattr(sys, "frozen", False):
        roots.append(Path(sys.executable).resolve().parent)
    for base in roots:
        for d in (base, base / "bin"):
            if any((d / n).exists() for n in ("ffmpeg", "ffmpeg.exe")):
                os.environ["PATH"] = str(d) + os.pathsep + os.environ.get("PATH", "")
                return


def main() -> None:
    multiprocessing.freeze_support()
    _prepend_bundled_ffmpeg()

    if getattr(sys, "frozen", False):
        app_path = Path(sys._MEIPASS) / "et_transcribe.py"
    else:
        root = Path(__file__).resolve().parent.parent
        app_path = root / "et_transcribe.py"

    os.environ.setdefault("STREAMLIT_TELEMETRY_OPT_OUT", "1")

    port = os.environ.get("ET_PORT", "8501")
    from streamlit.web import cli as stcli

    sys.argv = [
        "streamlit",
        "run",
        str(app_path),
        "--global.developmentMode=false",
        "--server.port",
        port,
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
    ]
    raise SystemExit(stcli.main())


if __name__ == "__main__":
    main()
