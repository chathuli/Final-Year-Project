@echo off
echo ========================================
echo RESTARTING SERVER WITH NEW CHANGES
echo ========================================
echo.
echo Step 1: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 2: Checking if server is running...
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Server is running. Stopping it...
    taskkill /F /IM python.exe /T 2>NUL
    timeout /t 2 /nobreak >NUL
    echo Server stopped.
) else (
    echo No server running.
)

echo.
echo Step 3: Starting server with new changes...
echo.
echo ========================================
echo SERVER STARTING...
echo ========================================
echo.
echo The password change endpoint is now available!
echo Test it at: http://localhost:5000/profile
echo.
python src\app.py

pause
