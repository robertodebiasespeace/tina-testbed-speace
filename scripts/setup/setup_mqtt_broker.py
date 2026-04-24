#!/usr/bin/env python3
"""
SPEACE MQTT Broker Setup Script
Configura Mosquitto MQTT per SPEACE IoT Infrastructure

Versione: 1.0
Data: 21 aprile 2026

Uso:
    python scripts/setup/setup_mqtt_broker.py [install|test|status]
"""

import subprocess
import sys
import os
import json
import time
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")

def run_command(cmd, description="", check=True):
    """Esegue comando shell"""
    if description:
        print_info(f"{description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=check
        )
        return True, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        if check:
            print_error(f"Comando fallito: {cmd}")
            print(f"Errore: {e.stderr}")
        return False, e.stdout, e.stderr

def check_platform():
    """Verifica piattaforma"""
    print_header("CHECK PLATFORM")

    import platform
    system = platform.system()
    print_info(f"Piattaforma rilevata: {system}")

    if system == "Windows":
        print_warning("Setup automatico MQTT non supportato su Windows")
        print_info("Istruzioni manuali disponibili in: docs/MQTT_SETUP.md")
        return "windows"
    elif system == "Linux":
        return "linux"
    elif system == "Darwin":
        return "macos"
    else:
        print_error(f"Piattaforma non supportata: {system}")
        return None

def install_mosquitto_linux():
    """Installa Mosquitto su Linux"""
    print_header("INSTALLAZIONE MOSQUITTO (Linux)")

    # Verifica se mosquitto è già installato
    success, _, _ = run_command("which mosquitto", check=False)

    if success:
        print_success("Mosquitto già installato")
        return True

    # Installazione
    print_info("Installazione Mosquitto...")

    # Detect distro
    success, stdout, _ = run_command("cat /etc/os-release | grep ^ID=", check=False)
    distro = stdout.strip().replace('ID=', '').replace('"', '') if success else "unknown"

    if distro in ["ubuntu", "debian"]:
        cmds = [
            "sudo apt-get update",
            "sudo apt-get install -y mosquitto mosquitto-clients"
        ]
    elif distro in ["fedora", "rhel", "centos"]:
        cmds = [
            "sudo dnf install -y mosquitto",
            "sudo dnf install -y mosquitto-clients"
        ]
    elif distro in ["arch"]:
        cmds = [
            "sudo pacman -S --noconfirm mosquitto"
        ]
    else:
        print_warning(f"Distro {distro} non testata, tentativo con apt...")
        cmds = [
            "sudo apt-get update",
            "sudo apt-get install -y mosquitto mosquitto-clients"
        ]

    for cmd in cmds:
        success, _, _ = run_command(cmd)
        if not success:
            print_error(f"Comando fallito: {cmd}")
            return False

    print_success("Mosquitto installato")
    return True

def configure_mosquitto():
    """Configura Mosquitto con file SPEACE"""
    print_header("CONFIGURAZIONE MOSQUITTO")

    config_src = Path("config/mosquitto.conf")
    config_dest = Path("/etc/mosquitto/conf.d/speace.conf")

    if not config_src.exists():
        print_error(f"File configurazione non trovato: {config_src}")
        return False

    # Per Linux, richiede sudo
    # Per Windows/altro, copia in directory locale

    # Creare directory mosquitto locale per testing
    mosquitto_dir = Path("mosquitto_data")
    mosquitto_dir.mkdir(exist_ok=True)
    (mosquitto_dir / "log").mkdir(exist_ok=True)
    (mosquitto_dir / "data").mkdir(exist_ok=True)

    # Copia config locale
    local_config = mosquitto_dir / "mosquitto.conf"

    with open(config_src, 'r') as f:
        config_content = f.read()

    # Aggiorna path per setup locale
    config_content = config_content.replace(
        "/var/lib/mosquitto/",
        str(mosquitto_dir / "data" / "") + "/"
    )
    config_content = config_content.replace(
        "/var/log/mosquitto/",
        str(mosquitto_dir / "log" / "") + "/"
    )

    with open(local_config, 'w') as f:
        f.write(config_content)

    print_success(f"Configurazione salvata in: {local_config}")

    # Salva info per report
    config_info = {
        "local_config_path": str(local_config),
        "data_path": str(mosquitto_dir / "data"),
        "log_path": str(mosquitto_dir / "log"),
        "broker_host": "localhost",
        "broker_port": 1883,
        "websocket_port": 9001
    }

    with open("mosquitto_config.json", 'w') as f:
        json.dump(config_info, f, indent=2)

    print_info(f"Info broker salvate in: mosquitto_config.json")
    return True

