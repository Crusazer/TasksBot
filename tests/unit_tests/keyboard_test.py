from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from app.keyboards.keyboards import main_menu_keyboard, inline_task_keyboard


def test_main_menu_keyboard():
    expected_keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("Создать задачу"),
          KeyboardButton("Показать все задачи")]],
    )

    keyboard = main_menu_keyboard()

    assert keyboard == expected_keyboard


def test_inline_task_keyboard():
    """ Test inline keyboard assigned to tasks """
    task_id = 100
    expected_keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Изменить", callback_data=f"update_{task_id}"),
        InlineKeyboardButton("Завершить", callback_data=f"complete_{task_id}"),
        InlineKeyboardButton("Удалить", callback_data=f"delete_{task_id}")
    ]])

    keyboard = inline_task_keyboard(task_id)
    assert keyboard == expected_keyboard
