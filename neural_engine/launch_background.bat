@echo off
chcp 65001 > nul
echo ============================================
echo  SPEACE Neural Engine Launcher
echo  Versione 1.0 | Windows
echo ============================================
echo.

REM Avvia il Neural Engine in modalita background continuo
REM con output loggato su file per evitare problemi di buffering

set LOGFILE=neural_engine_background.log
set INTERVAL=10

echo [Launcher] Avvio Neural Engine in background...
echo [Launcher] Log file: %LOGFILE%
echo [Launcher] Intervallo cicli: %INTERVAL%s
echo.

start /B python -u neural_engine\neural_main.py --background --interval %INTERVAL% > %LOGFILE% 2>&1

echo [Launcher] Neural Engine avviato in background.
echo [Launcher] Per visualizzare il log in tempo reale, esegui:
echo    powershell -Command "Get-Content %LOGFILE% -Wait"
echo.
echo [Launcher] Per fermare il Neural Engine, esegui:
echo    taskkill /F /IM python.exe
echo.
pause
