import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from chekword import checkWord
from transliterate import to_cyrillic,to_latin
from uzwords import words


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)






def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    
    update.message.reply_markdown_v2(
        f"Assalomu alaykum {user.mention_markdown_v2()} \n\n  Imlo bo'timizga xush kelibsiz \! "
    )
    


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Bo'timizdan foydalanish uchun istalgan so'zni kiriting")


def echo(update: Update, context: CallbackContext) -> None:
    word = update.message.text
    message_splited = word.split()
    for i in message_splited:
        if i in words:
            result = checkWord(i)
            if result['available']:
                response = f'✅{i.capitalize()}'
            else:
                response = f'❌{i.capitalize()}\n'
                for text in result['matches']:
                    response += f'✅{text.capitalize()}\n'
            update.message.reply_text(response)
        else:
            result = checkWord(to_cyrillic(i))
            if result['available']:
                response = f'✅{to_latin(i.capitalize())}'
            else:
                response = f'❌{to_latin(i.capitalize())}\n'
                for text in result['matches']:
                    response += f'✅{to_latin(text.capitalize())}\n'
            update.message.reply_text(response)



def main() -> None:
    updater = Updater("BOT_TOKEN")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()