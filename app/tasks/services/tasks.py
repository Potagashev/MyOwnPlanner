from datetime import datetime
import json
import logging
from app.llm_clients.llm_client_abc import LLMClientABC
from app.llm_services.llm_service_abc import LLMServiceABC
from app.repositories.tasks import TaskRepository
from app.schemas.tasks import TaskItem
from app.settings import Settings

logger = logging.getLogger(__name__)


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
            logger.info(f"[DB] Добавлена задача: {task_text} (ID: {new_task.id})")

            analysis_result = await self.llm_service.analyze_task(task_text)
            analysis_result['ai_analyzed'] = datetime.now()
            await self.repo.update_task(new_task.id, analysis_result)
            logger.info(f"[AI] Задача проанализирована: {analysis_result}")

            return {
                "task_id": new_task.id,
                "analysis": analysis_result
            }
        except Exception as e:
            logger.error(f"[ERROR] Ошибка при добавлении задачи: {e}")
            return {"task_id": -1, "analysis": None}

    async def today_tasks(self) -> list[TaskItem]:
        tasks = await self.repo.get_tasks(
            status="inbox",
            scheduled_for=datetime.now().astimezone().date(),
            order_by="priority desc",
        )
