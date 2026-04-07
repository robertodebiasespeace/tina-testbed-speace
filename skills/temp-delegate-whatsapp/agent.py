#!/usr/bin/env python3
"""
Temporary Delegate WhatsApp Agent — handles messages during active delegation.
Runs as a sub-agent, receives messages from main session, executes under SafeProactive auto-approve rules.
"""

import os
import json
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
import logging

WORKSPACE = Path(__file__).resolve().parents[2]
SAFE_PROACTIVE_DIR = WORKSPACE / "safe-proactive"
LOGS_DIR = WORKSPACE / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Setup logging to both file and stdout for debugging
logging.basicConfig(
    filename=LOGS_DIR / "delegated_actions.log",
    level=logging.INFO,
    format="%(message)s"
)
logger = logging.getLogger("delegate")

def load_rules():
    rules_path = SAFE_PROACTIVE_DIR / "auto-rules.json"
    with open(rules_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_rules(rules):
    rules_path = SAFE_PROACTIVE_DIR / "auto-rules.json"
    with open(rules_path, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2)

def is_delegation_active(rules):
    state = rules["delegation_state"]
    if not state["enabled"]:
        return False
    expires = datetime.fromisoformat(state["expires_at"].replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    if now > expires:
        # Auto-expire
        state["enabled"] = False
        state["expires_at"] = None
        state["activated_at"] = None
        state["activated_by"] = None
        state["mode"] = None
        rules["active_rules"] = []
        save_rules(rules)
        logger.info(json.dumps({"timestamp": now.isoformat(), "event": "delegation_auto_expired"}))
        return False
    return True

def log_action(rule_id, action, chain=None, amount_usd=None, outcome=None, tx_hash=None, extra=None):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec='seconds'),
        "rule_id": rule_id,
        "action": action,
        "chain": chain,
        "amount_usd": amount_usd,
        "outcome": outcome,
        "tx_hash": tx_hash,
        "extra": extra or {}
    }
    print(json.dumps(entry))  # stdout for parent session
    logger.info(json.dumps(entry))

def match_rule(operation_type, context, rules):
    """Find first active rule that matches the operation and conditions."""
    global_limits = rules["global_limits"]
    active_rule_ids = rules["active_rules"]
    for rule in rules["rules"]:
        if rule["id"] not in active_rule_ids:
            continue
        if rule["trigger"] != operation_type:
            continue

        # Evaluate conditions
        conds = rule["conditions"]
        # Chain check
        if "chain" in conds:
            if context.get("chain") != conds["chain"]:
                continue
        # Amount limits (USD or ETH)
        if "max_amount_usd" in conds:
            amt = context.get("amount_usd", 0)
            if amt > conds["max_amount_usd"]:
                continue
        if "max_amount_eth" in conds:
            eth_amt = context.get("amount_eth", 0)
            if eth_amt > conds["max_amount_eth"]:
                continue
        # Token symbols
        if "token_symbols" in conds:
            token = context.get("token", "").upper()
            if token not in [s.upper() for s in conds["token_symbols"]]:
                continue
        # Protocol triggers
        if "protocols" in conds:
            proto = context.get("protocol", "").lower()
            if proto not in [p.lower() for p in conds["protocols"]]:
                continue
        # Unlimited approve safeguard
        if conds.get("unlimited_approve") is False:
            if context.get("unlimited", False):
                continue

        return rule
    return None

def execute_operation(rule, context):
    """Dispatch to appropriate executor based on rule trigger."""
    trigger = rule["trigger"]
    # These are stubs — real implementation would call onchainos CLI
    outcome = "simulated_executed"
    tx_hash = f"0xSIMULATED_{int(time.time())}"
    details = {}

    if trigger == "yield_opportunity":
        # Stub: call onchainos for yield farming on X Layer
        details = {"protocol": context.get("protocol", "xlayer-staking"), "amount_usd": context.get("amount_usd", 25)}
        log_action(rule["id"], "yield_execute", chain=196, amount_usd=details["amount_usd"], outcome=outcome, tx_hash=tx_hash, extra=details)
        return {"ok": True, "tx_hash": tx_hash, "message": f"Yield executed: {details['amount_usd']} USD via {details['protocol']}."}

    elif trigger == "balance_inquiry":
        # Stub: call onchainos wallet balance
        result = {"totalValueUsd": "0.00", "accounts": []}
        log_action(rule["id"], "balance_check", outcome=outcome)
        return {"ok": True, "data": result, "message": "Balance checked."}

    elif trigger == "token_approve":
        # Stub: token approval
        token = context.get("token", "USDC")
        amount = context.get("amount_usd", 10)
        details = {"token": token, "amount_usd": amount}
        log_action(rule["id"], "token_approve", chain=196, amount_usd=amount, outcome=outcome, tx_hash=tx_hash, extra=details)
        return {"ok": True, "tx_hash": tx_hash, "message": f"Approved {amount} {token}."}

    elif trigger == "monitoring_check":
        # Stub: run monitoring scan
        log_action(rule["id"], "monitoring_scan", outcome=outcome)
        return {"ok": True, "message": "Monitoring scan completed."}

    else:
        return {"ok": False, "message": f"Unknown trigger: {trigger}"}