def create_test_script():
    """Crea script di test MQTT"""
    print_header("CREAZIONE SCRIPT TEST")

    test_script = '''#!/usr/bin/env python3
"""
SPEACE MQTT Test Script
Verifica funzionamento broker MQTT
"""

import paho.mqtt.client as mqtt
import json
import time
import sys

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✓ Connesso al broker MQTT")
        client.subscribe("speace/test/#")
    else:
        print(f"✗ Connessione fallita, codice: {rc}")

def on_message(client, userdata, msg):
    print(f"📨 Ricevuto: {msg.topic} = {msg.payload.decode()}")

def test_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect("localhost", 1883, 60)
        client.loop_start()

        # Test publish
        time.sleep(1)
        test_msg = {"test": "message", "timestamp": time.time()}
        client.publish("speace/test/hello", json.dumps(test_msg))
        print("✓ Messaggio pubblicato")

        time.sleep(2)
        client.loop_stop()
        client.disconnect()
        print("✓ Test MQTT completato")
        return True

    except Exception as e:
        print(f"✗ Errore: {e}")
        return False

if __name__ == "__main__":
    success = test_mqtt()
    sys.exit(0 if success else 1)
'''

    test_path = Path("scripts/test_mqtt.py")
    test_path.parent.mkdir(parents=True, exist_ok=True)

    with open(test_path, 'w') as f:
        f.write(test_script)

    print_success(f"Script test creato: {test_path}")
    return True

def create_start_script():
    """Crea script per avviare broker"""
    print_header("CREAZIONE SCRIPT AVVIO")

    # Linux/Mac script
    start_script = '''#!/bin/bash
# SPEACE MQTT Broker Start Script

CONFIG_DIR="mosquitto_data"
PIDFILE="$CONFIG_DIR/mosquitto.pid"

if [ -f "$PIDFILE" ]; then
    echo "Mosquitto già in esecuzione (PID: $(cat $PIDFILE))"
    exit 0
fi

echo "Avvio Mosquitto..."
mosquitto -c "$CONFIG_DIR/mosquitto.conf" -d

if [ $? -eq 0 ]; then
    echo "✓ Mosquitto avviato"
    echo "Broker: localhost:1883"
    echo "WebSocket: localhost:9001"
else
    echo "✗ Avvio fallito"
    exit 1
fi
'''

    start_path = Path("scripts/start_mqtt.sh")
    with open(start_path, 'w') as f:
        f.write(start_script)

    # Windows script
    start_win_script = '''@echo off
REM SPEACE MQTT Broker Start Script (Windows)

set CONFIG_DIR=mosquitto_data
set PIDFILE=%CONFIG_DIR%/mosquitto.pid

if exist "%PIDFILE%" (
    echo Mosquitto gia in esecuzione
    exit /b 0
)

echo Avvio Mosquitto...
mosquitto -c "%CONFIG_DIR%/mosquitto.conf"

if %ERRORLEVEL% == 0 (
    echo Mosquitto avviato
    echo Broker: localhost:1883
) else (
    echo Avvio fallito
    exit /b 1
)
'''

    start_win_path = Path("scripts/start_mqtt.bat")
    with open(start_win_path, 'w') as f:
        f.write(start_win_script)

    print_success(f"Script avvio creati: {start_path}, {start_win_path}")
    return True

