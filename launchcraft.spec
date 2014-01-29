# -*- mode: python -*-
a = Analysis(['launchcraft.py'],
             pathex=['/mnt/storage/code/python/launchcraft'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

import os

# Fix certifi dependency.
# The certifi directory will be different on Linux and Windows.
cert_path = 'venv'
if os.getenv('APPDATA') is None:
  cert_path = os.path.join(cert_path, 'lib')
else:
  cert_path = os.path.join(cert_path, 'Lib')
cert_path = os.path.join(cert_path, 'python2.7', 'site-packages', 'certifi', 'cacert.pem')
a.datas.append(('cacert.pem', cert_path, 'DATA'))

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
