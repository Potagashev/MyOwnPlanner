from app.database.database import SessionLocal
from app.llm_clients.gigachat import GigaChatClient
from app.llm_services.gigachat import GigaChatService
from app.repositories.tasks import TaskRepository
from app.tasks.services.tasks import TaskService
from app.settings import Settings, settings
from app.utils.utils import Singleton

class DI(metaclass=Singleton):
    settings: Settings
    task_service: TaskService

    def __init__(self) -> None:
        self.settings = settings
        session_factory = SessionLocal

        task_repository = TaskRepository(session_factory=session_factory)
        llm_client = GigaChatClient(settings=self.settings)
        llm_service = GigaChatService(llm_client_abc=llm_client, settings=self.settings)
        self.task_service = TaskService(
            settings=self.settings,
            repo=task_repository,
            llm_service=llm_service,
        )

di = DI()