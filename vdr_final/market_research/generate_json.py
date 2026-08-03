#!/usr/bin/env python3
"""
Market Intelligence Data Generator
=====================================
Main entry point for generating comparables.json from all data sources.

Combines data from:
- AirROI (primary source for La Vega)
- AirDNA (market-level data)
- Booking.com (hotel comparables)
- Airbnb (vacation rental comparables)
- Manual curation (international benchmarks)

Outputs: comparables.json with ranked similarity scores.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.airbnb_scraper import AirbnbScraper
from scraper.booking_scraper import BookingScraper
from comparator.comparator import SimilarityComparator


def load_airroi_data():
    """Load AirROI data for La Vega."""
    airroi_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "airroi_data.json"
    )
    if os.path.exists(airroi_path):
        with open(airroi_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def load_airdna_data():
    """Load AirDNA data for La Vega market."""
    airdna_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "airdna_data.json"
    )
    if os.path.exists(airdna_path):
        with open(airdna_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def build_database():
    """Build the complete comparable property database."""
    db = []

    # Add Airbnb data
    airbnb = AirbnbScraper()
    db.extend(airbnb.search_properties())

    # Add Booking data
    booking = BookingScraper()
    db.extend(booking.search_properties())

    # Add AirROI data if available
    airroi = load_airroi_data()
    if airroi and "properties" in airroi:
        for p in airroi["properties"]:
            db.append(
                {
                    "id": f"airroi_{p['name'].lower().replace(' ', '_')}",
                    "name": p["name"],
                    "platform": "AirROI",
                    "url": "",
                    "latitude": 0.0,
                    "longitude": 0.0,
                    "distance_km": 0.0,
                    "municipality": "La Vega",
                    "country": "Colombia",
                    "rooms": p.get("rooms", 0),
                    "capacity": 0,
                    "type": "Villa",
                    "area_sqm": 0.0,
                    "adr_usd": p.get("adr_usd", 0),
                    "occupancy_percent": p.get("occupancy_percent", 0),
                    "revpar_usd": 0.0,
                    "rating": 0.0,
                    "num_reviews": 0,
                    "has_pool": False,
                    "has_jacuzzi": False,
                    "has_restaurant": False,
                    "has_spa": False,
                    "architecture_style": "modern",
                    "view_type": "mountain",
                    "nature_immersion": 0.7,
                    "luxury_level": 0.7,
                    "year_built_or_renovated": 0,
                    "source": "AirROI",
                    "notes": p.get("notes", ""),
                }
            )

    # Add international benchmarks (Level 3)
    international = [
        {
            "id": "intl_nosara",
            "name": "Nosara Eco Lodge",
            "platform": "Booking",
            "url": "https://www.booking.com/hotel/cr/nosara-eco-lodge",
            "latitude": 10.0,
            "longitude": -85.0,
            "distance_km": 9999,
            "municipality": "Nosara",
            "country": "Costa Rica",
            "rooms": 8,
            "capacity": 16,
            "type": "Eco Lodge",
            "area_sqm": 300.0,
            "adr_usd": 280.0,
            "occupancy_percent": 65.0,
            "revpar_usd": 182.0,
            "rating": 9.2,
            "num_reviews": 312,
            "has_pool": True,
            "has_jacuzzi": True,
            "has_restaurant": True,
            "has_spa": True,
            "architecture_style": "rustic",
            "view_type": "forest",
            "nature_immersion": 0.95,
            "luxury_level": 0.82,
            "year_built_or_renovated": 2021,
            "source": "Booking",
            "notes": "Regenerative eco-luxury benchmark in Costa Rica.",
        },
        {
            "id": "intl_uvita",
            "name": "Uvita Boutique Hotel",
            "platform": "Booking",
            "url": "https://www.booking.com/hotel/cr/uvita-boutique",
            "latitude": 9.0,
            "longitude": -84.0,
            "distance_km": 9999,
            "municipality": "Uvita",
            "country": "Costa Rica",
            "rooms": 10,
            "capacity": 20,
            "type": "Boutique Hotel",
            "area_sqm": 450.0,
            "adr_usd": 320.0,
            "occupancy_percent": 58.0,
            "revpar_usd": 185.6,
            "rating": 9.1,
            "num_reviews": 278,
            "has_pool": True,
            "has_jacuzzi": False,
            "has_restaurant": True,
            "has_spa": True,
            "architecture_style": "modern",
            "view_type": "ocean",
            "nature_immersion": 0.90,
            "luxury_level": 0.85,
            "year_built_or_renovated": 2022,
            "source": "Booking",
            "notes": "Luxury beachfront boutique in Costa Rica.",
        },
        {
            "id": "intl_tulum",
            "name": "Tulum Regenerative Hotel",
            "platform": "Booking",
            "url": "https://www.booking.com/hotel/mx/tulum-regenerative",
            "latitude": 20.0,
            "longitude": -87.0,
            "distance_km": 9999,
            "municipality": "Tulum",
            "country": "Mexico",
            "rooms": 15,
            "capacity": 30,
            "type": "Boutique Hotel",
            "area_sqm": 500.0,
            "adr_usd": 420.0,
            "occupancy_percent": 72.0,
            "revpar_usd": 302.4,
            "rating": 9.3,
            "num_reviews": 456,
            "has_pool": True,
            "has_jacuzzi": True,
            "has_restaurant": True,
            "has_spa": True,
            "architecture_style": "modern",
            "view_type": "beach",
            "nature_immersion": 0.93,
            "luxury_level": 0.92,
            "year_built_or_renovated": 2023,
            "source": "Booking",
            "notes": "Premium regenerative luxury benchmark.",
        },
    ]
    db.extend(international)

    return db


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    # Build database
    print("Building comparable property database...")
    db = build_database()
    print(f"  Total properties: {len(db)}")

    # Calculate similarity scores
    print("Calculating similarity scores...")
    comparator = SimilarityComparator()
    ranked = comparator.rank(db, top_n=8)

    # Generate report
    print("Generating market report...")
    report = comparator.generate_report(ranked)

    # Save comparables.json
    output_path = os.path.join(output_dir, "comparables.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"  Generated: {output_path}")

    # Save full database
    db_path = os.path.join(output_dir, "full_database.json")
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    print(f"  Generated: {db_path}")

    # Print top comparables
    print("\nTop 8 Comparables:")
    for i, prop in enumerate(ranked, 1):
        print(
            f"  {i}. {prop['name']} — {prop['similarity_score']}% similarity — ADR: USD {prop.get('adr_usd', 'N/A')}"
        )


if __name__ == "__main__":
    main()