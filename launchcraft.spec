# -*- mode: python -*-
a = Analysis(['launchcraft.py'],
             pathex=['/mnt/storage/code/python/launchcraft', '/mnt/storage/code/python/launchcraft/lib/site-packages'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

# Fix certifi dependency.
a.datas.append(('cacert.pem', 'venv/lib/python2.7/site-packages/certifi/cacert.pem', 'DATA'))

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts + [('O','','OPTION')],
          a.binaries,
          a.zipfiles,
          a.datas,
          name='launchcraft',
          debug=False,
          strip=None,
          upx=True,
          console=True )
