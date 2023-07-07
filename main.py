import os
import telebot
import asyncio
import g4f
import logging
import threading
import re

# Specify logging level
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
BOT_WHITELIST: list[int] = []
if (not os.environ.get('BOT_WHITELIST')):
    logging.warning("No whitelist have been specified, this means that anybody can use this bot and you may get banned!")
else:
    try:
        for element in os.environ.get('BOT_WHITELIST').strip().split(","):
            BOT_WHITELIST.append(int(element.strip()))
    except:
        logging.critical("Invalid whitelist format! Syntax: 12345,09876,...")
        raise Exception("Invalid BOT_WHITELIST")

# Read bot admin to forward some details
BOT_ADMIN = os.environ.get('BOT_ADMIN')
if (not BOT_ADMIN):
    logging.warning("No admin ID has been specified")
else:
    if (BOT_ADMIN not in BOT_WHITELIST):
        logging.warning("Adding admin to whitelist")
        BOT_WHITELIST.append(int(BOT_ADMIN))

# Debug info
logging.debug("Whitelist: " + str(BOT_WHITELIST))
logging.debug("Admin: " + str(BOT_ADMIN))

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
        # Return an error to the admin
        denyText = "Ignoring message from user: [@" + inputMessage.from_user.username + "] id: [" + str(inputMessage.chat.id) + "]"
        if (BOT_ADMIN):
            bot.send_message(BOT_ADMIN, denyText)
        logging.warning(denyText)
        return False

