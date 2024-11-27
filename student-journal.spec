# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/student_journal/bootstrap/entrypoint/qt.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('src/student_journal/adapters/db/schema/schema.sql', 'student_journal/adapters/db/schema/'),
    ('src/student_journal/presentation/resource/', 'student_journal/presentation/resource/'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ДневникШкольника',
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
    icon="src/student_journal/presentation/resource/favicon.ico",
)
