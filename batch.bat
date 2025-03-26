@echo off
:: Install dependencies from requirements.txt
echo Installing dependencies...
pip install -r requirements.txt

:: Run the Python script
echo Running translate_script.py...
python translate_script.py

:: Pause to keep the terminal open (optional)
pause
