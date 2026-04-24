# SPEACE Scripts

Utility e automazioni per il sistema SPEACE.

## Struttura

```
scripts/
├── setup/              # Script di setup e configurazione
│   ├── setup.bat       # Setup Windows (dipendenze, directory)
│   └── git-push-github.ps1  # Template per push GitHub
│
├── ahk/                # AutoHotkey v2 scripts (Windows)
│   ├── speace-launcher.ahk   # GUI launcher completo
│   └── speace-monitor.ahk    # Tray monitor con alert
│
├── speace-cortex-evolver.py    # Stimolatore evolutivo (moved from SPEACE_Cortex/)
├── speace_status_monitor.py    # Report stato (ogni 40 min)
└── run_daily_brief.py          # Generazione daily brief
```

## Setup Iniziale (Windows)

```bash
# Esegui setup.bat come Administrator
.\scripts\setup\setup.bat

# O esegui manualmente:
pip install -r requirements.txt
```

## AutoHotkey Scripts

### Requisiti
- AutoHotkey v2 installato: https://www.autohotkey.com/

### speace-launcher.ahk
GUI per avviare SPEACE con vari moduli:
- Doppio click su `scripts/ahk/speace-launcher.ahk`
- Pulsanti: Full System, Ciclo Singolo, Evolver, Monitor, Status

### speace-monitor.ahk
Monitoraggio continuo con tray icon:
- **Ctrl+Alt+S**: Apri status report
- **Ctrl+Alt+P**: Apri proposals
- **Ctrl+Alt+E**: Esegui evolver
- Icona tray con menu rapido

## GitHub Push

Il file `scripts/setup/git-push-github.ps1` è un **TEMPLATE**.

**ATTENZIONE**: Modifica le variabili prima dell'uso:
- `GITHUB_TOKEN`: Il tuo Personal Access Token
- `GITHUB_USER`: Il tuo username GitHub
- `REPO_NAME`: Il nome del repository

**ELIMINA IL FILE DOPO L'USO** per sicurezza.

## Altri Script

- `speace-cortex-evolver.py`: Heartbeat 60 min, genera proposte mutazione
- `speace_status_monitor.py`: Report stato 40 min, alert automatici
- `run_daily_brief.py`: Generazione daily brief team scientifico

## Note

- Tutti gli script sono pensati per Windows 11
- I path sono relativi alla root del progetto
- Per Linux/Mac: adatta i path e usa equivalenti bash
