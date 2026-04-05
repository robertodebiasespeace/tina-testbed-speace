#!/usr/bin/env python3
"""
SPEACE Daily Planetary Health Brief Generator

This script orchestrates the SPEACE Scientific Team to produce the Daily Brief.
It is part of the TINA Testbed reference implementation.

Usage:
  python run_daily_brief.py

Requirements:
  - OpenClaw environment
  - Internet access for API data collection
  - SafeProactive configured

Output:
  - scientific-team/reports/daily-brief-YYYY-MM-DD.md
  - Updates team_state.json
  - Generates SafeProactive proposals for high-score items

Schedule:
  Intended to run daily at 06:00 UTC via cron or OpenClaw scheduler.
"""

import json
import os
from datetime import datetime
from pathlib import Path

WORKSPACE = Path.cwd()
REPORTS_DIR = WORKSPACE / "scientific-team" / "reports"
TEAM_STATE = WORKSPACE / "scientific-team" / "team_state.json"

def load_team_state():
    if TEAM_STATE.exists():
        with open(TEAM_STATE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "last_daily_brief": None,
        "team_status": "initializing",
        "active_alerts": [],
        "agent_status": {
            "climate": "pending",
            "economics": "pending",
            "governance": "pending",
            "technology": "pending",
            "health": "pending",
            "social": "pending",
            "space": "pending"
        },
        "iteration": 92,
        "proposals_created_today": 0,
        "alignment_score_avg": None
    }

def save_team_state(state):
    with open(TEAM_STATE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def main():
    print("[SPEACE] Starting Daily Brief generation...")

    # Load state
    state = load_team_state()
    today = datetime.utcnow().strftime("%Y-%m-%d")
    state["last_daily_brief"] = datetime.utcnow().isoformat() + "Z"
    state["team_status"] = "running"

    # In a full implementation, this would trigger each agent to collect fresh data
    # For the testbed, agents can be manual or automated via separate scripts
    print("[SPEACE] Collecting agent reports...")

    # Check which reports exist for today
    reports_today = list(REPORTS_DIR.glob(f"*{today}*.md"))
    if len(reports_today) >= 7:
        state["agent_status"] = {
            "climate": "completed",
            "economics": "completed",
            "governance": "completed",
            "technology": "completed",
            "health": "completed",
            "social": "completed",
            "space": "completed"
        }
        print("[SPEACE] All agents have reported. Ready for synthesis.")
    else:
        print(f"[SPEACE] Only {len(reports_today)}/7 agents reported. Waiting for completion.")
        state["team_status"] = "awaiting_reports"

    # In full implementation: Orchestrator synthesizes Daily Brief here
    # For now, assume human generates synthesis from reports

    save_team_state(state)
    print(f"[SPEACE] Daily Brief cycle complete. Status: {state['team_status']}")

if __name__ == "__main__":
    main()
