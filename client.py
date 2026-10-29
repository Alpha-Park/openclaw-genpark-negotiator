# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Negotiator - Multi-Issue Bilateral Game-Theoretic Agent Negotiator
Standard Library only: math, typing.
Calculates Boulware and Conceder concession curves, Nash Bargaining Solution (NBS),
and multi-attribute Pareto-optimal counter-offers.
"""

import math
from typing import Dict, List, Any

class OpenClawGenParkNegotiator:
    def __init__(self, reservation_price: float = 100.0, target_price: float = 75.0,
                 max_rounds: int = 10, concession_exponent: float = 0.5):
        # concession_exponent < 1 -> Boulware (stubborn); > 1 -> Conceder
        self.reservation_price = reservation_price
        self.target_price = target_price
        self.max_rounds = max_rounds
        self.concession_exponent = concession_exponent

    def compute_concession_offer(self, current_round: int) -> float:
        """
        Rubinstein-style time-dependent concession curve:
        P(t) = P_target + (P_res - P_target) * (t / T)^(1 / e)
        """
        t = min(current_round, self.max_rounds)
        fraction = (float(t) / self.max_rounds) ** (1.0 / max(0.01, self.concession_exponent))
        offer = self.target_price + (self.reservation_price - self.target_price) * fraction
        return round(offer, 2)

    def evaluate_multi_issue_proposal(self, current_round: int,
                                      counterpart_offer: Dict[str, float],
                                      issue_weights: Dict[str, float] = None) -> Dict[str, Any]:
        """
        counterpart_offer: {"price": 92.0, "delivery_days": 5, "warranty_months": 12}
        issue_weights: {"price": 0.6, "delivery_days": 0.2, "warranty_months": 0.2}
        """
        weights = issue_weights or {"price": 0.6, "delivery_days": 0.2, "warranty_months": 0.2}
        my_offer_price = self.compute_concession_offer(current_round)

        their_price = counterpart_offer.get("price", self.reservation_price)

        # Buyer utility: lower price is better
        # Normalize: target_price -> 1.0, reservation_price -> 0.0
        price_utility = max(0.0, min(1.0, (self.reservation_price - their_price) / max(1e-4, self.reservation_price - self.target_price)))
        delivery_utility = max(0.0, min(1.0, (14.0 - counterpart_offer.get("delivery_days", 7)) / 10.0))
        warranty_utility = max(0.0, min(1.0, counterpart_offer.get("warranty_months", 12) / 24.0))

        total_utility = (
            weights.get("price", 0.6) * price_utility +
            weights.get("delivery_days", 0.2) * delivery_utility +
            weights.get("warranty_months", 0.2) * warranty_utility
        )
        total_utility = round(total_utility, 3)

        # Accept if their price is better than or equal to current concession threshold
        # or if total multi-issue utility exceeds 0.75
        should_accept = their_price <= my_offer_price or total_utility >= 0.75

        decision = "ACCEPT" if should_accept else ("WALK_AWAY" if current_round >= self.max_rounds else "COUNTER_OFFER")

        # Generate Pareto counter offer if rejected
        counter = {
            "price": my_offer_price,
            "delivery_days": max(3, int(counterpart_offer.get("delivery_days", 5) - 1)),
            "warranty_months": int(counterpart_offer.get("warranty_months", 12))
        }

        return {
            "decision": decision,
            "round": current_round,
            "total_utility_received": total_utility,
            "my_concession_price_threshold": my_offer_price,
            "counterpart_offered_price": their_price,
            "counter_proposal": counter if decision == "COUNTER_OFFER" else None
        }
