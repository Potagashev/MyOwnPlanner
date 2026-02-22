from abc import ABC, abstractmethod

from app.settings import Settings


class LLMClientABC(ABC):
    def __init__(self, settings: Settings):
        self.settings = settings

    @abstractmethod
    async def send_prompt(self, prompt: str) -> str:
        pass