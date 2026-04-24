#!/usr/bin/env python3
"""
Setup External Frameworks for SPEACE
Clona e installa AutoGPT Forge e Hermes Agent in directory vendor/ isolate
per evitare conflitti con le dipendenze core di SPEACE.

Versione: 1.0
Data: 22 aprile 2026
"""

import sys
import os
import io

# Forza UTF-8 su Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

import subprocess
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
VENDOR_DIR = ROOT_DIR / "vendor"

# Repository esterni
REPOS = {
    "autogpt": {
        "url": "https://github.com/Significant-Gravitas/AutoGPT.git",
        "path": VENDOR_DIR / "autogpt",
        "deps_file": "requirements.txt",
        "min_python": "3.10",
    },
    "hermes": {
        "url": "https://github.com/NousResearch/hermes-agent.git",
        "path": VENDOR_DIR / "hermes-agent",
        "deps_file": "requirements.txt",
        "min_python": "3.11",
        "note": "Richiede Linux/macOS/WSL2. Su Windows nativo potrebbe fallire.",
    }
}


def run(cmd, cwd=None, check=False):
    """Esegue un comando shell e ritorna (rc, stdout, stderr)."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, capture_output=True, text=True
    )
    if check and result.returncode != 0:
        print(f"[Setup] Errore: {result.stderr}")
        raise RuntimeError(f"Comando fallito: {cmd}")
    return result.returncode, result.stdout, result.stderr


def check_git():
    rc, _, _ = run("git --version")
    if rc != 0:
        print("[Setup] ❌ git non installato. Installa Git da https://git-scm.com/")
        sys.exit(1)
    print("[Setup] ✅ git trovato")


def clone_repo(name: str, url: str, dest: Path):
    if dest.exists():
        print(f"[Setup] ⚠️  {name} esiste già in {dest}. Skippo clone.")
        return
    print(f"[Setup] ⏳ Clonazione {name} da {url}...")
    rc, out, err = run(f"git clone --depth 1 {url} {dest}")
    if rc != 0:
        print(f"[Setup] ❌ Clone fallito: {err}")
        return False
    print(f"[Setup] ✅ {name} clonato in {dest}")
    return True


def install_deps(path: Path, deps_file: str):
    req = path / deps_file
    if not req.exists():
        # Prova pyproject.toml o setup.py
        if (path / "pyproject.toml").exists() or (path / "setup.py").exists():
            print(f"[Setup] ⏳ Installazione {path.name} via pip install -e .")
            rc, out, err = run(f"python -m pip install -e {path}", cwd=path)
            if rc != 0:
                print(f"[Setup] ⚠️  Installazione fallita: {err[:500]}")
                return False
            print(f"[Setup] ✅ {path.name} installato")
            return True
        print(f"[Setup] ⚠️  Nessun {deps_file} trovato in {path}")
        return False

    print(f"[Setup] ⏳ Installazione dipendenze da {req}...")
    rc, out, err = run(f"python -m pip install -r {req}")
    if rc != 0:
        print(f"[Setup] ⚠️  Installazione dipendenze fallita: {err[:500]}")
        return False
    print(f"[Setup] ✅ Dipendenze {path.name} installate")
    return True


def setup_agbenchmark():
    """Installa agbenchmark (benchmark AutoGPT, disponibile su PyPI)."""
    print("[Setup] ⏳ Installazione agbenchmark da PyPI...")
    rc, out, err = run("python -m pip install agbenchmark")
    if rc != 0:
        print(f"[Setup] ⚠️  agbenchmark fallito: {err[:500]}")
        return False
    print("[Setup] ✅ agbenchmark installato")
    return True


def main():
    print("="*60)
    print("  SPEACE External Frameworks Setup")
    print("  AutoGPT Forge + Hermes Agent")
    print("="*60)
    print()

    # Verifica preliminari
    check_git()
    VENDOR_DIR.mkdir(parents=True, exist_ok=True)

    # Abilita long paths su Windows per evitare errori di checkout AutoGPT
    if sys.platform == "win32":
        run("git config --global core.longpaths true")
        print("[Setup] ✅ git core.longpaths abilitato per Windows")

    results = {}

    # Installa agbenchmark (PyPI)
    results["agbenchmark"] = setup_agbenchmark()

    # Clone e installa AutoGPT
    autogpt = REPOS["autogpt"]
    clone_ok = clone_repo("AutoGPT", autogpt["url"], autogpt["path"])
    if clone_ok and sys.platform == "win32":
        # Riabilita checkout con longpaths dopo il clone
        run(f"git -C {autogpt['path']} config core.longpaths true")
        run(f"git -C {autogpt['path']} checkout HEAD -- .")
    results["autogpt"] = install_deps(autogpt["path"], autogpt["deps_file"])

    # Clone e installa Hermes Agent
    hermes = REPOS["hermes"]
    print(f"[Setup] ℹ️  Nota: {hermes['note']}")
    clone_repo("Hermes Agent", hermes["url"], hermes["path"])
    results["hermes"] = install_deps(hermes["path"], hermes["deps_file"])

    print()
    print("="*60)
    print("  Setup completato — Riepilogo")
    print("="*60)
    for name, ok in results.items():
        status = "✅ OK" if ok else "⚠️  Parziale/Fallito"
        print(f"  {name:20s} {status}")
    print()
    print("  Hermes Agent: operativo se configurato con HERMES_BASE_URL")
    print("  AutoGPT:      stub operativo con tool locali (calculator, file_ops)")
    print("  agbenchmark:  disponibile per benchmark task")
    print()
    print("  Vendor directory:", VENDOR_DIR)
    print("  Per aggiornare i repo in futuro, esegui:")
    print("    cd vendor/autogpt && git pull")
    print("    cd vendor/hermes-agent && git pull")
    print()


if __name__ == "__main__":
    main()
