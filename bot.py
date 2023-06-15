import logging
import datetime
import random
import os
from dotenv import load_dotenv

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
load_dotenv()
TOKEN = os.environ.get('TOKEN')

# Global variables bc i am lazy
data = {'food': "", 'time': ""}
FOOD = 1
TIME = 2
FINAL = 3


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


hottakes = [
    "S/Us shouldn't exist",
    "Piss is drinkable",
    "Finals is the best thing to happen to mankind",
    "Oranges should be cut not peeled",
    "Sex is better than running",
    "You just have to eliminate all your opponents to win",
    "Shit smells like shit",
    "viva la mushroom soup",
    "I am detrimental to humanity",
    "Everything is S/U-able or too easy",
    "One day this bot will pass the turing test",
    "Windows laptops are sus",
    "Apple desktops are sus",
    "If you wanna buy something, just do it",
    "If you can’t decide, flip a coin",
    "If you don’t like the coin’s result, choose the other result",
    "Don’t you love living in fear",
    "I will wake up at 7:29:52",
    "POK POK",
    "Why is there a limit on meal credits? I want to eat 120 hotdogs in one day",
    "An asshole is just a drink machine",
    "My new favourite is Roy. Wah the drift so good leh",
    "I’d rather have finals everyday",
    "Who is Jason?",
    "All men are pathetic and that’s why old women stay single",
    "Actually a degree is useless",
    "If you know you know\nIf you don’t know you don’t know",
    "Acai tastes nice with karaage",
    "If piss is drinkable then shit is edible",
    "Honestly coding is like eating",
    "Cock is the best, followed by cocaine",
    "I love balls",
    "Society is superficial",
    "Oooo boobs",
    "If the paper is easy, then ask your prof to set a harder paper!",
    "Wa mummy why got so much foam in my mouth",
    "If coding is graded, it is simply a leisurely activity",
    "I carry drugs",
    "Most people are dumb, if you look a the bellcurve, and cut it in half, 50% of the people are dumb already",
    "I’m immune to balls. *ball hits him*",
    "Sticks and stones looks like sticks and balls",
    "I like 12 inch sticks",
    "Jason: If there is one crack, there will be more cracks\nDariel: But my butt crack only one though",
    "If shuttle buses shuttle buses, what do shuttlecocks shuttle? COCK",
    "Stop touching my queen. I said touching... intentionally. Touch me more",
    "Yes",
    "I love jesus",
    "I need an intervention",
    "I hate the chinese",
    "JS stands for Jason Sucks",
    "If you drink soy sauce while you are pregnant, your child will turn out black.",
    "I've never eaten ass also.",
    "Gays are NULL",
    "I wanna be a sugar daddy",
    "I have a girlfriend, she is of type Optional",
    "I am an early birb",
    "onomatoPEAhPEAh",
    "jason janai. birb des."
]

length = len(hottakes) - 1

greetings = "Hello I am Jason Lee! \n" \
            + "I like to slay and give hot takes on controversial things. \n" \
            + "Do /hottake to hear one of my hot takes! \n" \
            + "Also, I love saba fish and tako balls."


def hottake(update, context):
    """Sends a hot take."""
    context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )
    a = random.randint(0, length)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=hottakes[a]
    )


def start(update, context):
    """Says hello"""
    context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=greetings
    )


def slay(update, context):
    """Slays"""
    context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="SLAYYYYYYYY"
    )


def hotcake(update, context):
    """Send a message when the command /hotcake is issued."""
    keyboard = [
        [
            InlineKeyboardButton("Macs", callback_data="1"),
            InlineKeyboardButton("Ameens", callback_data="2"),
            InlineKeyboardButton("Niqqi's", callback_data="3")
        ],
        [InlineKeyboardButton("Cancel", callback_data="0")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("What would you like to eat:", reply_markup=reply_markup)

    return FOOD


def orderFood(data):
    if data == 1:
        return "Macs"
    elif data == 2:
        return "Ameens"
    elif data == 3:
        return "Niqqi's"


def button(update, context):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    if int(query.data) == 0:
        query.edit_message_text(text="Order cancelled")
        return ConversationHandler.END

    data['food'] = orderFood(int(query.data))
    query.edit_message_text(text=f"{data['food']} ordered")

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="What time would you like to order?"
    )

    return TIME


def getTime(update, context):
    context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )
    timeFormat = "%H%M"
    try:
        validTime = datetime.datetime.strptime(update.message.text, timeFormat)
        data['time'] = update.message.text
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{data['food']} order close {data['time']}",
        )

        return ConversationHandler.END
    except ValueError:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Eh what kind of time is this, give me in HHMM leh",
        )
        return TIME


def cancel(update, context):
    update.message.reply_text('canceled')

    # end of conversation
    return ConversationHandler.END


def reply(update, context):
    user_id = update.message.from_user.username
    if user_id == "Dioclei":
        reply_text = ""
        msg = update.message.text
        msg = msg.lower()
        if "hello" in msg:
            reply_text = "Hello Jason"
        elif "slay" in msg:
            reply_text = "Slay indeed Jason"
        if reply_text != "":
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=reply_text
            )


def pokpok(update, context):
    context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="POK POK"
    )
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open('images/1.png', 'rb')
    )


def quack(update, context):
    context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Quack."
    )
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open('images/2.jpeg', 'rb')
    )


def birb(update, context):
    context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Birb."
    )
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open('images/3.jpg', 'rb')
    )


def chihuahua(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Vape? No. Chihuahua."
    )
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open('images/4.jpg', 'rb')
    )


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("hottake", hottake))
    dp.add_handler(CommandHandler("hello", start))
    dp.add_handler(CommandHandler("slay", slay))
    dp.add_handler(CommandHandler("pokpok", pokpok))
    dp.add_handler(CommandHandler("quack", quack))
    dp.add_handler(CommandHandler("cheepcheep", birb))
    dp.add_handler(CommandHandler("vape", chihuahua))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("hotcake", hotcake)],
        states={
            FOOD: [
                CallbackQueryHandler(button)
            ],
            TIME: [
                CommandHandler('cancel', cancel),
                MessageHandler(Filters.text, getTime)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    # dp.add_handler(MessageHandler(Filters.text, reply))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://jason-lee-bot.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
