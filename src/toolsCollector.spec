# -*- mode: python -*-

block_cipher = None


a = Analysis(['toolscollector.py'],
             pathex=['c:\\Users\\Thomas\\Development\\python\\ToolsCollector\\src\\releasescripts', 'c:\\Users\\Thomas\\Development\\python\\ToolsCollector\\src'],
             binaries=[],
             datas=[('mainwindow.ui', '.'), ('toolsCollector.ini', '.'), ('batch_files', 'batch_files')],
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
          [],
          exclude_binaries=True,
          name='ToolsCollector',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='ToolsCollector')
