"""Image-based waste sorting helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple


@dataclass
class Prediction:
    """Top prediction from an image classifier."""

    label: str
    confidence: float


KEYWORD_TO_BIN: Dict[str, Sequence[str]] = {
    "recycling": (
        "bottle",
        "can",
        "carton",
        "cardboard",
        "paper",
        "newspaper",
        "magazine",
        "box",
        "jar",
        "plastic",
        "glass",
        "aluminum",
        "tin",
        "container",
    ),
    "compost": (
        "banana",
        "apple",
        "orange",
        "lemon",
        "vegetable",
        "broccoli",
        "cabbage",
        "mushroom",
        "pumpkin",
        "corn",
        "food",
        "bread",
        "egg",
        "leaf",
        "plant",
        "flower",
    ),
    "trash": (
        "diaper",
        "cigarette",
        "toothbrush",
        "sponge",
        "rag",
        "styrofoam",
        "foam",
        "chip",
        "candy",
        "wrapper",
        "battery",
        "lightbulb",
    ),
}


def pick_waste_bin(predictions: Iterable[Prediction]) -> Tuple[str, str]:
    """Return a bin recommendation and explanation from classifier predictions."""
    scored_bins = {"recycling": 0.0, "compost": 0.0, "trash": 0.0}
    details: List[str] = []

    for prediction in predictions:
        label = prediction.label.lower()
        for waste_bin, keywords in KEYWORD_TO_BIN.items():
            if any(keyword in label for keyword in keywords):
                scored_bins[waste_bin] += prediction.confidence
                details.append(f"{prediction.label} → {waste_bin}")

    if not details:
        return (
            "trash",
            "I couldn't confidently match this item to recycling or compost, so trash is the safest default.",
        )

    best_bin = max(scored_bins, key=scored_bins.get)
    reason = (
        f"Matched model labels ({'; '.join(details)}) with highest score for **{best_bin}**. "
        "Always verify with local city rules."
    )
    return best_bin, reason
