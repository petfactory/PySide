# -*- mode: python -*-

block_cipher = None


a = Analysis(['png_comp.py'],
             pathex=['/Users/johan/Dev/pyside/png_comp'],
             binaries=None,
             datas=[('assets/01 bg/bg.png', './assets/01 bg/'),
                    ('assets/02 body/body_1.png', './assets/02 body/'),
                    ('assets/02 body/body_2.png', './assets/02 body/'),
                    ('assets/02 body/body_3.png', './assets/02 body/'),
                    ('assets/03 wheels/wheels_1.png', './assets/03 wheels/'),
                    ('assets/03 wheels/wheels_2.png', './assets/03 wheels/'),
                    ('assets/03 wheels/wheels_3.png', './assets/03 wheels/'),
                    ('up_arrow.png', '.'),
                    ('down_arrow.png', '.'),
                    ('open_dir.png', '.')],
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
             icon='icon.icns',
             bundle_identifier=None)
