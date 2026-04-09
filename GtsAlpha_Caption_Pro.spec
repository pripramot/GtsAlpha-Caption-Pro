# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for GtsAlpha Caption Pro
# Run:  pyinstaller GtsAlpha_Caption_Pro.spec

block_cipher = None

a = Analysis(
    ['src/GtsAlpha_Caption_Pro_Thai_Final.py'],
    pathex=['src'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'gtsalpha',
        'gtsalpha.__main__',
        'gtsalpha.core',
        'gtsalpha.core.caption',
        'gtsalpha.core.downloader',
        'gtsalpha.core.summarizer',
        'gtsalpha.core.translator',
        'gtsalpha.core.tts',
        'gtsalpha.gui',
        'gtsalpha.gui.app',
        'gtsalpha.gui.theme',
        'gtsalpha.gui.widgets',
        'gtsalpha.utils',
        'gtsalpha.utils.config',
        'gtsalpha.utils.url_parser',
        'yt_dlp',
        'youtube_transcript_api',
        'deep_translator',
        'gtts',
        'requests',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'tkinter.filedialog',
    ],
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
    name='GtsAlpha_Caption_Pro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # ไม่เปิดหน้าต่าง Console (GUI เท่านั้น)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,              # ใส่ path ไอคอน .ico ได้ที่นี่ เช่น 'assets/icon.ico'
)
