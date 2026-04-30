#!/usr/bin/env python3
"""
SPEACE Auto-Revision & Consolidation Script (ARCS)
Processo automatizzato di revisione strutturale, validazione import,
allineamento dipendenze e sincronizzazione configurazione.

Versione: 1.0
Data: 22 aprile 2026
Autore: SPEACE Cortex
Uso:
    python scripts/speace_auto_revision.py [--scan-only] [--apply-fixes] [--apply-deps] [--full-auto] [--silent]

Focus attuale:
  1. Rendere eseguibile SPEACE-main.py
  2. Allineare requirements.txt con gli import reali
  3. Sincronizzare valori hardcoded (alignment, fitness)
"""

import sys
import os
import io

# Forza UTF-8 su Windows per evitare UnicodeEncodeError con simboli ANSI
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

import json
import ast
import re
import argparse
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict

# ---------------------------------------------------------------------------
# CONFIGURAZIONE
# ---------------------------------------------------------------------------
VERSION = "1.0"
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
REPORT_PATH = PROJECT_ROOT / "speace_auto_revision_report.json"
PROPOSALS_PATH = PROJECT_ROOT / "safe-proactive" / "PROPOSALS_AUTO_REVISION.md"
REQUIRED_DIRS = [
    "DigitalDNA",
    "SPEACE_Cortex",
    "SPEACE_Cortex/smfoi-kernel",
    "SPEACE_Cortex/agente_organismo",
    "SPEACE_Cortex/adaptive_consciousness",
    "safe-proactive",
    "scientific-team",
    "scientific-team/agents",
    "MultiFramework",
    "MultiFramework/anythingllm",
    "scripts",
    "docs",
    "tests",
]
REQUIRED_FILES = [
    "README.md",
    "requirements.txt",
    "SPEACE-main.py",
    "SPEACE-Engineering-Document-v1.2.md",
    "DigitalDNA/genome.yaml",
    "DigitalDNA/epigenome.yaml",
    "DigitalDNA/fitness_function.yaml",
    "DigitalDNA/mutation_rules.yaml",
    "SPEACE_Cortex/smfoi-kernel/smfoi_v0_3.py",
    "safe-proactive/PROPOSALS.md",
]
# Mappa degli import noti problematici (da correggere)
KNOWN_IMPORT_FIXES = {
    "safe_proactive.safe_proactive": {
        "issue": "package name contains hyphen",
        "actual_dir": "safe-proactive",
        "suggested_action": "Use importlib or rename directory to safe_proactive"
    },
    "SPEACE_Cortex.smfoi_kernel.smfoi_v0_3": {
        "issue": "directory is smfoi-kernel (hyphen)",
        "actual_dir": "SPEACE_Cortex/smfoi-kernel",
        "suggested_action": "Use importlib or rename directory to smfoi_kernel"
    },
    "MultiFramework.anythingllm.query_interface.WorldModelInterface": {
        "issue": "class does not exist",
        "actual_class": "WorldModelQueryInterface",
        "suggested_action": "Change import to WorldModelQueryInterface"
    }
}
# Mappa package top-level → nome in requirements.txt
IMPORT_TO_PACKAGE = {
    "anthropic": "anthropic",
    "chromadb": "chromadb",
    "flask": "flask",
    "numpy": "numpy",
    "paho": "paho-mqtt",
    "prometheus_client": "prometheus-client",
    "psutil": "psutil",
    "py2neo": "py2neo",
    "pydantic": "pydantic",
    "pyyaml": "pyyaml",
    "redis": "redis",
    "requests": "requests",
    "river": "river",
    "schedule": "schedule",
    "sentence_transformers": "sentence-transformers",
    "stable_baselines3": "stable-baselines3",
    "torch": "torch",
    "transformers": "transformers",
    "sklearn": "scikit-learn",
    "yaml": "pyyaml",
}

