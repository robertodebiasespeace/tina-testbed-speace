#!/usr/bin/env python3
"""
SPEACE ML Environment Setup Script
Automatizza setup dell'ambiente ML per SPEACE Learning Core

Versione: 1.0
Data: 21 aprile 2026
"""

import subprocess
import sys
import os
from pathlib import Path
import json

# Colori per output
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

def run_command(cmd, description=""):
    """Esegue comando shell e gestisce errori"""
    if description:
        print_info(f"{description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print_error(f"Comando fallito: {cmd}")
        print(f"Errore: {e.stderr}")
        return False, e.stderr

def check_python_version():
    """Verifica versione Python"""
    print_header("CHECK PYTHON VERSION")
    version = sys.version_info
    print_info(f"Python version rilevata: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print_error("Python >= 3.9 richiesto")
        return False

    print_success(f"Python {version.major}.{version.minor} OK")
    return True

def check_cuda_availability():
    """Verifica disponibilità CUDA"""
    print_header("CHECK CUDA AVAILABILITY")

    try:
        import torch
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            cuda_version = torch.version.cuda
            device_name = torch.cuda.get_device_name(0)
            print_success(f"CUDA disponibile: {cuda_version}")
            print_success(f"Device: {device_name}")
            return True
        else:
            print_warning("CUDA non disponibile - verrà usata CPU")
            return False
    except ImportError:
        print_warning("PyTorch non ancora installato")
        return False

def create_virtual_environment():
    """Crea virtual environment"""
    print_header("SETUP VIRTUAL ENVIRONMENT")

    venv_path = Path(".venv-speace-ml")

    if venv_path.exists():
        print_warning(f"Virtual environment esiste già: {venv_path}")
        return True

    success, _ = run_command(
        f"{sys.executable} -m venv {venv_path}",
        "Creazione virtual environment"
    )

    if success:
        print_success(f"Virtual environment creato: {venv_path}")
        print_info(f"Attivare con: {venv_path}/Scripts/activate")
        return True
    else:
        print_error("Creazione virtual environment fallita")
        return False

def install_requirements():
    """Installa requirements ML"""
    print_header("INSTALLAZIONE REQUIREMENTS")

    # Usa pip del virtual environment se esiste
    venv_pip = Path(".venv-speace-ml/Scripts/pip.exe")
    if venv_pip.exists():
        pip_cmd = str(venv_pip)
    else:
        pip_cmd = "pip"

    requirements_file = "requirements-ml.txt"

    if not os.path.exists(requirements_file):
        print_error(f"File {requirements_file} non trovato")
        return False

    success, _ = run_command(
        f"{pip_cmd} install -r {requirements_file}",
        "Installazione pacchetti ML"
    )

    if success:
        print_success("Requirements installati con successo")
        return True
    else:
        print_error("Installazione requirements fallita")
        return False

def verify_installations():
    """Verifica che tutti i pacchetti siano installati correttamente"""
    print_header("VERIFICA INSTALLAZIONI")

    packages = [
        ("river", "river"),
        ("torch", "torch"),
        ("transformers", "transformers"),
        ("sentence_transformers", "sentence-transformers"),
        ("stable_baselines3", "stable-baselines3"),
        ("chromadb", "chromadb"),
        ("numpy", "numpy"),
        ("pydantic", "pydantic"),
    ]

    all_ok = True
    results = {}

    for module_name, package_name in packages:
        try:
            module = __import__(module_name)
            version = getattr(module, "__version__", "unknown")
            print_success(f"{package_name}: {version}")
            results[package_name] = {"status": "ok", "version": version}
        except ImportError as e:
            print_error(f"{package_name}: NON INSTALLATO")
            results[package_name] = {"status": "error", "message": str(e)}
            all_ok = False

    # Verifica GPU PyTorch
    try:
        import torch
        if torch.cuda.is_available():
            print_success(f"PyTorch CUDA: Disponibile ({torch.cuda.get_device_name(0)})")
            results["cuda"] = {"status": "ok", "device": torch.cuda.get_device_name(0)}
        else:
            print_warning("PyTorch CUDA: Non disponibile (CPU mode)")
            results["cuda"] = {"status": "warning", "message": "CPU mode"}
    except:
        pass

    # Salva report
    report_file = "setup_ml_report.json"
    with open(report_file, 'w') as f:
        json.dump(results, f, indent=2)
    print_info(f"Report salvato in: {report_file}")

    return all_ok

def create_directory_structure():
    """Crea struttura directory per ML Core"""
    print_header("CREAZIONE STRUCTURE DIRECTORY")

    directories = [
        "SPEACE_Cortex/learning_core",
        "SPEACE_Cortex/learning_core/config",
        "SPEACE_Cortex/memory",
        "SPEACE_Cortex/memory/vector_store",
        "SPEACE_Cortex/memory/knowledge_graph",
        "experiments",
        "models",
        "data/ml",
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print_success(f"Directory creata: {directory}")

    return True

def create_init_files():
    """Crea __init__.py files"""
    print_header("CREAZIONE INIT FILES")

    init_files = [
        "SPEACE_Cortex/learning_core/__init__.py",
        "SPEACE_Cortex/memory/__init__.py",
    ]

    for init_file in init_files:
        Path(init_file).touch()
        print_success(f"Creato: {init_file}")

    return True

def main():
    """Main setup function"""
    print_header("SPEACE ML ENVIRONMENT SETUP")
    print(f"Data: {__import__('datetime').datetime.now().isoformat()}")
    print()

    steps = [
        ("Check Python version", check_python_version),
        ("Check CUDA availability", check_cuda_availability),
        ("Create directory structure", create_directory_structure),
        ("Create init files", create_init_files),
        ("Create virtual environment", create_virtual_environment),
        ("Install requirements", install_requirements),
        ("Verify installations", verify_installations),
    ]

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
        print_header("SETUP COMPLETATO CON SUCCESSO")
        print_info("Ambiente ML pronto per SPEACE Learning Core")
        print_info("Prossimo passo: implementare SPEACEOnlineLearner")
        return 0
    else:
        print_header("SETUP COMPLETATO CON ERRORI")
        print_warning("Verificare errori sopra e riprovare")
        return 1

if __name__ == "__main__":
    sys.exit(main())
