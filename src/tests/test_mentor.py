import unittest
from unittest.mock import patch, MagicMock
from src.mentor import LanguageMentor

class TestLanguageMentor(unittest.TestCase):
    @patch('src.mentor.LLMClient')
    def test_generate_feedback(self, mock_llm):
        """Test feedback generation with mock LLM client"""
        # Setup mock
        mock_client = MagicMock()
        mock_client.generate_response.return_value = "Good practice detected."
        mock_llm.return_value = mock_client
        
        mentor = LanguageMentor('python')
        feedback = mentor.generate_feedback('def hello(): pass')
        
        self.assertEqual(feedback, "Good practice detected.")
        mock_client.generate_response.assert_called_once()
    
    def test_analyze_code_structure(self):
        """Test code structure analysis"""
        mentor = LanguageMentor('python')
        code = """
def hello():
    print("world")
        """
        structure = mentor.analyze_code_structure(code)
        
        self.assertIn('functions', structure)
        self.assertEqual(len(structure['functions']), 1)
        self.assertEqual(structure['functions'][0]['name'], 'hello')

if __name__ == '__main__':
    unittest.main()
