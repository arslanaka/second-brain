import unittest
from unittest.mock import MagicMock, patch
from src.processor import StructureEngine
from src.models import StructuredOutput, StructuredItem, ThoughtCategory, UrgencyLevel, EffortLevel, Timeframe

class TestStructureEngine(unittest.TestCase):
    def setUp(self):
        self.mock_response = StructuredOutput(
            items=[
                StructuredItem(
                    title="Buy Milk",
                    description="Go to the store and get whole milk",
                    category=ThoughtCategory.TASK,
                    urgency=UrgencyLevel.HIGH,
                    effort=EffortLevel.SMALL,
                    timeframe=Timeframe.TODAY,
                    dependencies=[],
                    clarity_score=100,
                    next_step="Go to store"
                )
            ]
        )

    @patch("src.llm_client.OpenAI")
    def test_process_thought(self, mock_openai):
        # Mock the parsing response
        mock_client_instance = MagicMock()
        mock_openai.return_value = mock_client_instance
        
        mock_completion = MagicMock()
        mock_completion.choices[0].message.parsed = self.mock_response
        mock_client_instance.beta.chat.completions.parse.return_value = mock_completion

        # Initialize engine with a dummy key
        engine = StructureEngine(api_key="dummy-key")
        
        # Test processing
        result = engine.process_thought("Buy milk")
        
        self.assertIsInstance(result, StructuredOutput)
        self.assertEqual(len(result.items), 1)
        self.assertEqual(result.items[0].title, "Buy Milk")
        self.assertEqual(result.items[0].category, ThoughtCategory.TASK)

if __name__ == "__main__":
    unittest.main()