# ---------------------------------------------------------------------------
# COLORI ANSI
# ---------------------------------------------------------------------------
class Colors:
    OK = "\033[92m"      # verde
    WARN = "\033[93m"    # giallo
    ERR = "\033[91m"     # rosso
    INFO = "\033[94m"    # blu
    BOLD = "\033[1m"
    RESET = "\033[0m"
    @staticmethod
    def success(msg: str) -> str:
        return f"{Colors.OK}✓{Colors.RESET} {msg}"
    @staticmethod
    def warning(msg: str) -> str:
        return f"{Colors.WARN}⚠{Colors.RESET} {msg}"
    @staticmethod
    def error(msg: str) -> str:
        return f"{Colors.ERR}✗{Colors.RESET} {msg}"
    @staticmethod
    def info(msg: str) -> str:
        return f"{Colors.INFO}ℹ{Colors.RESET} {msg}"


# ---------------------------------------------------------------------------
# UTILITÀ
# ---------------------------------------------------------------------------
def sha256_dir(root: Path) -> str:
    """Calcola un hash della struttura file rilevante per tracciabilità."""
    hasher = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file() and ".git" not in path.parts:
            hasher.update(path.relative_to(root).as_posix().encode())
    return hasher.hexdigest()[:16]


def print_header(title: str):
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{title}{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")


def print_summary(results: Dict[str, Any], silent: bool):
    if silent:
        return
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}SPEACE AUTO-REVISION SUMMARY{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")
    total_issues = 0
    total_fixed = 0
    for phase, data in results.get("phases", {}).items():
        issues = data.get("issues_found", 0)
        fixed = data.get("issues_fixed", 0)
        total_issues += issues
        total_fixed += fixed
        color = Colors.OK if issues == 0 else Colors.WARN if fixed > 0 else Colors.ERR
        print(f"  {color}{phase:25s}{Colors.RESET}  issues: {issues:3d}  fixed: {fixed:3d}")
    print(f"\n  {Colors.BOLD}Total issues found : {total_issues}{Colors.RESET}")
    print(f"  {Colors.BOLD}Total safe fixes applied: {total_fixed}{Colors.RESET}")
    print(f"  {Colors.BOLD}Proposals generated: {results.get('proposals_generated', 0)}{Colors.RESET}")
    print(f"\n  Report saved to: {REPORT_PATH}")
    if PROPOSALS_PATH.exists():
        print(f"  Proposals saved to: {PROPOSALS_PATH}")
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}\n")


# ---------------------------------------------------------------------------
# PHASE 1 – STRUCTURAL SCAN
# ---------------------------------------------------------------------------
def phase_structural_scan() -> Tuple[List[Dict], int]:
    issues: List[Dict] = []
    fixed = 0

    print_header("PHASE 1: Structural Scan")

    # 1.1 Verifica directory richieste
    for d in REQUIRED_DIRS:
        p = PROJECT_ROOT / d
        if not p.exists():
            issues.append({
                "type": "missing_directory",
                "path": d,
                "severity": "high",
                "message": f"Directory richiesta mancante: {d}"
            })
            print(Colors.error(f"Missing directory: {d}"))
        else:
            print(Colors.success(f"Directory OK: {d}"))

    # 1.2 Verifica file richiesti
    for f in REQUIRED_FILES:
        p = PROJECT_ROOT / f
        if not p.exists():
            issues.append({
                "type": "missing_file",
                "path": f,
                "severity": "high",
                "message": f"File richiesto mancante: {f}"
            })
            print(Colors.error(f"Missing file: {f}"))
        else:
            print(Colors.success(f"File OK: {f}"))

    # 1.3 Rileva duplicati case-insensitive / trattini
    all_dirs = [d.name for d in PROJECT_ROOT.iterdir() if d.is_dir() and not d.name.startswith(".")]
    seen: Dict[str, List[str]] = defaultdict(list)
    for name in all_dirs:
        key = name.lower().replace("-", "_").replace(" ", "_")
        seen[key].append(name)
    for key, names in seen.items():
        if len(names) > 1:
            issues.append({
                "type": "duplicate_directory",
                "paths": names,
                "severity": "medium",
                "message": f"Directory duplicate rilevate: {names}"
            })
            print(Colors.warning(f"Duplicate directories: {names}"))

    # 1.4 Directory vuote documentate come "operative"
    empty_operational = [
        "SPEACE_Cortex/comparti",
        "SPEACE_Cortex/world_model",
        "SafeProactive/WAL",
        "SafeProactive/approval_gates",
        "SafeProactive/rollback_system",
        "Team_Scientifico/agents",
        "Team_Scientifico/orchestrator",
        "Team_Scientifico/output",
        "MultiFramework/ironclaw",
        "MultiFramework/nanoclaw",
        "MultiFramework/openclaw",
        "MultiFramework/superagi",
    ]
    for d in empty_operational:
        p = PROJECT_ROOT / d
        if p.exists() and p.is_dir():
            try:
                children = list(p.iterdir())
                if not children:
                    issues.append({
                        "type": "empty_operational_directory",
                        "path": d,
                        "severity": "low",
                        "message": f"Directory documentata come operativa ma vuota: {d}"
                    })
                    print(Colors.warning(f"Empty operational dir: {d}"))
            except Exception:
                pass

    return issues, fixed


