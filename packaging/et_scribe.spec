# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for ET Scribe (Streamlit + Whisper).
# Build on the target OS: Windows → .exe folder; macOS → folder + optional .app/.dmg via scripts.

from pathlib import Path

from PyInstaller.utils.hooks import collect_all, collect_data_files

PKG = Path(SPECPATH).resolve()
ROOT = PKG.parent

datas = [
    (str(ROOT / "et_transcribe.py"), "."),
    (str(ROOT / ".streamlit"), ".streamlit"),
]
binaries = []
hiddenimports = []

try:
    datas += collect_data_files("certifi")
except Exception:
    pass

for pkg in ("streamlit", "altair", "pydeck"):
    try:
        d, b, h = collect_all(pkg)
        datas += d
        binaries += b
        hiddenimports += h
    except Exception:
        pass

hiddenimports += [
    "whisper",
    "tiktoken",
    "torch",
    "torchaudio",
    "numpy",
    "certifi",
]

block_cipher = None

a = Analysis(
    [str(PKG / "run_app.py")],
    pathex=[str(ROOT)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ET-Scribe",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="ET-Scribe",
)
