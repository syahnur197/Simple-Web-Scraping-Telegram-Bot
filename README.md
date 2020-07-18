# Telegram Bot + Web Scraping Job Centre Website

This repository contains the source code for `Build a Simple Telegram Bot Using Scrapped Data from a Website` which was conducted on **Sunday, 26th of July 2020** for **web.dev** event.

## Requirements

- [Python 3.8](https://www.python.org/downloads/release/python-380/)

- [pip](https://lmgtfy.com/?q=how+to+install+pip)

- [pipenv](https://pypi.org/project/pipenv/) ([What is it?](https://opensource.com/article/18/2/why-python-devs-should-use-pipenv))

- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) ([doc](https://www.crummy.com/software/BeautifulSoup/bs4/doc/))

- [requests](https://pypi.org/project/requests/) ([doc](https://requests.readthedocs.io/en/master/))

- [Python Telegram Bot](https://pypi.org/project/python-telegram-bot/) ([GitHub](https://github.com/python-telegram-bot/python-telegram-bot), [doc](https://python-telegram-bot.readthedocs.io/en/stable/))

- [Telegram Bot Token](https://core.telegram.org/bots#6-botfather)



## Steps to run this code

1. Git clone this into your local machine

2. cd to the folder

3. run `pipenv install` to install dependencies in `Pipfile.lock`

4. run `pipenv shell` to start the virtual environment

5. Get the [Telegram Bot Token](https://core.telegram.org/bots#6-botfather) by consulting [BotFather](https://t.me/botfather)

6. Copy `.env.example` file content and paste into into a new file `.env`

7. Copy your `Telegram Bot Token` and assign it to `BOT_API_KEY` variable in `.env`

8. Look for your bot in `Telegram` and start a chat with it, it should be available in Telegram if you followed step 5 correctly

9. In the project root folder, run `python bot.py` to start the bot

10. Send `/start` to your bot!



## Common Problems

1. `python`, `pip`, and `pipenv` commands should be available in your terminal

2. Add the above command in your System Environment Path (Windows) if it is not available

3. Make sure you have the correct Python Version (3.8)



## Understanding Web Scraping

1. Identify the link of the website you want to scrape, in this project case, the link is `https://www.jobcentrebrunei.gov.bn/web/guest/search-job?q={keyword}`

2. Identify the html elements in the website you want to obtain, take note of the html tags, classes, and ids

3. Take a look at `jobCentre.py`, you'll learn how to extract relevant data in the website

```python
company = div.find_all("div", class_="jp_job_post_right_cont")[0].find_all("p")[0].find_all("a")[0].text
```

4. For example, the above code I want to extract the text in the first `<a>` tag, in the first `<p>` tag, in the first `<div>` tag with a class of `jp_job_post_right_cont`



## Understand Telegram Bot - The Theory

The theory of the Telegram Bot API is quite simple.

1. When a user sent a text to your bot, the text will be stored in Telegram server
2. Your bot server will continuously sends request to Telegram server to ask for an update
3. If there is a new user text sent to your bot, Telegram will send to your bot this text(s)
4. The new text is then will be put into an [Updater](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.updater.html) object
5. The `Updater` object will then create a [Dispatcher](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.dispatcher.html#telegram.ext.Dispatcher) object
6. The `Dispatcher` object will then dispatch the updated text into [Handler](https://python-telegram-bot.readthedocs.io/en/stable/telegram.html#handlers) objects to tell your bot how what function to perform based on the user's text
7. Based on the user's action, you can instruct the bot to assume in a particular state
8. When a bot in a state, it could only perform the necessary `Handlers` defined in the state
9. After the bot performed the necessary functions, you can tell the bot again the assume in a state 



tl;dr - Your bot fetch new text from Telegram server, the bot will then do the necessary functions to handle the text. Once it's done, it will then assume in a state



### Job Centre Web Scraping Bot 



I want to bring your attention to the `main()` function in the `bot.py` file.

```python
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
```



Now, if you take a look at ` MessageHandler(Filters.regex('/start'), start)`, you can see that I have instructed the bot to run `start(update, context)` function when it is in `INITIAL` state and a user sent `/start` message to the bot. Any function that is passed to a [handler is called callback function](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.handler.html#telegram.ext.Handler). For every callback function, they need to have the `update`, and `context` arguments in the function parameter. What we are interested at is the `update` argument. In the `update` argument, we can access any data that is passed by the user when responding the bot when the bot assume in a particular state. You can refer [here](https://python-telegram-bot.readthedocs.io/en/stable/telegram.update.html) to see what other things that you can access in the `update` argument.  The `update` argument can also be used to send something to the user.

To send a message to the user, you can call `update.message.reply_markdown(string)`.



```python
def start(update, context):
    response = "Please enter your keyword"
    
    # ask the user to enter the keyword
    update.message.reply_markdown(response)

    # return the state of the bot
    return SEARCH_VACANCIES_REPLY
```



Let's take a look at `search_vacancies(update, context)`



```python
def search_vacancies(update, context):
    # This is where we get the text the user keyed in
    searched_keyword = update.message.text
	
    # perform web scraping here
    
    
	# reply to the user
    update.message.reply_markdown(formatted_jobs_string)

    return INITIAL
```

You can see that I retrieved the text the user entered using `update.message.text` and put the text into `searched_keyword` variable



## Other Things You Can Do

- Send an options that the user can select by using [ReplyKeyboardMarkup](https://python-telegram-bot.readthedocs.io/en/stable/telegram.replykeyboardmarkup.html)

  ```python
  # Define your keyboard layout
  options_keyboard = [
      ['Option 1'],
      ['Option 2'],
      ['Option 3']
  ]
  
  # Define a ReplyKeyboardMarkup object
  options_keyboard_markup = ReplyKeyboardMarkup(options_keyboard, one_time_keyboard=True)
  
  # return the keyboard in your action
  def some_function(update, context):
      theText = update.message.text
      
      # perform something
      
      update.message.reply_markdown("Please select some options", reply_markup=options_keyboard_markup)
      
      return SELECT_OPTION_STATE
  
  def option_one_selected(update, context):
      # do something
      return INITIAL
  
  def option_two_selected(update, context):
      # do something
      return INITIAL
  
  def option_three_selected(update, context):
      # do something
      return INITIAL
  
  # add new state in your main() function
  def main():
      ......
      conv_handler = ConversationHandler(
      	......
          states = {
              .......
              SELECT_OPTION_STATE: [
                  MessageHandler(Filters.regex('^Option 1$'), option_one_selected),
                  MessageHandler(Filters.regex('^Option 2$'), option_two_selected),
                  MessageHandler(Filters.regex('^Option 3$'), option_three_selected),
              ],
              .......
          }
          ......
      )
  ```

## Some Nice Examples
This bot is actually quite simple and I haven't explored a lot of the functionalities outlined in the official documentation. I recommend everyone to have a look at the repository and try to learn from some of the examples in the repo. Personally, I refer to this [example](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot2.py) when developing this bot. You can have a look [here](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/README.md) to view other examples.

Have Fun!