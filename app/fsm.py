from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, filters, CommandHandler

from handlers.callback_handlers import update_task_handler
from handlers.command_handlers import cancel
from handlers.create_task_handlers import CreateTaskSteps, get_description_handler, create_new_task_handler
from handlers.message_handlers import create_task
from handlers.update_task_handlers import UpdateTaskSteps, get_description, get_new_deadline

# FSM to update task
change_task_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(update_task_handler, pattern=r"update_\d+")],
    states={
        UpdateTaskSteps.DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_description)],
        UpdateTaskSteps.DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_new_deadline)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

# FSM to create new task
create_task_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Text("Создать задачу") & ~filters.COMMAND, create_task)],
    states={
        CreateTaskSteps.DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_description_handler)],
        CreateTaskSteps.DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_new_task_handler)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)