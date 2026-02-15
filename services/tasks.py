from datetime import datetime
import json
from llm_services.llm_abc import LLMServiceABC
from repositories.tasks import TaskRepository
from schemas.tasks import TaskItem
from settings import Settings


class TaskService:
    def __init__(
        self,
        settings: Settings,
        repo: TaskRepository,
        llm_service: LLMServiceABC,
    ):
        self.settings = settings
        self.repo = repo
        self.llm_service = llm_service

    async def get_inbox_tasks(self) -> list[TaskItem]:
        tasks = await self.repo.get_inbox_tasks()
        return tasks

    async def add_task(self, task_text: str) -> dict:
        try:
            new_task = await self.repo.create_task(data={"text": task_text, "status": "inbox"})
            print(f"[DB] Добавлена задача: {task_text} (ID: {new_task.id})")

            analysis_result = await self._analyze_task(task_text)
            analysis_result['ai_analyzed'] = datetime.now()
            await self.repo.update_task(new_task.id, analysis_result)
            print(f"[AI] Задача проанализирована: {analysis_result}")

            return {
                "task_id": new_task.id,
                "analysis": analysis_result
            }
        except Exception as e:
            print(f"[ERROR] Ошибка при добавлении задачи: {e}")
            return {"task_id": -1, "analysis": None}
        
    
    async def _analyze_task(self, task_text: str) -> dict:
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
                print(f"[LLM WARNING] Не все поля в ответе: {result}")
                return {"category": "Другое", "priority": "Средний", "estimated_minutes": 30}

        except json.JSONDecodeError as e:
            print(f"[LLM ERROR] Ошибка парсинга JSON: {e}")
            print(f"[LLM ERROR] Ответ модели: {response_text}")
            return {"category": "Другое", "priority": "Средний", "estimated_minutes": 30}
        except Exception as e:
            print(f"[LLM ERROR] Ошибка при анализе задачи: {e}")
            return {"category": "Другое", "priority": "Средний", "estimated_minutes": 30}
