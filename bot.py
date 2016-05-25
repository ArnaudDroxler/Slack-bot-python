import time

from slackclient import SlackClient

TOKEN="xoxb-38243441969-g87a3Ok5QZ6vGab5HvuMrF3i"

bot = SlackClient(TOKEN)
if bot.rtm_connect():
    cpt = 0
    try:
        while True:
            messages = bot.rtm_read()
            if messages:
                print(str(cpt) + " ::: " + str(messages[0]['type']))
                cpt = cpt+1
                #bot.rtm_send_message([channel = messages[0]['channel'], message = messages[0]['text']])
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        pass
