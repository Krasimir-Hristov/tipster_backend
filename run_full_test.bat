@echo off
echo ========================================
echo Starting Django Server...
echo ========================================
start "Django Server" cmd /k ".\.venv\Scripts\python.exe manage.py runserver"

echo Waiting for server to start...
timeout /t 5 /nobreak

echo.
echo ========================================
echo Running Test: Kosovo vs Slovenia
echo ========================================
.\.venv\Scripts\python.exe test_api.py

echo.
echo ========================================
echo Test Complete!
echo ========================================
echo.
echo The Django server is still running in the other window.
echo Close it manually when done.
pause
