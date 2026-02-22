from app.llm_clients.llm_client_abc import LLMClientABC
from app.settings import Settings
from gigachat import GigaChat


class GigaChatClient(LLMClientABC):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.model_instance = GigaChat(
            credentials=settings.GIGACHAT_API_KEY,
            verify_ssl_certs=False,
        )

    async def send_prompt(self, prompt: str) -> str:
        response = await self.model_instance.achat(prompt)
        return response.choices[0].message.content
