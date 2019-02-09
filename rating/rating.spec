# -*- mode: python -*-

from PyInstaller.utils.hooks import collect_data_files

w = collect_data_files('weasyprint')
ww = []
for k,v in w:
	try:
		ww.append((k, v.split('weasyprint/')[1]))
	except IndexError:
		pass

added_files += ww
added_files += collect_data_files('pyphen')
extra_imports = ['pyphen', 'weasyprint']


a = Analysis(['C:\\Users\\ivand\\Desktop\\rating\\run.py'],
             pathex=['C:\\Users\\ivand\\Desktop\\rating\\main_app', 'C:\\Users\\ivand\\Desktop\\rating'],
             binaries=[],
             datas=added_files,
             hiddenimports=extra_imports,
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
          name='rating',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='icon.ico')
