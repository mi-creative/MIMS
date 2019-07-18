# -*- mode: python -*-

block_cipher = None


a = Analysis(['MIMS_main.py'],
             pathex=['C:\\Users\\leonarja\\devel\\MIMS'],
             binaries=[],
             datas=[],
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
          name='MIMS',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
		  
		  
added_files = [
         ( '/mygame/data', 'data' ),
         ( '/mygame/sfx/*.mp3', 'sfx' ),
         ( 'src/README.txt', '.' )
         ]
