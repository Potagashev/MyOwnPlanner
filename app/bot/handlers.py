from aiogram import Router, types
from aiogram.filters import Command

from app.bot.enums import CommandEnum
from app.di.di_container import di

router = Router()

@router.message(Command(CommandEnum.START))
async def cmd_start(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(
        f"Привет, {user_name}! 👋\n"
        f"Я твой ИИ-планировщик. Вот что я умею:\n"
        f"/add [задача] - добавить задачу в инбокс\n"
        f"/inbox - посмотреть задачи в инбоксе\n"
        f"/plan_today - запланировать задачи на сегодня"
    )


@router.message(Command(CommandEnum.ADD))
async def cmd_add(message: types.Message):
    service = di.task_service
    task_text = message.text[5:].strip()

    if not task_text:
        await message.answer("❌ Напишите задачу после команды /add\nНапример: /add купить молоко")
        return

    processing_msg = await message.answer("🔄 Анализирую задачу...")
    result = await service.add_task(task_text)

    if result["task_id"] != -1:
        analysis = result["analysis"]
        response_text = (
            f"✅ Задача добавлена (ID: {result['task_id']})\n"
            f"📝 {task_text}\n\n"
            f"🤖 **Анализ ИИ:**\n"
            f"• 🏷️ Категория: {analysis['category']}\n"
            f"• 🚦 Приоритет: {analysis['priority']}\n"
            f"• ⏱️ Время: ~{analysis['estimated_minutes']} мин"
        )
        await processing_msg.edit_text(response_text)
    else:
        await processing_msg.edit_text("❌ Ошибка при сохранении задачи")


@router.message(Command(CommandEnum.INBOX))
async def cmd_inbox(message: types.Message):
    service = di.task_service
    tasks = await service.get_inbox_tasks()

    if not tasks:
        await message.answer("📭 Инбокс пуст! Добавьте задачи командой /add")
        return

    tasks_list = "📥 **Задачи в инбоксе:**\n\n"
    for i, task in enumerate(tasks):
        priority_emoji = {"Высокий": "🔴", "Средний": "🟡", "Низкий": "🟢"}.get(task.priority, "⚪")
        category_emoji = {"Работа": "💼", "Личное": "👤", "Здоровье": "💪", "Обучение": "📚", "Семья": "👨‍👩‍👧‍👦"}.get(
            task.category, "📌",
        )
        tasks_list += (
            f"{i}. {task.text}\n"
            f"   {category_emoji} {task.category} | {priority_emoji} {task.priority} | ⏱️ {task.estimated_minutes} мин\n"
            f"   🆔 {task.id} | 🕒 {task.created_at.strftime('%H:%M')}\n\n"
        )

    await message.answer(tasks_list)


@router.message(Command(CommandEnum.PLAN_TODAY))
async def cmd_plan_today(message: types.Message):
    service = di.task_service
    tasks = await service.today_tasks()

    if not tasks:
        await message.answer("📅 План на сегодня пуст!")
        return

    plan_text = "📅 **План на сегодня:**\n\n"
    for task in tasks:
        priority_emoji = {"Высокий": "🔴", "Средний": "🟡", "Низкий": "🟢"}.get(task.priority, "⚪")
        category_emoji = {"Работа": "💼", "Личное": "👤", "Здоровье": "💪", "Обучение": "📚", "Семья": "👨‍👩‍👧‍👦"}.get(
            task.category, "📌",
        )
        plan_text += (
            f"• {task.text}\n"
            f"   {category_emoji} {task.category} | {priority_emoji} {task.priority} | ⏱️ {task.estimated_minutes} мин\n"
            f"   🆔 {task.id}\n\n"
        )

    await message.answer(plan_text)


@router.message()
async def echo_handler(message: types.Message):
    await message.answer(f"🤖 Вы сказали: \"{message.text}\"\n\nИспользуйте команды /start, /add, /inbox")
