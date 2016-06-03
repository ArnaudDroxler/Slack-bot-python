from bot import Faqfinoubot
from config import TOKEN
from random import choice

def randUser():
	global bot
	return "<@" + choice(bot.slack_users_list) + ">"

	
bot = Faqfinoubot(TOKEN)

messagesTestNegatif = [
"",
"coucou",
"start",
"start hello salut 3 2",
"start "+randUser()+" "+randUser(),
"start "+randUser()+" "+randUser()+" 3"
]

messagesTestPositif = [
"start "+randUser()+" "+randUser()+" 3 2"
]

for message in messagesTestNegatif:
	try:
		assert(not bot.validate(randUser(),message))
		print ("test négatif réussi : '" + message + "'")
	except AssertionError:
		print (">>>>>>>>>> test négatif échoué : '" + message + "'")
	
for message in messagesTestPositif:
	try:
		assert(bot.validate(randUser(),message))
		print ("test positif réussi : '" + message + "'")
	except AssertionError:
		print (">>>>>>>>>> test positif échoué : '" + message + "'")




