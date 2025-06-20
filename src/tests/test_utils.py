import unittest
from src.utils import validate_language, sanitize_input

class TestUtils(unittest.TestCase):
    def test_validate_language_supported(self):
        """Test that supported languages are validated correctly"""
        self.assertTrue(validate_language('python'))
        self.assertTrue(validate_language('javascript'))
    
    def test_validate_language_unsupported(self):
        """Test that unsupported languages are rejected"""
        self.assertFalse(validate_language('fortran'))
        self.assertFalse(validate_language(''))
    
    def test_sanitize_input(self):
        """Test input sanitization removes harmful patterns"""
        test_cases = [
            ("normal input", "normal input"),
            ("<script>alert('xss')</script>", "alert('xss')"),
            ("import os; os.system('rm -rf')", "os.system('rm -rf')"),
            ("SELECT * FROM users", "SELECT * FROM users")
        ]
        
        for input_str, expected in test_cases:
            with self.subTest(input_str=input_str):
                self.assertEqual(sanitize_input(input_str), expected)

if __name__ == '__main__':
    unittest.main()
