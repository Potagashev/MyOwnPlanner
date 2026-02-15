from sqlalchemy import insert, select, update
from models.tasks import Task
from repositories.repo_abc import RepositoryABC
from schemas.tasks import TaskItem


class TaskRepository(RepositoryABC):
    __table__ = Task

    async def create_task(self, data: dict) -> Task:
        async with self.unit_of_work() as uow:
            return await uow.scalar(insert(self.__table__).values(**data).returning(self.__table__))

    async def get_inbox_tasks(self) -> list[TaskItem]:
        async with self.unit_of_work() as uow:
            tasks = await uow.scalars(
                select(self.__table__)
                .where(self.__table__.status == 'inbox')
                .order_by(self.__table__.created_at.desc())
            )
            return [TaskItem.model_validate(task) for task in tasks.all()]
    
    async def update_task(self, task_id: int, data: dict) -> None:
        async with self.unit_of_work() as uow:
            await uow.execute(
                update(self.__table__)
                .where(self.__table__.id == task_id)
                .values(**data)
            )
            