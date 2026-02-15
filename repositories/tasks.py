from sqlalchemy import insert, select
from models.tasks import Task
from repositories.repo_abc import RepositoryABC
from schemas.tasks import TaskItem


class TaskRepository(RepositoryABC):
    __table__ = Task

    async def create_task(self, data: dict) -> Task:
        async with self.unit_of_work() as uow:
            return await uow.execute(insert(self.__table__).values(**data).returning(self.__table__))

    async def get_inbox_tasks(self) -> list[TaskItem]:
        async with self.unit_of_work() as uow:
            tasks = await uow.scalars(
                select(self.__table__)
                .where(self.__table__.status == 'inbox')
                .order_by(self.__table__.created_at.desc())
            )
            return [TaskItem.model_dump(task) for task in tasks.all()]
            