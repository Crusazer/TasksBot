from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("Создать задачу"), KeyboardButton("Показать все задачи")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def inline_task_keyboard(task_id: int) -> InlineKeyboardMarkup:
    """
    Create inline keyboard for task message. Allowed to delete, change status or update task.
    """
    keyboard = [[
        InlineKeyboardButton("Изменить", callback_data=f"update_{task_id}"),
        InlineKeyboardButton("Завершить", callback_data=f"complete_{task_id}"),
        InlineKeyboardButton("Удалить", callback_data=f"delete_{task_id}"), ]
    ]

    return InlineKeyboardMarkup(keyboard)
