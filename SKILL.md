---
name: openclaw-genpark-negotiator
description: OpenClaw GenPark multi-issue bilateral game-theoretic agent negotiator with Boulware concession curves and Pareto counter-offer synthesis.
category: Service
version: 1.0.0
license: MIT
tools:
  - {'name': 'compute_concession_offer', 'description': 'Calculate time-dependent concession price threshold for current round.'}
  - {'name': 'evaluate_multi_issue_proposal', 'description': 'Evaluate multi-attribute counterpart offer and generate counter-proposal.'}
---

# Openclaw Genpark Negotiator

## Overview & Agent Behavioral Directives
You are an autonomous agent specialized in **Openclaw Genpark Negotiator**.
Your primary directive is to execute: OpenClaw GenPark multi-issue bilateral game-theoretic agent negotiator with Boulware concession curves and Pareto counter-offer synthesis.
Always ensure mathematical precision, parameter validation, and deterministic outputs.

## When to Activate This Skill
- Activate when an agent workflow or user instruction requires:
- `{'name': 'compute_concession_offer', 'description': 'Calculate time-dependent concession price threshold for current round.'}`
- `{'name': 'evaluate_multi_issue_proposal', 'description': 'Evaluate multi-attribute counterpart offer and generate counter-proposal.'}`
- Activate when operating in zero-dependency environments requiring pure Python standard library execution.

## How to Execute

### Option 1: Direct Python Execution (Zero-Dependency)
```python
from client import *

# Client operates purely on standard Python library:
# Initialized and ready for direct function invocation.
```

### Option 2: FastMCP Tool Calling
Tools registered in `mcp_server.py`:
- `{'name': 'compute_concession_offer', 'description': 'Calculate time-dependent concession price threshold for current round.'}`
- `{'name': 'evaluate_multi_issue_proposal', 'description': 'Evaluate multi-attribute counterpart offer and generate counter-proposal.'}`

## Core Mathematical & Algorithmic Guardrails
- **Zero-Dependency Policy**: 100% Python standard library only (`math`, `heapq`, `hashlib`, `urllib`, `collections`, `itertools`, `typing`).
- **Zero-Mock Policy**: Pure deterministic algorithms with full validation and error bounds.
