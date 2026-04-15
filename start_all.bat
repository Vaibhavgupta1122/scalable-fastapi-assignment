@echo off
echo Starting Scalable FastAPI Assignment - Backend and Frontend
echo ==========================================================
echo.

echo [1/2] Starting Backend Server...
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo [2/2] Starting Frontend Server...
timeout /t 3 /nobreak >nul
start "Frontend Server" cmd /k "cd frontend && npm start"

echo.
echo Both servers are starting...
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit this window (servers will continue running)...
pause