# ---------------------------------------------------------------------------
# PHASE 2 – IMPORT VALIDATION
# ---------------------------------------------------------------------------
def phase_import_validation() -> Tuple[List[Dict], int]:
    issues: List[Dict] = []
    fixed = 0

    print_header("PHASE 2: Import Validation")

    py_files = list(PROJECT_ROOT.rglob("*.py"))
    for py_file in py_files:
        if ".git" in py_file.parts or "vendor" in py_file.parts:
            continue
        try:
            source = py_file.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except SyntaxError as e:
            issues.append({
                "type": "syntax_error",
                "file": str(py_file.relative_to(PROJECT_ROOT)),
                "severity": "high",
                "message": str(e)
            })
            print(Colors.error(f"Syntax error in {py_file.relative_to(PROJECT_ROOT)}: {e}"))
            continue
        except Exception as e:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    mod = alias.name.split(".")[0]
                    if mod in KNOWN_IMPORT_FIXES:
                        info = KNOWN_IMPORT_FIXES[mod]
                        issues.append({
                            "type": "known_bad_import",
                            "file": str(py_file.relative_to(PROJECT_ROOT)),
                            "import": alias.name,
                            "severity": "high",
                            "message": info["issue"],
                            "suggested_action": info["suggested_action"]
                        })
                        print(Colors.error(f"Known bad import: {alias.name} in {py_file.name}"))

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                full = module
                # Se importa un nome specifico, costruiamo la firma completa
                if node.names:
                    for alias in node.names:
                        candidate = f"{module}.{alias.name}" if module else alias.name
                        if candidate in KNOWN_IMPORT_FIXES:
                            info = KNOWN_IMPORT_FIXES[candidate]
                            issues.append({
                                "type": "known_bad_import",
                                "file": str(py_file.relative_to(PROJECT_ROOT)),
                                "import": candidate,
                                "severity": "high",
                                "message": info["issue"],
                                "suggested_action": info["suggested_action"]
                            })
                            print(Colors.error(f"Known bad import: {candidate} in {py_file.name}"))

                # Verifica trattini nel path del modulo
                parts = module.split(".")
                for part in parts:
                    if "-" in part:
                        issues.append({
                            "type": "hyphen_in_package_name",
                            "file": str(py_file.relative_to(PROJECT_ROOT)),
                            "import": module,
                            "severity": "high",
                            "message": f"Package name '{part}' contains hyphen, not importable in Python"
                        })
                        print(Colors.error(f"Hyphen in package name: {part} in {py_file.name}"))

                # Verifica esistenza modulo su disco (semplificato)
                if module.startswith("SPEACE_Cortex"):
                    rel = module.replace(".", "/") + ".py"
                    candidate = PROJECT_ROOT / rel
                    init_candidate = PROJECT_ROOT / module.replace(".", "/") / "__init__.py"
                    if not candidate.exists() and not init_candidate.exists():
                        issues.append({
                            "type": "unresolvable_local_import",
                            "file": str(py_file.relative_to(PROJECT_ROOT)),
                            "import": module,
                            "severity": "medium",
                            "message": f"Local module not found: {module}"
                        })
                        print(Colors.warning(f"Unresolved local import: {module} in {py_file.name}"))

    return issues, fixed


