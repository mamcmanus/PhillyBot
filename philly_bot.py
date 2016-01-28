from __future__ import print_function
import boto3
import json
import sys
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


bot = telepot.Bot('BOT KEY')


eagles_url = 'http://www.philly.com/philly_eagles.rss'
flyers_url = 'http://www.philly.com/philly_flyers.rss'
sixers_url = 'http://www.philly.com/philly_sixers.rss'
phillies_url = 'http://www.philly.com/sports_phillies.rss'

def get_eagles_news():
	eagles_feed = feedparser.parse(eagles_url)
	eagles_links = []
	for entry in eagles_feed.entries:
		pub_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
		if pub_date > (datetime.now() - timedelta(hours=24)):
			entry_tuple = (entry.title, entry.link, entry.description, entry.published)
			eagles_links.append(entry_tuple)
	return eagles_links

def get_flyers_news():
	flyers_feed = feedparser.parse(flyers_url)
	flyers_links = []
	for entry in flyers_feed.entries:
		pub_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
		if pub_date > (datetime.now() - timedelta(hours=24)):		
			entry_tuple = (entry.title, entry.link, entry.description, entry.published)
			flyers_links.append(entry_tuple)
	return flyers_links

def get_sixers_news():
	sixers_feed = feedparser.parse(sixers_url)
	sixers_links = []
	for entry in sixers_feed.entries:
		pub_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
		if pub_date > (datetime.now() - timedelta(hours=24)):		
			entry_tuple = (entry.title, entry.link, entry.description, entry.published)
			sixers_links.append(entry_tuple)
	return sixers_links

def get_phillies_news():
	phillies_feed = feedparser.parse(phillies_url)
	phillies_links = []
	for entry in phillies_feed.entries:
		pub_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
		if pub_date > (datetime.now() - timedelta(hours=24)):		
			entry_tuple = (entry.title, entry.link, entry.description, entry.published)
			phillies_links.append(entry_tuple)
	return phillies_links

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

def eagles(chat_id):
	bot.sendChatAction(chat_id, action='Typing')
	url_tuples = get_eagles_news()
	for url in url_tuples:
		url_md = dedent('''
			[{}]({})
			{}'''.format(url[0], url[1], url[2]))
		bot.sendMessage(chat_id=chat_id, parse_mode='Markdown', disable_web_page_preview=True, text=url_md)

def flyers(chat_id):
	bot.sendChatAction(chat_id, action='Typing')
	url_tuples = get_flyers_news()
	for url in url_tuples:
		url_md = dedent('''
			[{}]({})
			{}'''.format(url[0], url[1], url[2]))
		bot.sendMessage(chat_id, parse_mode='Markdown', disable_web_page_preview=True, text=url_md)

def sixers(chat_id):
	bot.sendChatAction(chat_id, action='Typing')
	url_tuples = get_sixers_news()
	for url in url_tuples:
		url_md = dedent('''
			[{}]({})
			{}'''.format(url[0], url[1], url[2]))
		bot.sendMessage(chat_id, parse_mode='Markdown', disable_web_page_preview=True, text=url_md)

def phillies(chat_id):
	bot.sendChatAction(chat_id, action='Typing')
	url_tuples = get_phillies_news()
	for url in url_tuples:
		url_md = dedent('''
			[{}]({})
			{}'''.format(url[0], url[1], url[2]))
		bot.sendMessage(chat_id, parse_mode='Markdown', disable_web_page_preview=True, text=url_md)

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
        	eagles(chat_id)
        elif command == '/flyers':
        	flyers(chat_id)
        elif command == '/sixers':
        	sixers(chat_id)
        elif command == '/phillies':
        	phillies(chat_id)
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

