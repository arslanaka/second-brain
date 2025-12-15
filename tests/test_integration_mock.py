import unittest
from unittest.mock import MagicMock, patch
from src.processor import StructureEngine
from src.models import StructuredOutput, StructuredItem, ThoughtCategory, UrgencyLevel, EffortLevel, Timeframe, EnergyLevel, Context
from src.vector_store import VectorStore
import time

class TestIntegrationMock(unittest.TestCase):
    def setUp(self):
        # Ensure Qdrant is reachable (we assume docker-compose up is run)
        self.vector_store = VectorStore(host="localhost", port=6333)
        # Clean collection for test
        try:
            self.vector_store.client.delete_collection("thoughts")
        except:
            pass
        self.vector_store._ensure_collection_exists()

    @patch("src.llm_client.OpenAI")
    @patch("src.embedding_service.OpenAI")
    def test_end_to_end_flow(self, mock_emb_openai, mock_llm_openai):
        # 1. Mock LLM Response
        mock_output = StructuredOutput(
            items=[
                StructuredItem(
                    title="Walk the dog",
                    description="Take the dog for a walk in the park",
                    category=ThoughtCategory.TASK,
                    urgency=UrgencyLevel.HIGH,
                    importance=8,
                    energy_level=EnergyLevel.MEDIUM,
                    context_tags=[Context.HOME, Context.ANYWHERE],
                    effort=EffortLevel.SMALL,
                    timeframe=Timeframe.TODAY,
                    dependencies=[],
                    clarity_score=100,
                    next_step="Get the leash"
                )
            ]
        )
        mock_completion = MagicMock()
        mock_completion.choices[0].message.parsed = mock_output
        mock_llm_openai.return_value.beta.chat.completions.parse.return_value = mock_completion

        # 2. Mock Embedding Response
        # Return a dummy 1536-dim vector
        dummy_vector = [0.1] * 1536
        mock_emb_response = MagicMock()
        mock_emb_response.data[0].embedding = dummy_vector
        mock_emb_openai.return_value.embeddings.create.return_value = mock_emb_response

        # 3. Run Engine
        engine = StructureEngine(api_key="dummy")
        result = engine.process_thought("Walk the dog")
        
        # 4. Verify Output
        self.assertEqual(result.items[0].title, "Walk the dog")

        # 5. Verify Storage (Wait a bit for async indexing if any, though upsert is usually sync)
        time.sleep(1)
        search_results = engine.search_thoughts("dog")
        
        # Since we mocked embedding for search too (it uses the same service), 
        # it will return the same dummy vector, which should match the stored one.
        self.assertTrue(len(search_results) > 0)
        self.assertEqual(search_results[0]['title'], "Walk the dog")

if __name__ == "__main__":
    unittest.main()
