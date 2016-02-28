# -*- mode: python -*-

block_cipher = None


a = Analysis(['test.py'],
             pathex=['/Users/johan/Dev/pyside/testPyInstaller'],
             binaries=None,
             datas=[ ('./logo.jpg', '.') ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='test',
          debug=False,
          strip=False,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='test.app',
             icon=None,
             bundle_identifier=None)
