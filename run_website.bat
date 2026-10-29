@echo off
title Alumnia Web Platform
cls
echo =====================================================================
echo   ALUMNIA - Generative AI Based Alumni Networking Platform
echo   Bannari Amman Institute of Technology, Sathyamangalam
echo =====================================================================
echo.
echo Launching unified web platform on http://localhost:8000 ...
echo.

cd /d "%~dp0backend"

echo Opening browser at http://localhost:8000 in 3 seconds...
start "" "http://localhost:8000"

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
pause
