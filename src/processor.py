from .llm_client import LLMClient
from .prompt_manager import PromptManager
from .models import StructuredOutput

class StructureEngine:
    def __init__(self, api_key: str = None):
        self.llm_client = LLMClient(api_key=api_key)
        self.prompt_manager = PromptManager()

    def process_thought(self, raw_text: str) -> StructuredOutput:
        """
        Takes raw text input and returns a structured output object.
        """
        system_prompt = self.prompt_manager.get_system_prompt()
        return self.llm_client.parse_input(
            text=raw_text,
            schema=StructuredOutput,
            system_prompt=system_prompt
        )
