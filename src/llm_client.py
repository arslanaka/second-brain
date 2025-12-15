import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Type, TypeVar
from pydantic import BaseModel

# Load environment variables
load_dotenv()

T = TypeVar("T", bound=BaseModel)

class LLMClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        self.client = OpenAI(api_key=self.api_key)

    def parse_input(self, text: str, schema: Type[T], system_prompt: str, model: str = "gpt-4o") -> T:
        """
        Parses raw text into a structured Pydantic model using OpenAI's structured outputs.
        """
        try:
            completion = self.client.beta.chat.completions.parse(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text},
                ],
                response_format=schema,
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            # Handle potential API errors or parsing failures
            print(f"Error calling LLM: {e}")
            raise e
