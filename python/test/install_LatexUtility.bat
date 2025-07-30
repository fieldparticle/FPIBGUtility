rmdir dist /S /Q
rmdir build /S /Q
pip3 install --upgrade PyInstaller pyinstaller-hooks-contrib
pyinstaller --clean --paths=.:J:/MOD/FPIBGUtility/python:J:/MOD/FPIBGUtility/python/test:J:/MOD/FPIBGUtility/python/shared --onefile  main_LatexUtility.py
rem pyinstaller --debug=imports --paths J:/MOD/FPIBGUtility/python:J:/MOD/FPIBGUtility/python/test:J:/MOD/FPIBGUtility/python/shared --onefile --windowed python/test/main_LatexUtility.py
copy ..\..\ParticleJB.cfg dist
pause