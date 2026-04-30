@echo off
echo ========================================
echo FORCE RESTARTING SERVER
echo ========================================
echo.

echo Killing all Python processes...
taskkill /F /IM python.exe /T >nul 2>&1

echo Waiting 3 seconds...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo STARTING SERVER WITH NEW CODE
echo ========================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat

echo Starting Flask server...
echo.
echo ========================================
echo SERVER IS STARTING...
echo ========================================
echo.
echo Password change endpoint is now active!
echo.
echo Login credentials:
echo   Username: Amaraweera
echo   Password: password123
echo.
echo   OR
echo.
echo   Username: admin
echo   Password: admin123
echo.
echo ========================================
echo.

python src\app.py

pause