# Moduli della standard library (non vanno in requirements.txt)
# Usa sys.stdlib_module_names se disponibile (Python 3.10+), altrimenti fallback a set hardcoded
import sys
STDLIB_MODULES: Set[str] = getattr(sys, "stdlib_module_names", set())
if not STDLIB_MODULES:
    STDLIB_MODULES = {
        "__future__", "abc", "argparse", "ast", "asyncio", "atexit", "base64", "bisect", "builtins", "collections", "concurrent", "copy",
        "codecs", "contextlib", "contextvars", "csv", "dataclasses", "datetime", "decimal", "difflib", "enum", "errno", "fnmatch", "functools", "hashlib",
        "getpass", "glob", "heapq", "hmac", "html", "http", "imaplib", "importlib", "inspect", "io", "ipaddress", "itertools", "json",
        "logging", "math", "mimetypes", "multiprocessing", "numbers", "operator", "os", "pathlib",
        "pickle", "pkgutil", "platform", "pprint", "queue", "random", "re", "runpy", "secrets", "select", "shlex", "shutil", "signal", "socket",
        "sqlite3", "ssl", "stat", "statistics", "string", "struct", "subprocess", "sys", "tarfile", "tempfile", "textwrap", "threading",
        "time", "traceback", "typing", "unicodedata", "unittest", "urllib", "uuid", "warnings", "weakref", "xml", "zipfile", "zlib",
    }


def build_all_local_names(root: Path) -> Set[str]:
    """Raccoglie tutti i nomi di directory e file .py nel progetto come set locale."""
    local = set()
    skip_dirs = {".git", ".claude", "__pycache__", "venv", ".venv", "env", "node_modules", "vendor"}
    for path in root.rglob("*"):
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.is_dir():
            local.add(path.name)
            local.add(path.name.replace("-", "_").replace(" ", "_"))
        elif path.is_file() and path.suffix == ".py" and path.name != "__init__.py":
            local.add(path.stem)
            local.add(path.stem.replace("-", "_").replace(" ", "_"))
    return local


LOCAL_TOP_LEVEL = build_all_local_names(PROJECT_ROOT)
# Aggiungi nomi noti che sono import non validi ma ricorrenti nel codice
LOCAL_TOP_LEVEL.add("safeproactive")


# ---------------------------------------------------------------------------
# PHASE 3 – DEPENDENCY ALIGNMENT
# ---------------------------------------------------------------------------
def phase_dependency_alignment(apply: bool) -> Tuple[List[Dict], int]:
    issues: List[Dict] = []
    fixed = 0

    print_header("PHASE 3: Dependency Alignment")

    # 3.1 Estrai import effettivamente usati (escludendo stdlib e locali)
    used_packages: Set[str] = set()
    for py_file in PROJECT_ROOT.rglob("*.py"):
        if ".git" in py_file.parts or "vendor" in py_file.parts:
            continue
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
        except Exception:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    if top not in STDLIB_MODULES and top not in LOCAL_TOP_LEVEL:
                        used_packages.add(top)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    top = node.module.split(".")[0]
                    if top not in STDLIB_MODULES and top not in LOCAL_TOP_LEVEL:
                        used_packages.add(top)

    # Mappa in nomi di package requirements.txt
    used_reqs = set()
    for pkg in used_packages:
        mapped = IMPORT_TO_PACKAGE.get(pkg, pkg)
        used_reqs.add(mapped)

    # Aggiungi dipendenze "note" che sono usate indirettamente (es. da YAML, Docker, setup)
    # ma non importate direttamente in .py
    indirect_deps = {"sentence-transformers", "pydantic", "py2neo"}
    used_reqs.update(indirect_deps)

    # Rimuovi eventuali false positivi (nomi di directory locali con underscore)
    used_reqs = {p for p in used_reqs if p not in LOCAL_TOP_LEVEL and p not in STDLIB_MODULES}

    # 3.2 Leggi requirements.txt
    req_path = PROJECT_ROOT / "requirements.txt"
    listed_packages: Set[str] = set()
    req_lines: List[str] = []
    if req_path.exists():
        req_lines = req_path.read_text(encoding="utf-8").splitlines()
        for line in req_lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            pkg_name = line.split("==")[0].split(">=")[0].split("<")[0].strip()
            listed_packages.add(pkg_name)

    # 3.3 Trova mancanti
    missing = used_reqs - listed_packages
    for pkg in sorted(missing):
        issues.append({
            "type": "missing_dependency",
            "package": pkg,
            "severity": "medium",
            "message": f"Package '{pkg}' imported but not listed in requirements.txt"
        })
        print(Colors.error(f"Missing dependency: {pkg}"))

    # 3.4 Trova inutilizzati (solo warning, non fix automatico)
    unused = listed_packages - used_reqs
    for pkg in sorted(unused):
        issues.append({
            "type": "unused_dependency",
            "package": pkg,
            "severity": "low",
            "message": f"Package '{pkg}' listed but not imported in any .py file"
        })
        print(Colors.warning(f"Unused dependency: {pkg}"))

    # 3.5 Auto-fix: aggiungi dipendenze mancanti
    if apply and missing:
        print(Colors.info("Applying safe dependency fixes..."))
        new_lines = req_lines.copy()
        for pkg in sorted(missing):
            new_lines.append(f"{pkg}")
            fixed += 1
            print(Colors.success(f"Added to requirements.txt: {pkg}"))
        req_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    return issues, fixed


