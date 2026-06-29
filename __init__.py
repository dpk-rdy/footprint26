"""Footprint 26: fan cost and carbon model for the 2026 FIFA World Cup."""
from .model import (
    VENUES, EF, COST, GROUND_THRESHOLD_KM, DM,
    Method, FIFA_STYLE, BOTTOM_UP, ALL_FLY,
    FanItinerary, JourneyResult,
    haversine, build_distance_matrix, leg_emissions, simulate, rollup,
    SEGMENTS, QATAR_REPORTED_MT, TARGET_2030_MT, EURO_FAN,
)

__version__ = "1.0.0"
__all__ = [
    "VENUES", "EF", "COST", "GROUND_THRESHOLD_KM", "DM",
    "Method", "FIFA_STYLE", "BOTTOM_UP", "ALL_FLY",
    "FanItinerary", "JourneyResult",
    "haversine", "build_distance_matrix", "leg_emissions", "simulate", "rollup",
    "SEGMENTS", "QATAR_REPORTED_MT", "TARGET_2030_MT", "EURO_FAN",
]
