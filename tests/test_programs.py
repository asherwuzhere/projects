import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProgramTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exponents = load_module(
            "large_exponent_calc", "Other Projects/large_exponent_calc.py"
        )
        cls.roman = load_module("roman_numeral", "Other Projects/roman_numeral.py")
        cls.poker = load_module("poker_bot", "Game Bots/poker_bot.py")
        cls.sorter = load_module("file_sorter_bot", "Game Bots/file_sorter_bot.py")

    def test_scientific_power(self):
        self.assertEqual(self.exponents.scientific_power(2.0, 10.0), (1.024, 3))
        self.assertEqual(self.exponents.scientific_power(10.0, 0.0), (1.0, 0))
        self.assertEqual(self.exponents.scientific_power(0.0, 3.0), (0.0, 0))

    def test_roman_round_trip(self):
        self.assertEqual(self.roman.RomanNumerals.int_to_roman(1994), "MCMXCIV")
        self.assertEqual(self.roman.RomanNumerals.roman_to_int("MCMXCIV"), 1994)
        with self.assertRaises(ValueError):
            self.roman.RomanNumerals.roman_to_int("IIII")

    def test_poker_input_and_pair_detection(self):
        self.assertFalse(self.poker.validate_hand_input(["ah", "ah"]))
        self.assertEqual(
            self.poker.evaluate_hand_with_community(
                ["ah", "kc"], ["ad", "2s", "3h"]
            ),
            "Pair or Two Pair",
        )

    def test_file_sorter(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "sample_bot.py"
            source.write_text("print('ok')\n", encoding="utf-8")
            self.sorter.sort_python_files(temp_dir)
            self.assertTrue((Path(temp_dir) / "Bot" / source.name).exists())


if __name__ == "__main__":
    unittest.main()
