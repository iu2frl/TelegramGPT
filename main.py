import os
import telebot
import asyncio
import g4f
import logging
import threading
import re

# Specify logging leveò
logging.basicConfig(level=logging.DEBUG)

# Read API Token from environment variables
BOT_TOKEN: str = os.environ.get('BOT_TOKEN')
if (not BOT_TOKEN):
    logging.critical("Input token is empty!")
    raise Exception("Invalid BOT_TOKEN")
if (len(BOT_TOKEN) < 10):
    logging.critical("Input token is too short!")
    raise Exception("Invalid BOT_TOKEN")
if (":" not in BOT_TOKEN):
    logging.critical("Invalid input token format")
    raise Exception("Invalid BOT_TOKEN")
# Generate bot object
bot = telebot.TeleBot(BOT_TOKEN)

# Read allowed chat from environment variables
if (not os.environ.get('BOT_WHITELIST')):
    logging.warning("No whitelist have been specified, this means that anybody can use this bot and you may get banned!")
    BOT_WHITELIST: list[int] = []
else:
    BOT_WHITELIST: list[int] = os.environ.get('BOT_WHITELIST').strip().split(",")
    if (BOT_WHITELIST is not list[int]):
        logging.critical("Invalid whitelist format! Syntax: 12345,09876,...")
        raise Exception("Invalid BOT_WHITELIST")

# Check if message comes from a valid source
def CheckWhitelist(inputMessage: telebot.types.Message) -> bool:
    logging.debug("Checking message from [" + str(inputMessage.chat.id) + "]")
    if (len(BOT_WHITELIST) == 0):
        logging.debug("No whitelist, accepting by default")
        return True
    elif (inputMessage.chat.id in BOT_WHITELIST):
        logging.debug("Chat is in whitelist, accepting")
        return True
    else:
        logging.debug("Ignoring message from user: [" + inputMessage.from_user.username + "]")

# Handle non-text messages
@bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document', 'location', 'contact', 'sticker'])
def default_command(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        bot.send_message(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nI'm very sorry but i have no idea on how to interact with this object")

# Handle AI command
@bot.message_handler(content_types=["text"], commands=['ai', 'bing'])
def HandleAiMessage(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        # Check that the massage contains some text
        if (len(inputMessage.text) <= 5):
            bot.reply_to(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nplease give me some data to process, syntax is: `/ai [text to interact with]`")
            return
        # Create async thread to handle replies
        thread = threading.Thread(target=ReplyAi, args=(inputMessage, ))
        thread.start()

# Create async reply
def ReplyAi(inputMessage: telebot.types.Message):
    # Create the ASYNC.IO loop (if needed)
    try:
        newLoop = asyncio.get_event_loop()
    except RuntimeError as e:
        if str(e).startswith('There is no current event loop in thread'):
            newLoop = asyncio.new_event_loop()
            asyncio.set_event_loop(newLoop)
        else:
            raise
    # Generate temporary reply
    newReply = bot.reply_to(inputMessage, "Please wait...")
    # Process the input query
    inputQuery = inputMessage.text.capitalize().replace("/ai", "").strip()
    # Create the GPT4FREE instance
    try:
        gptResponse: str = g4f.ChatCompletion.create(model=g4f.Model.gpt_4, messages=[{"role": "user", "content": inputQuery}])
    except Exception as retExc:
        # Plot errors if needed
        bot.edit_message_text(retExc, inputMessage.chat.id, newReply.id)
        return
    # Cleanup response from GPT if needed
    gptResponse = re.sub(r"(\[\^\d\^\])", "", gptResponse)
    # Try to process the input text as markdown
    try:
        bot.edit_message_text(gptResponse, inputMessage.chat.id, newReply.id, parse_mode="Markdown")
    except:
        bot.edit_message_text(gptResponse, inputMessage.chat.id, newReply.id)

# Welcome new users
@bot.message_handler(content_types=["text"], commands=['start', 'hello'])
def send_welcome(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        bot.reply_to(inputMessage, "Hello " + inputMessage.from_user.first_name + "\nHow can i assist you today?")

# Give project informations
@bot.message_handler(content_types=["text"], commands=['info'])
def send_welcome(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        bot.reply_to(inputMessage, "Hello " + inputMessage.from_user.first_name + "\nThis project is hosted on a GitHub repository, do you want to partecipate? Here's the link: https://github.com/iu2frl/YotaBot")

# @bot.message_handler(func=lambda msg: True)
# def echo_all(message: telebot.types.Message):
#     bot.reply_to(message, message.text)

if __name__ == "__main__":
    logging.info("Starting bot")
    bot.infinity_polling()