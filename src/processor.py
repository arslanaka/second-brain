from .llm_client import LLMClient
from .prompt_manager import PromptManager
from .models import StructuredOutput, StructuredItem
from .embedding_service import EmbeddingService
from .vector_store import VectorStore
from typing import List, Dict, Any

class StructureEngine:
    def __init__(self, api_key: str = None, host: str = "localhost", port: int = 6333):
        self.llm_client = LLMClient(api_key=api_key)
        self.embedding_service = EmbeddingService(api_key=api_key)
        self.vector_store = VectorStore(host=host, port=port)
        self.prompt_manager = PromptManager()

    def process_thought(self, raw_text: str) -> StructuredOutput:
        """
        Takes raw text input, structures it, generates embeddings, and stores it.
        """
        # 1. Parse text using LLM
        system_prompt = self.prompt_manager.get_system_prompt()
        structured_output = self.llm_client.parse_input(
            text=raw_text,
            schema=StructuredOutput,
            system_prompt=system_prompt
        )

        # 2. Generate embeddings and store each item
        for item in structured_output.items:
            # Create a text representation for embedding (title + description)
            text_to_embed = f"{item.title}: {item.description}"
            vector = self.embedding_service.generate_embedding(text_to_embed)
            
            # 3. Store in Vector DB
            self.vector_store.upsert_item(item, vector)

        return structured_output

    def search_thoughts(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Semantic search for thoughts.
        """
        vector = self.embedding_service.generate_embedding(query)
        return self.vector_store.search_similar(vector, limit=limit)
