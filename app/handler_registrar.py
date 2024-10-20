from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ConversationHandler
)

from fsm import change_task_handler, create_task_handler
from handlers.callback_handlers import update_task_handler, delete_task_handler, complete_task_handler
from handlers.command_handlers import start, cancel
from handlers.create_task_handlers import CreateTasksSteps, handle_create_task_deadline, handle_create_task_description
from handlers.message_handlers import all_tasks, create_task
from handlers.update_task_handlers import UpdateTasksSteps, handle_update_task_description, handle_update_task_deadline


def register_all_handlers(app):
    """ Register all handlers. Every handler should registered  here """

    # Register command handler
    app.add_handler(CommandHandler('start', start))

    # Register message handlers
    app.add_handler(MessageHandler(filters.Text("Показать все задачи") & ~filters.COMMAND, all_tasks))

    # Register callback handlers
    app.add_handler(CallbackQueryHandler(complete_task_handler, pattern="^complete_"))
    app.add_handler(CallbackQueryHandler(delete_task_handler, pattern="^delete_"))

    # Register FSM handlers
    app.add_handler(change_task_handler)
    app.add_handler(create_task_handler)
