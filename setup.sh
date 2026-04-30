#!/usr/bin/env bash
# SPEACE Setup Script (Linux / macOS)
# Usage: ./setup.sh [--with-ml] [--force]
set -euo pipefail

WITH_ML=false; FORCE=false
for arg in "$@"; do
    case "$arg" in --with-ml) WITH_ML=true ;; --force) FORCE=true ;; esac
done

cd "$(dirname "$0")"

echo -e "\033[1;36m============================================\033[0m"
echo -e "\033[1;36m  SPEACE Framework - Setup\033[0m"
echo -e "\033[1;36m============================================\033[0m"
echo ""

echo -e "\033[1;33m[1/4] Checking Python...\033[0m"
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        v=$("$cmd" --version 2>&1)
        PYTHON="$cmd"
        echo -e "  \033[0;32mFound: $v\033[0m"
        break
    fi
done
if [ -z "$PYTHON" ]; then
    echo -e "\033[0;31m  ERROR: Python 3.10+ required.\033[0m"
    exit 1
fi

echo -e "\033[1;33m[2/4] Setting up virtual environment...\033[0m"
if [ -d "venv" ]; then
    if $FORCE; then
        rm -rf venv
    else
        echo -e "  \033[0;36mvenv exists. Use --force to recreate.\033[0m"
    fi
fi
if [ ! -d "venv" ]; then
    "$PYTHON" -m venv venv
    echo -e "  \033[0;32mCreated venv/\033[0m"
fi
source venv/bin/activate
pip install --upgrade pip --quiet

echo -e "\033[1;33m[3/4] Installing dependencies...\033[0m"
pip install -r requirements.txt --quiet
if $WITH_ML; then
    echo -e "  \033[0;35mInstalling ML deps (~2GB, be patient)...\033[0m"
    pip install -r requirements-ml.txt --quiet
fi

echo -e "\033[1;33m[4/4] Finalizing...\033[0m"
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo -e "  \033[0;36mCreated .env from .env.example\033[0m"
fi

echo ""
echo -e "\033[1;36m============================================\033[0m"
echo -e "\033[1;32m  SETUP COMPLETE\033[0m"
echo -e "\033[1;36m============================================\033[0m"
echo ""
echo -e "  \033[0mNext: edit .env, then:\033[0m"
echo -e "    \033[0mpython scripts/speace-cli.py\033[0m"
echo -e "    \033[0mpython scripts/speace_autopilot.py\033[0m"
