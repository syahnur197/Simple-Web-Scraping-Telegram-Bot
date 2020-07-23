import logging
import os
from dotenv import load_dotenv

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, Dispatcher)

# load the .env variables
load_dotenv()

# Setting up the bot api key from .env file
token = os.getenv("BOT_API_KEY")

# Setting up the logging for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# define the available states the telegram bot can be
MY_STATE = range(1)

def greeting(update, context):
    # This is where we get the text the user keyed in
    name = update.message.text

    # display the result to the user
    update.message.reply_markdown(
        "Your name is {}".format(name)
    )

    return MY_STATE

"""RUN THIS IF USER TEXTED /start"""
def start(update, context):
    response = "What is your name?"
    
    # ask the user to enter the keyword
    update.message.reply_markdown(response)

    # return the state of the bot
    return MY_STATE


"""JUST TO LOG THE ERROR, NOT IMPORTANT"""
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

"""WHAT TO DO IF USER ENTERED INVALID COMMAND, NOT IMPORTANT"""
def fallback(update, context):
    update.message.reply_markdown("Sorry, I couldn't understand your command")
    return MY_STATE

def main():
    # put the updates in an Updater object
    updater = Updater(token, use_context=True)
    
    # dispatch the updates
    dp = updater.dispatcher

    # defining the handler
    conv_handler = ConversationHandler(
        # what to do when user start the program
        entry_points=[
            CommandHandler('start', start),
        ],
		
        # definining the states your bot can assume
        states={
            # the INITIAL state, if your bot in this state, it could only understand the /start command
            MY_STATE: [
                # what to do when the user sends /start to the bot
                
                MessageHandler(Filters.regex('/start'), start),
                # run the start() function when user sends /start 

                MessageHandler(Filters.text, greeting)
            ],
        },
		
        # What to do if the bot don't understand anything
        fallbacks=[MessageHandler(Filters.text, fallback)]
    )
	
    # add a handler to the Dispatcher object
    dp.add_handler(conv_handler)
	
    # poll telegram server and continuously request for updates
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()