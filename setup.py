import os
import sys
from cx_Freeze import setup, Executable

diretorio_script = os.path.dirname(os.path.realpath(__file__))
caminho_icone = os.path.join(diretorio_script, 'Assets', 'icon.ico')
#Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "includes": ["os","sqlite3","pandas","openpyxl","xlsxwriter"]}

#GUI applications require a different base on Windows (the default is for
#a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Sod Solutions",
    version="0.1",
    description="",
    options={"build_exe": build_exe_options},
    executables=[Executable("interface.py", base=base, icon=caminho_icone)]
)