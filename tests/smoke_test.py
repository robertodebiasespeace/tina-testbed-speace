#!/usr/bin/env python3
"""
Smoke tests for TINA Testbed / SPEACE repository.
Verifies structure, file presence, and basic integrity.
"""

import os
import sys
import json
from pathlib import Path

REQUIRED_DIRS = [
    "docs",
    "scientific-team",
    "scientific-team/agents",
    "scientific-team/reports",
    "scripts",
]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "requirements.txt",
    "scientific-team/orchestrator-logic.md",
    "scientific-team/orchestrator.md",
    "scientific-team/team_state.example.json",
    "scripts/run_daily_brief.py",
]

def check_dirs():
    for d in REQUIRED_DIRS:
        if not os.path.isdir(d):
            print(f"❌ Missing directory: {d}")
            return False
        print(f"✅ Directory: {d}")
    return True

def check_files():
    all_present = True
    for f in REQUIRED_FILES:
        if not os.path.isfile(f):
            print(f"❌ Missing file: {f}")
            all_present = False
        else:
            size = os.path.getsize(f)
            print(f"✅ File: {f} ({size} bytes)")
    return all_present

def check_agent_profiles():
    agents_dir = Path("scientific-team/agents")
    if not agents_dir.exists():
        print("❌ Agents directory missing")
        return False
    count = len(list(agents_dir.glob("*.md")))
    if count < 7:
        print(f"❌ Expected at least 7 agent profiles, found {count}")
        return False
    print(f"✅ Found {count} agent profiles")
    return True

def check_sample_reports():
    reports_dir = Path("scientific-team/reports")
    if not reports_dir.exists():
        print("❌ Reports directory missing")
        return False
    count = len(list(reports_dir.glob("*.md")))
    if count < 8:  # 7 agents + daily brief
        print(f"⚠️ Expected at least 8 reports (7 agents + daily brief), found {count}")
        # Not a failure, just a warning
    print(f"✅ Found {count} reports")
    return True

def check_team_state_example():
    path = Path("scientific-team/team_state.example.json")
    if not path.exists():
        print("❌ team_state.example.json missing")
        return False
    try:
        data = json.loads(path.read_text())
        print(f"✅ team_state.example.json valid JSON with keys: {list(data.keys())}")
        return True
    except Exception as e:
        print(f"❌ team_state.example.json invalid: {e}")
        return False

def main():
    print("=== SPEACE TINA Testbed Smoke Test ===\n")

    checks = [
        ("Directories", check_dirs),
        ("Files", check_files),
        ("Agent Profiles", check_agent_profiles),
        ("Sample Reports", check_sample_reports),
        ("Team State Example", check_team_state_example),
    ]

    results = []
    for name, fn in checks:
        print(f"\n[{name}]")
        results.append(fn())

    print("\n=== Summary ===")
    if all(results):
        print("✅ All smoke tests passed")
        return 0
    else:
        print("❌ Some smoke tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
