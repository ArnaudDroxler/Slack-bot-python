import time

from slackclient import SlackClient
from config import TOKEN


bot = SlackClient(TOKEN)

if bot.rtm_connect():
	try:
		while True:
			messages = bot.rtm_read()
			if messages:
				for message in messages :
					#print(message)
					if "type" in message and message['type'] == 'message':
						if message['user'] != 'U1BMBKURE': # id du bot
							print(message['user'] + " dit " + message['text'])
							bot.rtm_send_message('random', message['text'])
			else:
				time.sleep(1)
	except KeyboardInterrupt:
		pass
else:
	print("connexion échouée")