# ---------------------------------------------------------------------------
# PHASE 4 – CONFIGURATION SYNC
# ---------------------------------------------------------------------------
def phase_config_sync() -> Tuple[List[Dict], int]:
    issues: List[Dict] = []
    fixed = 0

    print_header("PHASE 4: Configuration Sync")

    # 4.1 Leggi alignment score da epigenome.yaml
    epigenome_path = PROJECT_ROOT / "DigitalDNA" / "epigenome.yaml"
    alignment_yaml = None
    if epigenome_path.exists():
        try:
            import yaml
            data = yaml.safe_load(epigenome_path.read_text(encoding="utf-8"))
            alignment_yaml = float(data.get("epigenome", {}).get("stato_corrente", {}).get("alignment_score", 0))
        except Exception as e:
            print(Colors.warning(f"Could not parse epigenome.yaml: {e}"))

    # 4.2 Cerca valori hardcoded in SPEACE-main.py
    main_path = PROJECT_ROOT / "SPEACE-main.py"
    if main_path.exists():
        text = main_path.read_text(encoding="utf-8")
        for match in re.finditer(r'alignment[_\s]*[:=]?\s*([0-9]+\.?[0-9]*)', text, re.IGNORECASE):
            val = float(match.group(1))
            if alignment_yaml is not None and abs(val - alignment_yaml) > 0.01:
                issues.append({
                    "type": "alignment_mismatch",
                    "file": "SPEACE-main.py",
                    "severity": "medium",
                    "message": f"Alignment score hardcoded {val} != epigenome.yaml {alignment_yaml}"
                })
                print(Colors.warning(f"Alignment mismatch in SPEACE-main.py: {val} vs YAML {alignment_yaml}"))

    # 4.3 Cerca in smfoi_v0_3.py
    smfoi_path = PROJECT_ROOT / "SPEACE_Cortex" / "smfoi-kernel" / "smfoi_v0_3.py"
    if smfoi_path.exists():
        text = smfoi_path.read_text(encoding="utf-8")
        for match in re.finditer(r'alignment[_\s]*score["\']?\s*[:=]?\s*([0-9]+\.?[0-9]*)', text, re.IGNORECASE):
            val = float(match.group(1))
            if alignment_yaml is not None and abs(val - alignment_yaml) > 0.01:
                issues.append({
                    "type": "alignment_mismatch",
                    "file": "SPEACE_Cortex/smfoi-kernel/smfoi_v0_3.py",
                    "severity": "medium",
                    "message": f"Alignment score hardcoded {val} != epigenome.yaml {alignment_yaml}"
                })
                print(Colors.warning(f"Alignment mismatch in smfoi_v0_3.py: {val} vs YAML {alignment_yaml}"))

    # 4.4 Verifica fitness function weights coerenza
    fitness_path = PROJECT_ROOT / "DigitalDNA" / "fitness_function.yaml"
    if fitness_path.exists():
        try:
            import yaml
            data = yaml.safe_load(fitness_path.read_text(encoding="utf-8"))
            weights = data.get("fitness_function", {}).get("weights", {})
            if smfoi_path.exists():
                text = smfoi_path.read_text(encoding="utf-8")
                # Cerca i pesi hardcoded nel codice (es. alignment * 0.35)
                code_weights = {}
                for match in re.finditer(r'alignment\s*\*\s*([0-9.]+)', text):
                    code_weights['alignment'] = float(match.group(1))
                for match in re.finditer(r'success_rate\s*\*\s*([0-9.]+)', text):
                    code_weights['success_rate'] = float(match.group(1))
                for match in re.finditer(r'stability\s*\*\s*([0-9.]+)', text):
                    code_weights['stability'] = float(match.group(1))
                for match in re.finditer(r'efficiency\s*\*\s*([0-9.]+)', text):
                    code_weights['efficiency'] = float(match.group(1))
                for match in re.finditer(r'ethics\s*\*\s*([0-9.]+)', text):
                    code_weights['ethics'] = float(match.group(1))

                for key, yaml_val in weights.items():
                    code_val = code_weights.get(key)
                    if code_val is not None and abs(code_val - yaml_val) > 0.001:
                        issues.append({
                            "type": "fitness_weight_mismatch",
                            "file": "SPEACE_Cortex/smfoi-kernel/smfoi_v0_3.py",
                            "severity": "medium",
                            "message": f"Fitness weight '{key}': code={code_val} != yaml={yaml_val}"
                        })
                        print(Colors.warning(f"Fitness weight mismatch '{key}': code={code_val} vs yaml={yaml_val}"))
        except Exception as e:
            print(Colors.warning(f"Could not parse fitness_function.yaml: {e}"))

    return issues, fixed


