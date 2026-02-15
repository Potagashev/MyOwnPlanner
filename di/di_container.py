from database import SessionLocal
from llm_services.gigachat import GigaChatService
from repositories.tasks import TaskRepository
from services.tasks import TaskService
from settings import settings

class DI:
    task_service: TaskService

    def init(self) -> None:
        self.settings = settings
        session_factory = SessionLocal

        task_repository = TaskRepository(session_factory=session_factory)
        gigachat_service = GigaChatService(settings=self.settings)
        self.task_service = TaskService(
            settings=self.settings,
            repo=task_repository,
            llm_service=gigachat_service,
        )