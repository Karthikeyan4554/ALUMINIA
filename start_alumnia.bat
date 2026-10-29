@echo off
title Alumnia Full-Stack Web Platform
cls
echo =====================================================================
echo   ALUMNIA - Generative AI Based Alumni Networking Platform
echo   Bannari Amman Institute of Technology, Sathyamangalam
echo =====================================================================
echo.
echo [1/2] Starting FastAPI Backend & Unified Web Server on http://localhost:8000 ...
start "Alumnia Backend (Port 8000)" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Starting React Vite Dev Server on http://localhost:5173 ...
start "Alumnia Frontend (Port 5173)" cmd /k "cd /d %~dp0frontend && npm.cmd run dev"

echo Waiting for servers to initialize...
timeout /t 5 /nobreak >nul

echo Opening browser at http://localhost:8000 ...
start "" "http://localhost:8000"

echo.
echo =====================================================================
echo   Alumnia Web Platform is running!
echo   Main Website    : http://localhost:8000 (Unified, zero-proxy)
echo   Vite Dev Server : http://localhost:5173 (Development)
echo   API Swagger Docs: http://localhost:8000/docs
echo =====================================================================
