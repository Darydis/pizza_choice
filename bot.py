import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

import handlers


def main() -> None:
    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        raise RuntimeError('BOT_TOKEN not set')
    logging.basicConfig(level=logging.INFO)

    app = Application.builder().token(bot_token).build()
    app.add_handler(CommandHandler('start', handlers.start))
    # ОБРАБОТЧИК ДЛЯ КНОПКИ "Готово"
    app.add_handler(MessageHandler(filters.PHOTO, handlers.handle_photo))
    app.add_handler(
        CallbackQueryHandler(handlers.done_callback, pattern=r'^done$')
    )
    # затем кнопка «Присоединиться»
    app.add_handler(
        MessageHandler(filters.Regex(r'^Присоединиться$'), handlers.join_start_callback)
    )
    app.add_handler(MessageHandler(filters.Regex(r'^Узнать результат$'), handlers.result_callback))
    # ловим ввод номера опроса
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_join_input))
    app.add_handler(CallbackQueryHandler(handlers.button, pattern=r'^rate:'))
    app.add_handler(CommandHandler('result', handlers.result))
    app.run_polling()


if __name__ == '__main__':
    main()
