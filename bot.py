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
						if message['user'] != 'U1BMBKURE' and message['user'] != 'U146XKR8Q': # id du bot
							#bot.rtm_send_message('random', message['text'])
							echo = message['user'] + " dit " + message['text']
							print(echo)
							reponse = bot.api_call("chat.postMessage", as_user="true:", channel="U146XKR8Q", text=echo)
							print(reponse)
			else:
				time.sleep(1)
	except KeyboardInterrupt:
		pass
else:
	print("connexion échouée")
