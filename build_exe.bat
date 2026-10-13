@echo off
python -m pip install -r requirements.txt pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --windowed --name ADDT_Research_Preview app.py
pause
