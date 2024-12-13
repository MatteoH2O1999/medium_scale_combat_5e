# -*- mode: python ; coding: utf-8 -*-
import sys

block_cipher = None

executable_name = 'Datasheet generator'

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[("src/resources/*", "resources")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=executable_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="src/resources/icon.ico"
)

if sys.platform == 'darwin':
    app = BUNDLE(exe,
        name=f'{executable_name}.app',
        icon="src/resources/icon.icns",
        bundle_identifier=None
    )
