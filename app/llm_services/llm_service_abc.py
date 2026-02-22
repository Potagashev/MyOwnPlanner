from app.llm_clients.llm_client_abc import LLMClientABC
from app.settings import Settings


class LLMServiceABC:
    def __init__(self, llm_client_abc: LLMClientABC, settings: Settings):
        self.llm_client = llm_client_abc
        self.settings = settings

    async def analyze_task(self, task_text: str) -> dict:
        pass