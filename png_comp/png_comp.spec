# -*- mode: python -*-

block_cipher = None


a = Analysis(['png_comp.py'],
             pathex=['/Users/johan/Dev/pyside/png_comp'],
             binaries=None,
             datas=[('blue.png', '.'),
                    ('green.png', '.'),
                    ('red.png', '.')],
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
          name='png_comp',
          debug=False,
          strip=False,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='png_comp.app',
             icon=None,
             bundle_identifier=None)
