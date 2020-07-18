import logging
import os
from dotenv import load_dotenv

from jobCentre import JobCentre

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, Dispatcher)

# load the .env variables
load_dotenv()

# Setting up the bot api key from .env file
token = os.getenv("BOT_API_KEY")

# Setting up the logging for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# define the available states the telegram bot can be
INITIAL, SEARCH_VACANCIES_REPLY = range(2)

def search_vacancies(update, context):
    # This is where we get the text the user keyed in
    searched_keyword = update.message.text

    # init new JobCentre class object
    jc = JobCentre()

    # scrape the website based on the keyword
    jobs = jc.scrape(searched_keyword)

    # format the jobs array to nicer looking string
    formatted_jobs_string = jobs_formatter(jobs)

    # display the result to the user
    update.message.reply_markdown(
        "Your selected keyword is {}".format(searched_keyword)
    )

    update.message.reply_markdown(formatted_jobs_string)

    return INITIAL

"""RUN THIS IF USER TEXTED /start"""
def start(update, context):
    response = "Please enter your keyword"
    
    # ask the user to enter the keyword
    update.message.reply_markdown(response)

    # return the state of the bot
    return SEARCH_VACANCIES_REPLY

"""FORMAT THE JOBS ARRAY TO NICE STRINGS TO DISPLAY TO THE USER"""
def jobs_formatter(jobs):
    formatted_jobs_string = ""

    """LOOP THE JOBS ARRAY"""
    for job in jobs:
        formatted_jobs_string += "\n*Company:* {}".format(job["company"])
        formatted_jobs_string += "\n*Title:* [{}]({})".format(job["title"], job["link"])
        formatted_jobs_string += "\n*Salary:* {}".format(job["salary"])
        formatted_jobs_string += "\n[Apply Now]({})".format(job["applyLink"])
        formatted_jobs_string += "\n\n"
    
    """RETURN THE FORMATTED STRING"""
    return formatted_jobs_string

"""JUST TO LOG THE ERROR, NOT IMPORTANT"""
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

"""WHAT TO DO IF USER ENTERED INVALID COMMAND, NOT IMPORTANT"""
def fallback(update, context):
    update.message.reply_markdown("Sorry, I couldn't understand your command", reply_markup=main_keyboard_markup)
    return INITIAL

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
            INITIAL: [
                # what to do when the user sends /start to the bot
                
                MessageHandler(Filters.regex('/start'), start),
                # run the start() function when user sends /start 
            ],
			
            # if your bot in this state, it could only understand the keyword sent by the user
            # sending /start to the bot if it is in this state will make it to query for /start keyword
            # in job centre
            SEARCH_VACANCIES_REPLY : [
                # what to do when user replied with a keyword

                MessageHandler(Filters.text, search_vacancies)
                # run the search_vacancies() function when user reply with a keyword
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