import os
import telebot
import asyncio
import g4f
import logging
import threading
import re

# Read API Token from environment variables
BOT_TOKEN: str = os.environ.get('BOT_TOKEN')
if (len(BOT_TOKEN) < 10):
    raise Exception("Input token is too short!")
if (":" not in BOT_TOKEN):
    raise Exception("Invalid input token format")
bot = telebot.TeleBot(BOT_TOKEN)

# Read allowed chat from environment variables
BOT_WHITELIST: list[int] = os.environ.get('BOT_WHITELIST').strip().split(",")
if (len(BOT_WHITELIST) == 0):
    print("WARNING: No whitelist have been specified, this means that anybody can use this bot and you may get banned!")
if (BOT_WHITELIST is not list[int]):
    raise Exception("WARNING: Invalid whitelist format! Syntax: 12345,09876,...")
bot = telebot.TeleBot(BOT_WHITELIST)

# Check if message comes from a valid source
def CheckWhitelist(inputMessage: telebot.types.Message) -> bool:
    if (len(BOT_WHITELIST) == 0)

# Handle non-text messages
@bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document', 'location', 'contact', 'sticker'])
def default_command(inputMessage: telebot.types.Message):
    bot.send_message(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nI'm very sorry but i have no idea on how to interact with this object")

# Handle AI command
@bot.message_handler(commands=['ai'])
def HandleAiMessage(inputMessage: telebot.types.Message):
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

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda msg: True)
def echo_all(message: telebot.types.Message):
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    print("Starting bot")
    bot.infinity_polling()
