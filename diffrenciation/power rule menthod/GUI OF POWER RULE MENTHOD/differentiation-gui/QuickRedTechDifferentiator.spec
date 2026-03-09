# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = []
hiddenimports += collect_submodules('gui')
hiddenimports += collect_submodules('core')


a = Analysis(
    ['E:\\code base\\differentiation-algorithms-research-1\\diffrenciation\\power rule menthod\\GUI OF POWER RULE MENTHOD\\differentiation-gui\\main.py'],
    pathex=['E:\\code base\\differentiation-algorithms-research-1\\diffrenciation\\power rule menthod\\GUI OF POWER RULE MENTHOD\\differentiation-gui'],
    binaries=[],
    datas=[('E:\\code base\\differentiation-algorithms-research-1\\diffrenciation\\power rule menthod\\GUI OF POWER RULE MENTHOD\\differentiation-gui\\resources', 'resources')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='QuickRedTechDifferentiator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='QuickRedTechDifferentiator',
)
