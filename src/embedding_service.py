from openai import OpenAI
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class EmbeddingService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        self.client = OpenAI(api_key=self.api_key)

    def generate_embedding(self, text: str, model: str = "text-embedding-3-small") -> List[float]:
        """
        Generates a vector embedding for the given text.
        """
        try:
            response = self.client.embeddings.create(input=text, model=model)
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise e
