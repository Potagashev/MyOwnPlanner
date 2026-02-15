from llm_services.llm_abc import LLMServiceABC
from settings import Settings
from gigachat import GigaChat


class GigaChatService(LLMServiceABC):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.model_instance = GigaChat(
            credentials=settings.GIGACHAT_API_KEY,
            verify_ssl_certs=False,
        )

    async def send_prompt(self, prompt: str) -> str:
        response = await self.model_instance.achat(prompt)
        return response.choices[0].message.content
