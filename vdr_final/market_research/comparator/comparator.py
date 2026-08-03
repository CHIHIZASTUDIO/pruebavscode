"""
Similarity Comparator Engine
==============================
Calculates similarity scores between La Nuit and comparable properties
using weighted multi-factor analysis.

Scoring weights:
- Luxury Level: 25%
- Architecture Match: 20%
- Nature Immersion: 20%
- Property Size: 15%
- Amenities: 10%
- Distance: 10%
"""

import json
from typing import List, Dict, Optional


class SimilarityComparator:
    """Calculates similarity scores for comparable properties."""

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or {
            "luxury_level": 0.25,
            "architecture_match": 0.20,
            "nature_immersion": 0.20,
            "property_size": 0.15,
            "amenities": 0.10,
            "distance": 0.10,
        }

        # La Nuit reference profile
        self.la_nuit_profile = {
            "luxury_level": 0.90,
            "architecture_style": "modern",
            "nature_immersion": 0.95,
            "area_sqm": 250.0,
            "has_pool": True,
            "has_jacuzzi": True,
            "has_restaurant": True,
            "has_spa": True,
            "rooms": 12,
            "type": "Boutique Hotel",
        }

    def calculate_similarity(self, property_data: Dict) -> Dict:
        """
        Calculate similarity score for a single property.

        Returns:
            Dict with property data and similarity score
        """
        scores = {}

        # Luxury Level (25%)
        scores["luxury_level"] = self._score_luxury(property_data)

        # Architecture Match (20%)
        scores["architecture_match"] = self._score_architecture(property_data)

        # Nature Immersion (20%)
        scores["nature_immersion"] = self._score_nature(property_data)

        # Property Size (15%)
        scores["property_size"] = self._score_size(property_data)

        # Amenities (10%)
        scores["amenities"] = self._score_amenities(property_data)

        # Distance (10%)
        scores["distance"] = self._score_distance(property_data)

        # Weighted total
        total = sum(
            scores[key] * self.weights[key] for key in self.weights
        )

        result = dict(property_data)
        result["similarity_score"] = round(total * 100, 1)
        result["score_breakdown"] = {
            k: round(v * 100, 1) for k, v in scores.items()
        }

        return result

    def _score_luxury(self, prop: Dict) -> float:
        """Score based on luxury level (0-1)."""
        prop_luxury = prop.get("luxury_level", 0.5)
        return min(prop_luxury / self.la_nuit_profile["luxury_level"], 1.0)

    def _score_architecture(self, prop: Dict) -> float:
        """Score based on architecture style match."""
        prop_arch = prop.get("architecture_style", "")
        target_arch = self.la_nuit_profile["architecture_style"]
        if prop_arch == target_arch:
            return 1.0
        # Partial match for similar styles
        modern_styles = ["modern", "minimalist", "contemporary"]
        rustic_styles = ["rustic", "colonial", "traditional"]
        if prop_arch in modern_styles and target_arch in modern_styles:
            return 0.8
        if prop_arch in rustic_styles and target_arch in rustic_styles:
            return 0.7
        return 0.4

    def _score_nature(self, prop: Dict) -> float:
        """Score based on nature immersion level."""
        prop_nature = prop.get("nature_immersion", 0.5)
        target_nature = self.la_nuit_profile["nature_immersion"]
        return min(prop_nature / target_nature, 1.0)

    def _score_size(self, prop: Dict) -> float:
        """Score based on property size similarity."""
        prop_size = prop.get("area_sqm", 100.0)
        target_size = self.la_nuit_profile["area_sqm"]
        ratio = min(prop_size, target_size) / max(prop_size, target_size)
        return ratio

    def _score_amenities(self, prop: Dict) -> float:
        """Score based on amenity match."""
        target_amenities = [
            "has_pool",
            "has_jacuzzi",
            "has_restaurant",
            "has_spa",
        ]
        matches = 0
        total = len(target_amenities)
        for amenity in target_amenities:
            if prop.get(amenity, False) == self.la_nuit_profile.get(amenity, False):
                matches += 1
        return matches / total if total > 0 else 0.5

    def _score_distance(self, prop: Dict) -> float:
        """Score based on distance (closer = higher score)."""
        distance = prop.get("distance_km", 100.0)
        if distance <= 20:
            return 1.0
        elif distance <= 50:
            return 0.8
        elif distance <= 100:
            return 0.6
        else:
            return 0.3

    def rank(
        self, properties: List[Dict], top_n: int = 8
    ) -> List[Dict]:
        """
        Rank properties by similarity score.

        Args:
            properties: List of property dictionaries
            top_n: Number of top results to return

        Returns:
            Sorted list of properties with similarity scores
        """
        scored = [self.calculate_similarity(p) for p in properties]
        scored.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored[:top_n]

    def generate_report(self, ranked: List[Dict]) -> Dict:
        """
        Generate a summary report from ranked comparables.

        Returns:
            Dict with summary statistics and top comparables
        """
        if not ranked:
            return {"total": 0, "top_comparables": []}

        adrs = [p.get("adr_usd", 0) for p in ranked if p.get("adr_usd")]
        occupancies = [
            p.get("occupancy_percent", 0) for p in ranked if p.get("occupancy_percent")
        ]

        return {
            "total_properties": len(ranked),
            "top_comparables": ranked,
            "market_avg_adr": round(sum(adrs) / len(adrs), 2) if adrs else 0,
            "market_avg_occupancy": round(sum(occupancies) / len(occupancies), 1) if occupancies else 0,
            "la_nuit_projected_adr": 357,
            "la_nuit_projected_occupancy": 55,
        }