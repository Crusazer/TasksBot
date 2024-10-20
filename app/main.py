from telegram.ext import ApplicationBuilder

from config import settings
from utils import prepare_database
from handler_registrar import register_all_handlers


if __name__ == '__main__':
    prepare_database()
    app = ApplicationBuilder().token(settings.TOKEN).build()
    register_all_handlers(app)
    app.run_polling()
