@echo off
:: Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Install dependencies from requirements.txt
echo Installing dependencies...
pip install -r requirements.txt

:: Wait for user to press any key before closing
echo.
echo Done install dependencies Press any key to close...
pause >nul
