import sys
from cx_Freeze import setup, Executable
import os

build_exe_options = {"packages": ["pygame", "fenrir", "db"], "excludes": ["tkinter"],
                     'include_files': [os.path.join(sys.base_prefix, 'DLLs', 'sqlite3.dll')]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="fenrir",
    version="1.0",
    description="A fantasy turn-based role-playing game",
    options={"build_exe": build_exe_options},
    executables=[Executable("projectfen.py",
                            base=base,
                            target_name="Project Fenrir",
                            icon="icon.ico")]
)
