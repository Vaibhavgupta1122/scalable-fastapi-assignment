@echo off
echo Setting up demo database for Scalable FastAPI Assignment...
echo.

REM Activate virtual environment
call venv\Scripts\activate

REM Create demo data
python create_demo_data.py

echo.
echo Demo database is ready!
echo.
echo Login Credentials:
echo   Admin: admin@demo.com / admin
echo   Users: john@demo.com / john
echo          jane@demo.com / jane  
echo          bob@demo.com / bob
echo.
echo Access the app at:
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:8000/docs
echo.
pause
