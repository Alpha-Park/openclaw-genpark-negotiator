# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkNegotiator

negotiator = OpenClawGenParkNegotiator()

def run_tool(name, args):
    if name == "compute_concession_offer":
        r = int(args.get("current_round", 1))
        return {"offered_price": negotiator.compute_concession_offer(r)}
    elif name == "evaluate_multi_issue_proposal":
        r = int(args.get("current_round", 1))
        offer = args.get("counterpart_offer", {})
        w = args.get("issue_weights", None)
        return negotiator.evaluate_multi_issue_proposal(r, offer, w)
    else:
        raise ValueError(f"Unknown tool: {name}")

from typing import Any, Dict, List, Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:
    raise SystemExit("MCP requires the mcp package. Run: python -m pip install -r requirements.txt") from exc

mcp = FastMCP('openclaw-genpark-negotiator')

@mcp.tool()
def compute_concession_offer(current_round: int = 1) -> str:
    """Compute the next concession offer."""
    return json.dumps(run_tool('compute_concession_offer', {'current_round': current_round}))

@mcp.tool()
def evaluate_multi_issue_proposal(current_round: int = 1, counterpart_offer: Optional[Dict[str, float]] = None, issue_weights: Optional[Dict[str, float]] = None) -> str:
    """Evaluate a supplied multi-issue negotiation proposal."""
    return json.dumps(run_tool('evaluate_multi_issue_proposal', {'current_round': current_round, 'counterpart_offer': counterpart_offer if counterpart_offer is not None else {}, 'issue_weights': issue_weights}))

def main():
    if "--test" in sys.argv:
        print("[TEST] Running OpenClaw Negotiator Self-Test...")
        p1 = negotiator.compute_concession_offer(0)
        p2 = negotiator.compute_concession_offer(10)
        assert p1 <= p2
        res = negotiator.evaluate_multi_issue_proposal(1, {"price": 76.0, "delivery_days": 4, "warranty_months": 12})
        assert res["decision"] == "ACCEPT"
        print("[TEST] All tests passed successfully!")
        return

    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
