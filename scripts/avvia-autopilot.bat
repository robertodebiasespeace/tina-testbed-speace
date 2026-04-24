@echo off
chcp 65001 >nul
echo ============================================
echo  SPEACE Auto-Pilot Bridge - Avvio Rapido
echo ============================================
echo.

REM Verifica che lo script Python esista
if not exist "scripts\speace_autopilot.py" (
    echo [ERRORE] scripts\speace_autopilot.py non trovato.
    echo Assicurati di eseguire questo .bat dalla root del progetto.
    pause
    exit /b 1
)

REM Attiva virtual environment se esiste
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [INFO] Virtual environment attivato.
) else if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo [INFO] Virtual environment attivato.
) else (
    echo [WARN] Nessun virtual environment trovato, uso Python di sistema.
)

REM Verifica dipendenza pyautogui (pygetwindow e' opzionale)
python -c "import pyautogui" 2>nul
if errorlevel 1 (
    echo [WARN] pyautogui non installato. Installazione in corso...
    python -m pip install pyautogui
)
python -c "import pygetwindow" 2>nul
if errorlevel 1 (
    echo [INFO] pygetwindow non installato (opzionale). L'auto-pilot funziona ugualmente.
    echo         Assicurati che il terminale di Claude Code sia la finestra attiva.
)

REM Parsing argomenti
set DRY_RUN=
set ONCE=
set INTERVAL_MIN=10
set INTERVAL_MAX=30

:parse_args
if "%~1"=="" goto :run
if "%~1"=="--dry-run" (
    set DRY_RUN=--dry-run
    echo [INFO] Modalita dry-run attiva.
)
if "%~1"=="--once" (
    set ONCE=--once
    echo [INFO] Modalita ciclo singolo attiva.
)
if "%~1"=="--interval-min" (
    set INTERVAL_MIN=%~2
    shift
)
if "%~1"=="--interval-max" (
    set INTERVAL_MAX=%~2
    shift
)
shift
goto :parse_args

:run
echo.
echo [INFO] Avvio SPEACE Auto-Pilot...
echo        Intervallo: %INTERVAL_MIN%-%INTERVAL_MAX% minuti
echo        Premi Ctrl+C per interrompere.
echo.

python scripts\speace_autopilot.py %DRY_RUN% %ONCE% --interval-min %INTERVAL_MIN% --interval-max %INTERVAL_MAX%

if errorlevel 1 (
    echo.
    echo [ERRORE] Auto-Pilot terminato con errore.
)

echo.
echo [INFO] Auto-Pilot fermato.
pause
exit /b 0
