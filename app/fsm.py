from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, filters, CommandHandler

from handlers.callback_handlers import update_task_handler
from handlers.command_handlers import cancel
from handlers.create_task_handlers import CreateTasksSteps, handle_create_task_description, handle_create_task_deadline
from handlers.message_handlers import create_task
from handlers.update_task_handlers import UpdateTasksSteps, handle_update_task_description, handle_update_task_deadline

# FSM to update task
change_task_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(update_task_handler, pattern=r"update_\d+")],
    states={
        UpdateTasksSteps.DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_update_task_description)],
        UpdateTasksSteps.DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_update_task_deadline)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

# FSM to create new task
create_task_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Text("Создать задачу") & ~filters.COMMAND, create_task)],
    states={
        CreateTasksSteps.DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_create_task_description)],
        CreateTasksSteps.DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_create_task_deadline)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
