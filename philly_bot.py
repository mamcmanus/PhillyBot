from __future__ import print_function
import boto3
import json
import sys
import time
import telepot
import feedparser
from datetime import datetime, timedelta
from textwrap import dedent


try:
    from Queue import Queue
except ImportError:
    from queue import Queue

"""
$ python2.7 telegram webhook AWS lambda
"""

#TODO: Add messages for empty news sets


bot = telepot.Bot('BOT KEY HERE')

##RSS feeds for each team that are being parsed for the latest news
sources = {'eagles': 'http://www.philly.com/philly_eagles.rss',
		'flyers': 'http://www.philly.com/philly_flyers.rss',
		'sixers': 'http://www.philly.com/philly_sixers.rss',
		'phillies': 'http://www.philly.com/sports_phillies.rss'
		}
###Function to parse the news based on whatever command the user sends to the bot
def get_news(source):
	feed = feedparser.parse(source)
	links = []
	for entry in feed.entries:
		pub_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
		if pub_date > (datetime.now() - timedelta(hours=24)):
			entry_tuple = (entry.title.encode('ascii', 'ignore'), 
				entry.link.encode('ascii', 'ignore'), 
				entry.description.encode('ascii', 'ignore'), 
				entry.published.encode('ascii', 'ignore'))
			links.append(entry_tuple)
	return links

###All the command and chat handlers
def start(chat_id):
	bot.sendMessage(chat_id, text='Hi! I am the Philly Phanatic, the best mascot in all of sports. You can ask me about the latest and greatest news about your favorite Philly sports teams. Type "/help" to see what is possible.')

def unknown(chat_id):
	bot.sendMessage(chat_id, text="Sorry, I didn't understand that command.")

def help(chat_id):
	bot.sendMessage(chat_id, 
		text=dedent('''
			They call me the Philly Phanatic, I can help you stay up to date on the latest news surrounding your favorite Philly sports team.

			You can control me by sending these commands:

			/eagles - The last 24 hours worth of Eagles news
			/flyers - The last 24 hours worth of Flyers news
			/sixers - The last 24 hours worth of Sixers news
			/phillies - The last 24 hours worth of Phillies news'''
		))

def settings(chat_id):
	bot.sendMessage(chat_id, text="Philly Phanatic cannot be configured via any settings yet. Check back soon!")

def news_command_handler(chat_id, team):
	bot.sendChatAction(chat_id, action='Typing')
	url_tuples = get_news(sources[team])
	for url in url_tuples:
		url_md = dedent('''
			[{}]({})
			{}'''.format(url[0], url[1], url[2]))
		bot.sendMessage(chat_id=chat_id, parse_mode='Markdown', disable_web_page_preview=True, text=url_md)


##Function to handle incoming messages and determine what the user is asking for
def handle(msg):
    flavor = telepot.flavor(msg)
    # normal message
    if flavor == 'normal':
        content_type, chat_type, chat_id = telepot.glance2(msg)
        print('Normal Message:', content_type, chat_type, chat_id)
        command = msg['text']
        if command == '/start':
        	start(chat_id)
        elif command == '/eagles':
        	news_command_handler(chat_id, 'eagles')
        elif command == '/flyers':
        	news_command_handler(chat_id, 'flyers')
        elif command == '/sixers':
        	news_command_handler(chat_id, 'sixers')
        elif command == '/phillies':
        	news_command_handler(chat_id, 'phillies')
        elif command == '/help':
        	help(chat_id)
        elif command == '/settings':
        	settings(chat_id)
        else:
        	unknown(chat_id)

        return('Message sent')

        # Do your stuff according to `content_type` ...

    # inline query - need `/setinline`
    elif flavor == 'inline_query':
        query_id, from_id, query_string = telepot.glance2(msg, flavor=flavor)
        print('Inline Query:', query_id, from_id, query_string)

        # Compose your own answers
        articles = [{'type': 'article',
                        'id': 'abc', 'title': 'ABC', 'message_text': 'Good morning'}]

        bot.answerInlineQuery(query_id, articles)

    # chosen inline result - need `/setinlinefeedback`
    elif flavor == 'chosen_inline_result':
        result_id, from_id, query_string = telepot.glance2(msg, flavor=flavor)
        print('Chosen Inline Result:', result_id, from_id, query_string)

        # Remember the chosen answer to do better next time

    else:
        raise telepot.BadFlavor(msg)


def my_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    handle(event['message'])
    return('Hopefully it sent...')

###FOR LOCAL DEV
# def my_handler(event):
#     print("Received event: " + json.dumps(event, indent=2))
#     handle(event)

# bot.notifyOnMessage(my_handler)

# print('Listening ...')

# # Keep the program running.
# while 1:
#     time.sleep(10)