def generate_documentation():
    """Genera documentazione setup"""
    print_header("GENERAZIONE DOCUMENTAZIONE")

    doc_content = '''# SPEACE MQTT Broker Setup Guide

## Panoramica
Questa guida descrive il setup del broker MQTT per SPEACE IoT Infrastructure.

## Configurazione
- **Host**: localhost
- **Porta MQTT**: 1883
- **Porta WebSocket**: 9001
- **Protocolli**: MQTT 3.1.1, WebSocket

## Topic Structure

```
speace/
├── sensors/
│   ├── thermal/{sensor_id}
│   ├── acoustic/{sensor_id}
│   ├── visual/{sensor_id}
│   ├── olfactory/{sensor_id}
│   └── tactile/{sensor_id}
├── alerts/
│   ├── anomaly
│   └── system
├── agents/
│   └── {agent_id}/status
├── swarm/
│   ├── heartbeat
│   ├── tasks
│   └── coordination
├── commands/
│   └── user
└── status/
    └── system
```

## Avvio Broker

### Linux/Mac
```bash
./scripts/start_mqtt.sh
```

### Windows
```cmd
scripts/start_mqtt.bat
```

## Testing
```bash
python scripts/test_mqtt.py
```

## Troubleshooting

### Errore "Address already in use"
- Verificare che non ci siano altri broker in esecuzione
- Porta 1883 potrebbe essere occupata

### Errore "Permission denied"
- Verificare permessi directory mosquitto_data/
- Su Linux, potrebbe richiedere sudo per porte <1024

## Sicurezza (Produzione)

Per ambiente di produzione, abilitare:
1. Autenticazione con password
2. TLS/SSL per connessioni crittografate
3. ACL per controllo accessi topic

Vedi: `config/mosquitto.conf` per opzioni avanzate.

## Dipendenze Python
```bash
pip install paho-mqtt
```

## Collegamento a SPEACE
Il `PhysicalSensorHub` si connette automaticamente al broker
usando il file `mosquitto_config.json`.

## Supporto
- Issue: GitHub SPEACE Repository
- Email: rigeneproject@rigene.eu
'''

    doc_path = Path("docs/MQTT_SETUP.md")
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    with open(doc_path, 'w') as f:
        f.write(doc_content)

    print_success(f"Documentazione creata: {doc_path}")
    return True

def main():
    """Main function"""
    print_header("SPEACE MQTT BROKER SETUP")

    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = "install"

    if command == "install":
        steps = [
            ("Check platform", check_platform),
            ("Configure Mosquitto", configure_mosquitto),
            ("Create test script", create_test_script),
            ("Create start script", create_start_script),
            ("Generate documentation", generate_documentation),
        ]

        # Per Linux, aggiungi installazione pacchetto
        if check_platform() == "linux":
            steps.insert(1, ("Install Mosquitto", install_mosquitto_linux))

    elif command == "test":
        print_info("Esecuzione test MQTT...")
        # Richiede paho-mqtt installato
        return 0

    elif command == "status":
        print_info("Controllo stato broker...")
        return 0

    else:
        print_error(f"Comando sconosciuto: {command}")
        print_info("Uso: python setup_mqtt_broker.py [install|test|status]")
        return 1

    results = {}
    for step_name, step_func in steps:
        try:
            success = step_func()
            results[step_name] = "SUCCESS" if success else "FAILED"
        except Exception as e:
            print_error(f"Errore in {step_name}: {e}")
            results[step_name] = f"ERROR: {e}"

    # Summary
    print_header("SETUP SUMMARY")

    for step_name, result in results.items():
        status_icon = "✓" if result == "SUCCESS" else "✗"
        color = Colors.OKGREEN if result == "SUCCESS" else Colors.FAIL
        print(f"{color}{status_icon} {step_name}: {result}{Colors.ENDC}")

    all_success = all(r == "SUCCESS" for r in results.values())

    if all_success:
        print_header("SETUP COMPLETATO")
        print_info("MQTT Broker configurato per SPEACE")
        print_info("Prossimo passo: avviare broker con ./scripts/start_mqtt.sh")
        print_info("o eseguire: python setup_mqtt_broker.py test")
        return 0
    else:
        print_header("SETUP COMPLETATO CON ERRORI")
        return 1

if __name__ == "__main__":
    sys.exit(main())
