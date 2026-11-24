@echo off
title MediLink Healthcare Platform Launcher
color 0b

echo =========================================================
echo              Starting MediLink Healthcare Platform
echo =========================================================
echo.

:: Detect root directory whether launched from outer or inner folder
set "ROOT=%~dp0"
if exist "%ROOT%Medilink\backend\run.py" (
    set "BACKEND_DIR=%ROOT%Medilink\backend"
    set "FRONTEND_DIR=%ROOT%Medilink\frontend"
) else if exist "%ROOT%backend\run.py" (
    set "BACKEND_DIR=%ROOT%backend"
    set "FRONTEND_DIR=%ROOT%frontend"
) else (
    echo [ERROR] Could not find MediLink backend and frontend folders!
    echo Looked in: %ROOT%
    pause
    exit /b 1
)

echo [OK] Project root located:
echo      Backend:  %BACKEND_DIR%
echo      Frontend: %FRONTEND_DIR%
echo.

:: Verify Python Virtual Environment
if not exist "%BACKEND_DIR%\venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment python.exe not found at:
    echo "%BACKEND_DIR%\venv\Scripts\python.exe"
    pause
    exit /b 1
)

:: Free up ports 5000 and 5173 if lingering processes exist
echo [*] Checking and clearing ports 5000 and 5173...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5000 "') do (
    if not "%%a"=="" if not "%%a"=="0" taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5173 "') do (
    if not "%%a"=="" if not "%%a"=="0" taskkill /F /PID %%a >nul 2>&1
)

echo [1/2] Launching MediLink Backend API (Flask on http://127.0.0.1:5000)...
start "MediLink Backend API" cmd /k "cd /d "%BACKEND_DIR%" && ".\venv\Scripts\python.exe" run.py"

echo [2/2] Launching MediLink Frontend (Vite on http://localhost:5173)...
start "MediLink Frontend Web" cmd /k "cd /d "%FRONTEND_DIR%" && npm run dev"

echo.
echo [*] Waiting 3 seconds for services to initialize...
ping 127.0.0.1 -n 4 >nul

echo [*] Opening MediLink in your default browser...
start http://localhost:5173

echo.
echo =========================================================
echo  MediLink is now running!
echo  Frontend URL: http://localhost:5173
echo  Backend API:  http://127.0.0.1:5000
echo.
echo  Demo Credentials:
echo  - Patient:        patient@medilink.com  / Patient@123
echo  - Hospital Admin: hospital@medilink.com / Hospital@123
echo  - Super Admin:    admin@medilink.com    / Admin@123
echo =========================================================
echo  Keep the server command windows open while using the app.
echo.
pause