def process_message(msg_text):
    """Main entry: process a WhatsApp message string during delegation."""
    rules = load_rules()
    text = msg_text.strip().upper()

    # Lifecycle commands (always handled, even if delegation not active? Usually handled by main agent, but we also respond when active)
    if text in ("STOP DELEGATE", "REVOKE", "DISABLE DELEGATE"):
        # Deactivate immediately
        rules["delegation_state"]["enabled"] = False
        rules["delegation_state"]["expires_at"] = None
        rules["delegation_state"]["activated_at"] = None
        rules["delegation_state"]["activated_by"] = None
        rules["delegation_state"]["mode"] = None
        rules["active_rules"] = []
        save_rules(rules)
        log_action("system", "delegation_deactivated", outcome="user_command")
        return "✅ Delega disattivata immediatamente."

    if text == "DELEGATE STATUS":
        state = rules["delegation_state"]
        if not state["enabled"]:
            return "🔴 Delega non attiva."
        now = datetime.now(timezone.utc)
        exp = datetime.fromisoformat(state["expires_at"].replace("Z", "+00:00"))
        remaining = (exp - now).total_seconds() / 60
        response = [
            f"🟢 Delega ATTIVA — Mode: {state['mode']}",
            f"⏳ Scade tra: {int(remaining)} minuti",
            f"👤 Attivata da: {state['activated_by']}",
            f"📋 Regole attive: {', '.join(rules['active_rules']) if rules['active_rules'] else 'nessuna'}"
        ]
        return "\n".join(response)

    # Check delegation state
    if not is_delegation_active(rules):
        return None  # Not our business; main agent handles

    # Parse intent from message
    # Simple keyword matching for demo; real version would use NLP
    context = {"chain": 196}  # Default to X Layer

    # Determine operation type
    operation = None
    if any(k in text for k in ("BALANCE", "SALDO", "PORTFOLIO")):
        operation = "balance_inquiry"
    elif any(k in text for k in ("YIELD", "FARM", "STAKE", "STAKING")):
        operation = "yield_opportunity"
        # Attempt to extract amount
        context["amount_usd"] = 25  # default stub
        context["protocol"] = "xlayer-staking"
    elif "APPROVE" in text:
        operation = "token_approve"
        context["token"] = "USDC"
        context["amount_usd"] = 10
    elif any(k in text for k in ("MONITOR", "SCAN", "CHECK")):
        operation = "monitoring_check"
    else:
        return f"🤖 Delega attiva. Messaggio non riconosciuto: \"{msg_text}\". In attesa di tua conferma."

    # Match rule
    rule = match_rule(operation, context, rules)
    if rule:
        # Execute under rule
        result = execute_operation(rule, context)
        if result["ok"]:
            return f"✅ Operazione自动 autorizzata da regola `{rule['id']}`.\n{result['message']}"
        else:
            return f"❌ Esecuzione fallita: {result['message']}"
    else:
        return f"⚠️ Nessuna regola attiva per questa operazione. Richiesta conferma umana."

# --- Agent entry point ---
def main():
    # In real usage, this agent would be spawned by OpenClaw and receive messages via sessions_send
    # Here we simulate reading from stdin or process arguments
    if len(sys.argv) > 1:
        msg = " ".join(sys.argv[1:])
        resp = process_message(msg)
        if resp:
            print(resp)
    else:
        # Interactive test mode
        print("Delegated WhatsApp Agent (test mode). Type 'quit' to exit.")
        while True:
            try:
                line = input(">> ")
                if line.strip().lower() in ("quit", "exit"):
                    break
                resp = process_message(line)
                if resp:
                    print(resp)
            except (EOFError, KeyboardInterrupt):
                break

if __name__ == "__main__":
    main()
