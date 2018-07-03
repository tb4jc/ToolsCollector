# ToolsCollecto/setup.py
import sys
import os

from cx_Freeze import setup, Executable

__version__ = "0.1.0"

options = {
    'build_exe': {
        'packages': [],
        'excludes': ["Tkinter", "unittest", "email"],
        'includes': ["atexit"],
        'include_files': ['mainwindow.ui', 'toolsCollector.ini']
    }
}
executables = [Executable("toolsCollector.py", base="Win32GUI")]

setup(name="MCG Release Tool",
    version=__version__,
    author="",
    author_email="",
    requires=["PyQt5"],
    options=options,
    executables=executables)
