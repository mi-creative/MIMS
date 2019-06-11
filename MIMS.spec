# -*- mode: python -*-

block_cipher = None

added_files = [
         ( 'style', 'style/' ),
         ( 'ui/', 'ui' ),
         ( 'html/', 'html' ),
         ( 'icons/', 'icons' ),
         ( 'mdls/', 'mdls' )
         ]


a = Analysis(['MIMS_main.py'],
             pathex=['C:\\Users\\leonarja\\devel\\MIMS'],
             binaries=[],
             datas= added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='MassInteraction_ModelScripter',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )


app = BUNDLE(exe,
         name='myscript.app',
         icon=None,
         bundle_identifier=None)
