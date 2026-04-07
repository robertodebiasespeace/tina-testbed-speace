---
name: safe-proactive
version: 1.1.0
description: Framework per agenti autonomi sicuri con Write-Ahead Logging, Proposal-First e human approval gates.
maintainer: Roberto De Biase
license: MIT
tags: [safety, wal, approval, audit, alignment]
---

# SafeProactive v1.1

SafeProactive è il guardiano di SPEACE. Ogni azione autonoma segue il protocollo Safe-WAL:
1. Self-Location (SMFOI)
2. Constraint Mapping
3. Push Detection + Semantic Validation
4. Proposal Generation
5. Write-Ahead Log
6. Human Approval (Level 2+)
7. Execution
8. Outcome Logging + Intrinsic Learning

Livelli di rischio:
- Level 0 (Integrity): auto
- Level 1 (Exploration): auto (read-only)
- Level 2 (Expansion): human approval
- Level 3 (Recursion): human + simulation

Integra nativamente con DigitalDNA e SMFOI-KERNEL.