# -*- mode: python -*-
a = Analysis(['launchcraft.py'],
             pathex=['/home/nikita/code/python/launchcraft'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='launchcraft',
          debug=False,
          strip=None,
          upx=True,
          console=True )
