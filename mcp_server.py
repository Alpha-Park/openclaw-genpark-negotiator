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

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            res = run_tool(req.get("name"), req.get("arguments", {}))
            print(json.dumps({"jsonrpc": "2.0", "id": req.get("id"), "result": res}))
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