# ---------------------------------------------------------------------------
# PHASE 5 – AUTO-FIX SAFE & PROPOSAL GENERATION
# ---------------------------------------------------------------------------
def phase_autofix_and_proposals(all_issues: List[Dict], apply_fixes: bool) -> Tuple[int, int]:
    safe_fixed = 0
    proposals = 0

    print_header("PHASE 5: Auto-Fix & Proposals")

    proposal_lines: List[str] = [
        "# Proposte di Revisione Auto-Generate",
        f"**Data:** {datetime.now().isoformat()}",
        "**Sorgente:** scripts/speace_auto_revision.py",
        "",
        "---",
        ""
    ]

    # Raggruppa per tipo
    by_type: Dict[str, List[Dict]] = defaultdict(list)
    for issue in all_issues:
        by_type[issue["type"]].append(issue)

    # Fix low-risk: aggiungi commento TODO nei file con stub/mock rilevati
    if apply_fixes:
        stub_files = set()
        for issue in by_type.get("empty_operational_directory", []):
            # Non possiamo fixare directory vuote automaticamente
            pass
        # Non ci sono fix low-risk strutturali automatici sicuri da fare
        # senza rischio di rottura
        print(Colors.info("No automatic structural fixes applied (human review required)."))

    # Genera proposte per issue high/medium
    for issue in all_issues:
        severity = issue.get("severity", "low")
        if severity in ("medium", "high"):
            proposals += 1
            proposal_lines.append(f"## Proposal AUTO-{proposals:03d}")
            proposal_lines.append(f"**Tipo:** {issue['type']}")
            proposal_lines.append(f"**Severità:** {severity}")
            proposal_lines.append(f"**File/Path:** {issue.get('file', issue.get('path', 'N/A'))}")
            proposal_lines.append(f"**Messaggio:** {issue['message']}")
            if "suggested_action" in issue:
                proposal_lines.append(f"**Azione Suggerita:** {issue['suggested_action']}")
            proposal_lines.append("")
            proposal_lines.append("### Decisione")
            proposal_lines.append("- [ ] Approva")
            proposal_lines.append("- [ ] Rifiuta")
            proposal_lines.append("- [ ] Richiede chiarimenti")
            proposal_lines.append("")
            proposal_lines.append("---")
            proposal_lines.append("")

    if proposals > 0:
        PROPOSALS_PATH.parent.mkdir(parents=True, exist_ok=True)
        PROPOSALS_PATH.write_text("\n".join(proposal_lines), encoding="utf-8")
        print(Colors.info(f"Generated {proposals} proposals in {PROPOSALS_PATH}"))
    else:
        print(Colors.success("No medium/high severity issues requiring proposals."))

    return safe_fixed, proposals


