# -*- mode: python -*-

block_cipher = None


a = Analysis(['marioStylesheet.py'],
             pathex=['/Users/johan/Dev/pyside/petfactoryStylesheetCompile'],
             binaries=None,
             datas=[('scenegraph.xml', '.')],
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
          name='marioStylesheet',
          debug=False,
          strip=False,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='marioStylesheet.app',
             icon='icon.icns',
             bundle_identifier=None)
