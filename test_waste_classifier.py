import unittest

from waste_classifier import Prediction, pick_waste_bin


class WasteClassifierTests(unittest.TestCase):
    def test_recycling_keyword_wins(self):
        predictions = [
            Prediction("water bottle", 0.7),
            Prediction("beer glass", 0.2),
            Prediction("banana", 0.1),
        ]
        result, _ = pick_waste_bin(predictions)
        self.assertEqual(result, "recycling")

    def test_compost_keyword_wins(self):
        predictions = [Prediction("banana", 0.6), Prediction("leaf beetle", 0.3)]
        result, _ = pick_waste_bin(predictions)
        self.assertEqual(result, "compost")

    def test_default_to_trash(self):
        predictions = [Prediction("space shuttle", 0.9)]
        result, _ = pick_waste_bin(predictions)
        self.assertEqual(result, "trash")


if __name__ == "__main__":
    unittest.main()