# ---------------------------------------------------------------------------
# PHASE 6 – REPORT GENERATION
# ---------------------------------------------------------------------------
def phase_report(results: Dict[str, Any]):
    print_header("PHASE 6: Report Generation")

    results["timestamp"] = datetime.now().isoformat()
    results["version"] = VERSION
    results["repository_hash"] = sha256_dir(PROJECT_ROOT)
    results["report_path"] = str(REPORT_PATH)

    REPORT_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(Colors.success(f"Report saved to {REPORT_PATH}"))


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="SPEACE Auto-Revision & Consolidation Script")
    parser.add_argument("--scan-only", action="store_true", help="Solo scansione, nessuna modifica")
    parser.add_argument("--apply-fixes", action="store_true", help="Applica fix a basso rischio")
    parser.add_argument("--apply-deps", action="store_true", help="Aggiunge dipendenze mancanti a requirements.txt")
    parser.add_argument("--full-auto", action="store_true", help="Scan + fix safe + deps + report")
    parser.add_argument("--silent", action="store_true", help="Output solo su file JSON")
    args = parser.parse_args()

    silent = args.silent
    scan_only = args.scan_only
    full_auto = args.full_auto
    apply_fixes = args.apply_fixes or full_auto
    apply_deps = args.apply_deps or full_auto

    if not silent:
        print(f"{Colors.BOLD}SPEACE Auto-Revision & Consolidation v{VERSION}{Colors.RESET}")
        print(f"Project root: {PROJECT_ROOT}\n")

    if scan_only:
        apply_fixes = False
        apply_deps = False

    # Esecuzione fasi
    struct_issues, struct_fixed = phase_structural_scan()
    import_issues, import_fixed = phase_import_validation()
    dep_issues, dep_fixed = phase_dependency_alignment(apply_deps)
    config_issues, config_fixed = phase_config_sync()

    all_issues = struct_issues + import_issues + dep_issues + config_issues
    safe_fixed, proposals = phase_autofix_and_proposals(all_issues, apply_fixes)

    # Calcola totali
    total_fixed = struct_fixed + import_fixed + dep_fixed + config_fixed + safe_fixed

    results = {
        "phases": {
            "structural_scan": {
                "issues_found": len(struct_issues),
                "issues_fixed": struct_fixed,
                "details": struct_issues
            },
            "import_validation": {
                "issues_found": len(import_issues),
                "issues_fixed": import_fixed,
                "details": import_issues
            },
            "dependency_alignment": {
                "issues_found": len(dep_issues),
                "issues_fixed": dep_fixed,
                "details": dep_issues
            },
            "config_sync": {
                "issues_found": len(config_issues),
                "issues_fixed": config_fixed,
                "details": config_issues
            }
        },
        "proposals_generated": proposals,
        "safe_fixes_applied": total_fixed,
    }

    phase_report(results)
    print_summary(results, silent)

    # Exit code: 0 se nessun issue high, 1 altrimenti
    high_issues = [i for i in all_issues if i.get("severity") == "high"]
    if high_issues:
        if not silent:
            print(Colors.error(f"{len(high_issues)} high severity issues found. Review required."))
        sys.exit(1)
    else:
        if not silent:
            print(Colors.success("No high severity issues. Repository is healthy."))
        sys.exit(0)


if __name__ == "__main__":
    main()
