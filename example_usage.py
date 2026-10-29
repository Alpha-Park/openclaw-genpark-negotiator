# -*- coding: utf-8 -*-
from client import OpenClawGenParkNegotiator

def main():
    negotiator = OpenClawGenParkNegotiator(
        reservation_price=100.0,
        target_price=70.0,
        max_rounds=5,
        concession_exponent=0.4 # Boulware strategy
    )
    print("=== OpenClaw GenPark Game-Theoretic Negotiator ===")

    # Simulated negotiation rounds with counterpart seller
    counterpart_proposals = [98.0, 93.0, 88.0, 82.0, 75.0]

    for round_idx, seller_price in enumerate(counterpart_proposals, 1):
        res = negotiator.evaluate_multi_issue_proposal(
            current_round=round_idx,
            counterpart_offer={"price": seller_price, "delivery_days": 5, "warranty_months": 12}
        )
        print(f"Round {round_idx}: Seller=${seller_price} -> Decision={res['decision']} (MyConcession=${res['my_concession_price_threshold']}, Utility={res['total_utility_received']})")
        if res["decision"] == "ACCEPT":
            print("Deal successfully closed!")
            break

if __name__ == "__main__":
    main()
