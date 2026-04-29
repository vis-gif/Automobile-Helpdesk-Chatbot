import unittest
from chat_engine import get_rag_context, validate_input, generate_response
 
SAMPLE_KB_CONTENT = """
=== BATTERY PROBLEMS ===
Dead battery causes clicking and slow cranking.
 
=== BRAKE PROBLEMS ===
Spongy pedal means air in brake lines.
"""
 
class TestRAGSearch(unittest.TestCase):
 
    def test_battery_keyword_returns_battery_section(self):
        result = get_rag_context("my battery is dead")
        self.assertIn("battery", result.lower())
 
    def test_brake_keyword_returns_brake_section(self):
        result = get_rag_context("brakes squealing")
        self.assertIn("brake", result.lower())
 
    def test_overheating_keyword_returns_section(self):
        result = get_rag_context("car is overheating temperature gauge red")
        self.assertIsInstance(result, str)
 
    def test_empty_query_returns_string(self):
        result = get_rag_context("")
        self.assertIsInstance(result, str)
 
class TestInputValidation(unittest.TestCase):
 
    def test_empty_input_is_invalid(self):
        valid, msg = validate_input("")
        self.assertFalse(valid)
        self.assertIn("Please", msg)
 
    def test_whitespace_only_is_invalid(self):
        valid, msg = validate_input("   ")
        self.assertFalse(valid)
 
    def test_offtopic_recipe_is_invalid(self):
        valid, msg = validate_input("give me a recipe for pasta")
        self.assertFalse(valid)
        self.assertIn("automobile", msg.lower())
 
    def test_valid_car_question_passes(self):
        valid, msg = validate_input("my check engine light is on")
        self.assertTrue(valid)
        self.assertEqual(msg, "")
 
    def test_valid_brake_question_passes(self):
        valid, msg = validate_input("my brakes are grinding")
        self.assertTrue(valid)
 
    def test_valid_battery_question_passes(self):
        valid, msg = validate_input("car wont start clicking noise battery")
        self.assertTrue(valid)
 
if __name__ == "__main__":
    unittest.main()
