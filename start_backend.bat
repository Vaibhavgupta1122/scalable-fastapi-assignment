@echo off
echo Starting FastAPI Backend...
echo.

cd backend
call venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
