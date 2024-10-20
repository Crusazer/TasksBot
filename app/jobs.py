import logging
from datetime import datetime, timedelta

from telegram.ext import ContextTypes, Job

from config import settings
from core.schemas.task_dto import TaskDTO

logger = logging.getLogger(__name__)


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def remainder(context: ContextTypes.DEFAULT_TYPE):
    """ Send remainder message about deadline task to user """
    job: Job = context.job
    await context.bot.send_message(job.chat_id, text=f"Напоминание! Срок выполнения задачи через 1 день.\n{job.data} ")


def set_remainder(task: TaskDTO, chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    """ Add remainder of deadline task to queue """
    deadline = datetime.strptime(task.deadline, "%Y-%m-%d %H:%M:%S")
    remainder_time = deadline - timedelta(days=1) - datetime.now()
    delay = float(remainder_time.total_seconds())
    if delay > 0:
        context.job_queue.run_once(
            remainder,
            delay,
            chat_id=chat_id,
            name=f"{task.id}",
            data=(f"{task.description}\n"
                  f"Срок выполнения: {task.deadline}\n"
                  f"Изменена: {task.updated_at}\n"
                  f"Создана: {task.created_at}"
                  ),
        )
    logger.info("Remainder for task %s added", task.id)


def remove_remainder(context: ContextTypes.DEFAULT_TYPE, task_id: int) -> None:
    """ Delete remainder from queue """
    current_jobs = context.job_queue.get_jobs_by_name(str(task_id))
    if current_jobs:
        for job in current_jobs:
            job.schedule_removal()
            logger.info("Remainder for task %s removed.", task_id)
