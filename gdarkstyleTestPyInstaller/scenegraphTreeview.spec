# -*- mode: python -*-

block_cipher = None


a = Analysis(['scenegraphTreeview.py'],
             pathex=['/Users/johan/Dev/pyside/gdarkstyleTestPyInstaller'],
             binaries=None,
             datas=[('scenegraph.xml', 'Resources')],
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
          name='scenegraphTreeview',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='icon.icns')
app = BUNDLE(exe,
             name='scenegraphTreeview.app',
             icon='icon.icns',
             bundle_identifier=None)
