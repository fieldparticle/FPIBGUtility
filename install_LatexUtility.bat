rmdir dist /S /Q
rmdir build /S /Q
pip3 install --upgrade PyInstaller pyinstaller-hooks-contrib
pyinstaller --clean --hidden-import FPIBGMainWin --paths=.:J:/MOD/FPIBGUtility/python:J:/MOD/FPIBGUtility/python/test:J:/MOD/FPIBGUtility/python/shared --debug=imports  --windowed --onefile  python/test/main_LatexUtility.py
rem pyinstaller --debug=imports --paths J:/MOD/FPIBGUtility/python:J:/MOD/FPIBGUtility/python/test:J:/MOD/FPIBGUtility/python/shared --onefile --windowed python/test/main_LatexUtility.py
pause