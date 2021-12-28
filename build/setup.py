import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["encodings"], "excludes": []}

if sys.platform == "win32":
    build_exe_options["excludes"] = ["readline"]

setup(
    name = "unv",
    version = "0.0.1",
    description = "Unv command line tool",
    options = {"build_exe": build_exe_options},
    executables = [Executable("unv.py", base=None)]
)
