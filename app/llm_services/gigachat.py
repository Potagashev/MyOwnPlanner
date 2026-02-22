import json
import logging

from app.llm_services.llm_service_abc import LLMServiceABC

logger = logging.getLogger(__name__)


class GigaChatService(LLMServiceABC):

    async def analyze_task(self, task_text: str) -> dict:
        prompt = f"""
        Ты - помощник для планирования задач. Проанализируй задачу и верни ответ в формате JSON.

        Задача: "{task_text}"

        Проанализируй и определи:
        1. Категорию (только одно слово): Работа, Личное, Здоровье, Обучение, Семья, Другое
        2. Приоритет (только одно слово): Высокий, Средний, Низкий
        3. Ориентировочное время выполнения в минутах (только число)

        Критерии приоритета:
        - Высокий: срочные дела, дедлайны, важные встречи
        - Средний: обычные задачи, плановые дела  
        - Низкий: несрочные дела, хобби, отдых

        Пример ответа:
        {{"category": "Работа", "priority": "Высокий", "estimated_minutes": 120}}

        Верни ТОЛЬКО JSON, без лишнего текста:
        """

        try:
            response = await self.llm_service.send_prompt(prompt)
            response_text = response.strip()

            response_text = response_text.replace('```json', '').replace('```', '').strip()

            result = json.loads(response_text)

            required_fields = ["category", "priority", "estimated_minutes"]
            if all(field in result for field in required_fields):
                return result
            else:
                logger.warning(f"[LLM WARNING] Не все поля в ответе: {result}")
                return {"category": "Другое", "priority": "Средний", "estimated_minutes": 30}

        except json.JSONDecodeError as e:
            logger.error(f"[LLM ERROR] Ошибка парсинга JSON: {e}")
            logger.error(f"[LLM ERROR] Ответ модели: {response_text}")
            return {"category": "Другое", "priority": "Средний", "estimated_minutes": 30}
        except Exception as e:
            logger.error(f"[LLM ERROR] Ошибка при анализе задачи: {e}")
            return {"category": "Другое", "priority": "Средний", "estimated_minutes": 30}