---
name: delegated-whatsapp-agent
description: "Temporary delegate agent for WhatsApp. Handles confirmations, yield opportunities, and routine operations under SafeProactive auto-approve rules. TTL-limited, revocable, fully logged."
license: MIT
metadata:
  author: SPEACE
  version: "1.0.0"
  dependencies: ["safe-proactive", "digitaldna"]
---

# Delegated WhatsApp Agent

Temporary delegate for handling WhatsApp messages on behalf of the human overseer when delegation is active.

## Purpose

Receives and processes WhatsApp messages during active delegation periods. Can:
- Auto-approve operations matching active SafeProactive rules
- Forward high-risk/unknown requests to the human overseer
- Handle delegation lifecycle commands

## Activation / Deactivation

### Activate Delegation
- `ENABLE TEMPORARY DELEGATE` → activates default rules for 30 min (yield + routine)
- `ENABLE DELEGATE FOR YIELD` → activates only yield rules for 30 min
- `ENABLE DELEGATE FOR ROUTINE` → activates only routine rules for 30 min

### Check Status
- `DELEGATE STATUS` → shows active rules, TTL remaining, mode

### Deactivate Delegation (Human Override)
- `STOP DELEGATE` → immediate revocation
- `REVOKE` → immediate revocation
- `DISABLE DELEGATE` → immediate revocation

## Delegation State

Delegation is tracked in `safe-proactive/auto-rules.json`:

```json
{
  "delegation_state": {
    "enabled": true,
    "expires_at": "2026-04-07T10:00:00+02:00",
    "activated_at": "2026-04-07T09:30:00+02:00",
    "activated_by": "robertodebiase@outlook.it",
    "mode": "yield+routine"
  }
}
```

## Processing Flow

When a WhatsApp message arrives:

1. **Check delegation state**: Is delegation active? TTL expired?
2. **Parse command**: Is it a lifecycle command (`ENABLE`, `STOP`, `STATUS`)?
3. **Check rules**: Does the operation match an active auto-approve rule?
   - If **yes** → execute, log action, notify overseer
   - If **no** → forward to human overseer with context
4. **Log everything**: Every decision/action goes to `logs/delegated_actions.log`

## Safety Constraints

- **TTL enforcement**: Never extend beyond `max_ttl_minutes` (60 min). Default is 30 min.
- **Chain restriction**: Only X Layer (chainId 196). No Ethereum mainnet, no Solana, no cross-chain.
- **Amount limits**: Max $100 USD or 0.01 ETH per operation.
- **No CEX access**: Never use OKX CEX API in delegated mode.
- **No unlimited approvals**: Token approves are capped at the rule's amount limit.
- **Human always supersedes**: If the human sends any message, they are back in control temporarily.
- **Rollback support**: Where possible, transactions are reversible.

## Logging Format

All actions are logged to `logs/delegated_actions.log` in JSON lines format:

```json
{"timestamp": "2026-04-07T09:35:00+02:00", "rule_id": "yield_xlayer_small", "action": "stake_eth", "chain": 196, "amount_usd": 25, "outcome": "executed", "tx_hash": "0x..."}
```

## Edge Cases

- **TTL expires mid-operation**: Complete the current operation, then disable. Do not start new ones.
- **Conflicting commands**: If both `STOP DELEGATE` and `ENABLE` arrive, `STOP DELEGATE` always wins.
- **Human message during delegation**: Pauses delegation for the duration of the conversation. Resumes after inactivity if TTL hasn't expired.
- **Multiple delegate activations**: Only one active at a time. New activation resets TTL.

## Files

- `safe-proactive/auto-rules.json` — rule definitions and delegation state
- `logs/delegated_actions.log` — audit log
- `digitaldna/traits/delegated-autonomy.json` — DNA trait for mutations
