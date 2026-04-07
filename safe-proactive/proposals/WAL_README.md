# Write-Ahead Log (WAL) for SafeProactive

All autonomous proposals are logged here BEFORE execution.

## File Naming Convention
WAL_YYYY-MM-DD_HHMMSS_ID.md

## Content Structure
- Proposal ID and timestamp
- Self-Location (ITI + SEA)
- Constraints mapping (validated)
- Push signal details
- Proposed action with reasoning
- Safety assessment (stack level, reversibility)
- Approval status (PENDING/APPROVED/REJECTED/AUTO)
- Outcome log (after execution)

## Integrity
WAL files are append-only. Do not modify after creation.

## Retention
Keep all WAL entries permanently for audit purposes.
Archive old entries to WAL_ARCHIVE/ after 1000 entries.
