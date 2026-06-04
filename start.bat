@echo off
cd /d .\backend
..\venv\Scripts\uvicorn.exe main:app --reload --host 0.0.0.0
pause