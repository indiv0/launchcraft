# -*- mode: python -*-
VERSION = '1.0.4'
NAME = 'launchcraft-{}'.format(VERSION)

if os.name == 'nt':
  NAME += '.exe'

a = Analysis(['launchcraft.py'],
             pathex=['/mnt/storage/code/python/launchcraft'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

# Fix certifi dependency.
# The certifi directory will be different on Linux and Windows.
cert_path = 'venv'
if os.getenv('APPDATA') is None:
  cert_path = os.path.join(cert_path, 'lib', 'python2.7')
else:
  cert_path = os.path.join(cert_path, 'Lib')
cert_path = os.path.join(cert_path, 'site-packages', 'certifi', 'cacert.pem')
a.datas.append(('cacert.pem', cert_path, 'DATA'))

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts + [('O','','OPTION')],
          a.binaries,
          a.zipfiles,
          a.datas,
          name=NAME,
          debug=False,
          strip=None,
          upx=True,
          console=True,
          icon='launchcraft.ico')
app = BUNDLE(exe,
          name=NAME,
          console=True,
          icon='launchcraft.ico')
