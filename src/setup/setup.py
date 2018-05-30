# testgui/setup.py
from cx_Freeze import setup, Executable


__version__ = "0.0.0"

options = dict(
    build_exe=dict(
        packages=[],
        excludes=["Tkinter"],
        includes=["atexit"]
    )
)
executables = [Executable("testgui.py", base="Win32GUI")]

setup(name="TestGui",
    version=__version__,
    author="",
    author_email="",
    requires=["PyQt5"],
    options=options,
    executables=executables)