# Handle non-text messages
@bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document', 'location', 'contact', 'sticker'])
def default_command(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        bot.reply_to(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nI'm very sorry but i have no idea on how to interact with this object")

# Handle BING command
@bot.message_handler(content_types=["text"], commands=['bing'])
def HandleBingMessage(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        # Check that the massage contains some text
        if (len(inputMessage.text) <= 5):
            bot.reply_to(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nplease give me some data to process, syntax is: `/[command] [text to interact with]`")
            return
        # Create async thread to handle replies
        thread = threading.Thread(target=ReplyAi, args=(inputMessage, g4f.Model.gpt_4, g4f.Provider.Bing, ))
        thread.start()
    else:
        bot.reply_to(inputMessage, "Sorry but you're not in the whitelist!")

# Handle Forefront command
@bot.message_handler(content_types=["text"], commands=['forefront'])
def HandleForefrontMessage(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        # Check that the massage contains some text
        if (len(inputMessage.text) <= 5):
            bot.reply_to(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nplease give me some data to process, syntax is: `/[command] [text to interact with]`")
            return
        # Create async thread to handle replies
        thread = threading.Thread(target=ReplyAi, args=(inputMessage, g4f.Model.gpt_4, g4f.Provider.Forefront))
        thread.start()
    else:
        bot.reply_to(inputMessage, "Sorry but you're not in the whitelist!")

# Handle AI command
@bot.message_handler(content_types=["text"], commands=['ai'])
def HandleAiMessage(inputMessage: telebot.types.Message):
    # if CheckWhitelist(inputMessage):
    #     # Check that the massage contains some text
    #     if (len(inputMessage.text) <= 5):
    #         bot.reply_to(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nplease give me some data to process, syntax is: `/[command] [text to interact with]`")
    #         return
    #     # Create async thread to handle replies
    #     thread = threading.Thread(target=ReplyAi, args=(inputMessage, "gpt-3.5-turbo", None, ))
    #     thread.start()
    # else:
    #     bot.reply_to(inputMessage, "Sorry but you're not in the whitelist!")
    HandleGetgptMessage(inputMessage)

# Handle Aichat command
@bot.message_handler(content_types=["text"], commands=['aichat'])
def HandleAichatMessage(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        # Check that the massage contains some text
        if (len(inputMessage.text) <= 5):
            bot.reply_to(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nplease give me some data to process, syntax is: `/[command] [text to interact with]`")
            return
        # Create async thread to handle replies
        thread = threading.Thread(target=ReplyAi, args=(inputMessage, "gpt-3.5-turbo", g4f.Provider.Aichat, ))
        thread.start()
    else:
        bot.reply_to(inputMessage, "Sorry but you're not in the whitelist!")

# Handle Ails command
@bot.message_handler(content_types=["text"], commands=['ails'])
def HandleAilsMessage(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        # Check that the massage contains some text
        if (len(inputMessage.text) <= 5):
            bot.reply_to(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nplease give me some data to process, syntax is: `/[command] [text to interact with]`")
            return
        # Create async thread to handle replies
        thread = threading.Thread(target=ReplyAi, args=(inputMessage, "gpt-3.5-turbo", g4f.Provider.Ails, ))
        thread.start()
    else:
        bot.reply_to(inputMessage, "Sorry but you're not in the whitelist!")

# Handle You command
@bot.message_handler(content_types=["text"], commands=['you'])
def HandleYouMessage(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        # Check that the massage contains some text
        if (len(inputMessage.text) <= 5):
            bot.reply_to(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nplease give me some data to process, syntax is: `/[command] [text to interact with]`")
            return
        # Create async thread to handle replies
        thread = threading.Thread(target=ReplyAi, args=(inputMessage, "gpt-3.5-turbo", g4f.Provider.You, ))
        thread.start()
    else:
        bot.reply_to(inputMessage, "Sorry but you're not in the whitelist!")

# Handle Yqcloud command
@bot.message_handler(content_types=["text"], commands=['yqcloud'])
def HandleYouMessage(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        # Check that the massage contains some text
        if (len(inputMessage.text) <= 5):
            bot.reply_to(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nplease give me some data to process, syntax is: `/[command] [text to interact with]`")
            return
        # Create async thread to handle replies
        thread = threading.Thread(target=ReplyAi, args=(inputMessage, "gpt-3.5-turbo", g4f.Provider.Yqcloud, ))
        thread.start()
    else:
        bot.reply_to(inputMessage, "Sorry but you're not in the whitelist!")

# Handle Bard command
@bot.message_handler(content_types=["text"], commands=['bard'])
def HandleBardMessage(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        # Check that the massage contains some text
        if (len(inputMessage.text) <= 5):
            bot.reply_to(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nplease give me some data to process, syntax is: `/[command] [text to interact with]`")
            return
        # Create async thread to handle replies
        thread = threading.Thread(target=ReplyAi, args=(inputMessage, "Palm2", g4f.Provider.Bard, ))
        thread.start()
    else:
        bot.reply_to(inputMessage, "Sorry but you're not in the whitelist!")

# Handle GetGPT command
@bot.message_handler(content_types=["text"], commands=['getgpt'])
def HandleGetgptMessage(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        # Check that the massage contains some text
        if (len(inputMessage.text) <= 5):
            bot.reply_to(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nplease give me some data to process, syntax is: `/[command] [text to interact with]`")
            return
        # Create async thread to handle replies
        thread = threading.Thread(target=ReplyAi, args=(inputMessage, "gpt-3.5-turbo", g4f.Provider.GetGpt, ))
        thread.start()
    else:
        bot.reply_to(inputMessage, "Sorry but you're not in the whitelist!")

# Handle H2O command
@bot.message_handler(content_types=["text"], commands=['h2o'])
def HandleH20Message(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        # Check that the massage contains some text
        if (len(inputMessage.text) <= 5):
            bot.reply_to(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nplease give me some data to process, syntax is: `/[command] [text to interact with]`")
            return
        # Create async thread to handle replies
        thread = threading.Thread(target=ReplyAi, args=(inputMessage, "falcon-40b", g4f.Provider.H2o, ))
        thread.start()
    else:
        bot.reply_to(inputMessage, "Sorry but you're not in the whitelist!")

# Handle Liaobots command
@bot.message_handler(content_types=["text"], commands=['liaobots'])
def HandleLiaobotsMessage(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        # Check that the massage contains some text
        if (len(inputMessage.text) <= 5):
            bot.reply_to(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nplease give me some data to process, syntax is: `/[command] [text to interact with]`")
            return
        # Create async thread to handle replies
        thread = threading.Thread(target=ReplyAi, args=(inputMessage, "gpt-4", g4f.Provider.Liaobots, ))
        thread.start()
    else:
        bot.reply_to(inputMessage, "Sorry but you're not in the whitelist!")

# Handle Lockchat command
@bot.message_handler(content_types=["text"], commands=['lockchat'])
def HandleLockchatMessage(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        # Check that the massage contains some text
        if (len(inputMessage.text) <= 5):
            bot.reply_to(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nplease give me some data to process, syntax is: `/[command] [text to interact with]`")
            return
        # Create async thread to handle replies
        thread = threading.Thread(target=ReplyAi, args=(inputMessage, "gpt-4", g4f.Provider.Lockchat, ))
        thread.start()
    else:
        bot.reply_to(inputMessage, "Sorry but you're not in the whitelist!")

# Handle Lockchat command
@bot.message_handler(content_types=["text"], commands=['vercel'])
def HandleVercelMessage(inputMessage: telebot.types.Message):
    if CheckWhitelist(inputMessage):
        # Check that the massage contains some text
        if (len(inputMessage.text) <= 5):
            bot.reply_to(inputMessage, "Hi " + inputMessage.from_user.first_name + ",\nplease give me some data to process, syntax is: `/[command] [text to interact with]`")
            return
        # Create async thread to handle replies
        thread = threading.Thread(target=ReplyAi, args=(inputMessage, "gpt-3.5-turbo", g4f.Provider.Vercel, ))
        thread.start()
    else:
        bot.reply_to(inputMessage, "Sorry but you're not in the whitelist!")


# Check for services status
@bot.message_handler(content_types=["text"], commands=['uptest'])
def HandleYouMessage(inputMessage: telebot.types.Message):
    if inputMessage.from_user.id == int(BOT_ADMIN):
        providersList: list = [g4f.Provider.Aichat, g4f.Provider.Vercel, g4f.Provider.Theb, g4f.Provider.Ails, g4f.Provider.Bard, g4f.Provider.Bing, g4f.Provider.ChatgptLogin, g4f.Provider.DeepAi, g4f.Provider.Forefront, g4f.Provider.GetGpt, g4f.Provider.H2o, g4f.Provider.Liaobots, g4f.Provider.Lockchat] 
        for singleProvider in providersList:
            thread = threading.Thread(target=ReplyAi, args=(inputMessage, "gpt-3.5-turbo", singleProvider, ))
            thread.start()
    else:
        bot.reply_to(inputMessage, "Sorry but you're allowed to use this command!")

# Create async reply
def ReplyAi(inputMessage: telebot.types.Message, botType, botProvider):
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
    inputQuery = re.sub(r"\/(\w+)", "", inputMessage.text).strip()
    if (not inputQuery):
        inputQuery = "Hello, who are you?"
    logging.debug(inputQuery)
    # Create the GPT4FREE instance
    try:
        gptResponse: str = g4f.ChatCompletion.create(model=botType, provider=botProvider, messages=[{"role": "user", "content": inputQuery}])
    except Exception as retExc:
        # Plot errors if needed
        try:
            response = "Model: " + str(botProvider).replace("<module ", "").split("from")[0] + "\n\n" + retExc
        except:
            response = retExc
        bot.edit_message_text(response, inputMessage.chat.id, newReply.id)
        return
    # Cleanup response from GPT if needed
    gptResponse = re.sub(r"(\[\^\d\^\])", "", gptResponse)
    if (not gptResponse):
        gptResponse = "An empty response was returned..."
    gptResponse = "Model: " + str(botProvider).replace("<module ", "").split("from")[0] + "\n\n" + gptResponse
    # Try to process the input text as markdown
    try:
        bot.edit_message_text(gptResponse, inputMessage.chat.id, newReply.id, parse_mode="Markdown")
    except:
        bot.edit_message_text(gptResponse, inputMessage.chat.id, newReply.id)

# Welcome new users
@bot.message_handler(content_types=["text"], commands=['start', 'hello'])
def send_welcome(inputMessage: telebot.types.Message):
    bot.reply_to(inputMessage, "Hello " + inputMessage.from_user.first_name + "\nHow can i assist you today?")

# Give project informations
@bot.message_handler(content_types=["text"], commands=['info'])
def send_welcome(inputMessage: telebot.types.Message):
    bot.reply_to(inputMessage, "Hello " + inputMessage.from_user.first_name + "\nThis project is hosted on a GitHub repository, do you want to partecipate? Here's the link: https://github.com/iu2frl/TelegramGPT")

# @bot.message_handler(func=lambda msg: True)
# def echo_all(message: telebot.types.Message):
#     bot.reply_to(message, message.text)

if __name__ == "__main__":
    logging.info("Starting bot")
    bot.infinity_polling()