@echo off
REM Test The Odds API Integration
echo ======================================================================
echo Starting Django Server...
echo ======================================================================
start "Django Server" cmd /k "D:\myProjects\tipster_backend\.venv\Scripts\python.exe manage.py runserver"

echo Waiting for server to start...
timeout /t 5 /nobreak

echo.
echo ======================================================================
echo TEST 1: The Odds API Format (Turkey vs Bulgaria)
echo ======================================================================
curl -X POST http://localhost:8000/api/analyze/ ^
  -H "Content-Type: application/json" ^
  -d "{\"id\":\"test123\",\"sport_key\":\"soccer_uefa\",\"commence_time\":\"2025-10-12T19:00:00Z\",\"home_team\":\"Turkey\",\"away_team\":\"Bulgaria\"}"

echo.
echo.
echo ======================================================================
echo Test completed! Check the output above.
echo Press any key to close...
pause
