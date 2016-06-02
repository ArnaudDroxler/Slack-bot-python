import time

from slackclient import SlackClient
from config import TOKEN, BOT_ID


g_etat = "INIT"
g_joueurs=[]
g_g_tours_par_joueur=0
g_nb_mots_apparents=0
g_nb_g_tours=0
g_indice_joueur=0
g_mots=[]
g_tour=0
g_bot = SlackClient(TOKEN)
g_slack_users_list=[]

			
def send(joueur, message) :
	reponse = g_bot.api_call("chat.postMessage", as_user=True, channel=joueur, text=message)
	print(reponse)


def sendToAll(listeJoueurs, message) :
	for joueur in listeJoueurs:
		send(joueur, message)

def validate(user, message):
	global g_joueurs
	
	print(">>>>>>>> validation du message : " + message)
	mots = message.split()
	print(">>>>>>>>>> mots : " + str(mots))
	if(mots[0]=="start"):
		g_joueurs = [user]
		for mot in mots[1:]:
			joueur = mot[2:-1]
			if(joueur in g_slack_users_list):
				g_joueurs.append(joueur)
			else:
				return {"ok":False, "error": mot+" n'est pas connu"}
		return {"ok":True}
	else:
		return {"ok":False, "error":"Pour commencez une partie, écrivez : start @joueur1 @joueur2 @joueur3 etc..."}
		
		
		
def process(user, message):
	global g_etat, g_g_tours_par_joueur, g_nb_mots_apparents, g_joueurs, g_nb_g_tours, g_indice_joueur, g_mots, g_tour
	
	print(">>>> PROCESSING")
	print(">>>> user : " + user + "  -- message : " + message + " -- etat : " + g_etat)

	if(g_etat=="CONNECTE"):
		print(">>>>>> etat : " + g_etat)
		
		validation = validate(user, message);
		print(">>>>>>>> validation : " + str(validation))
		if(validation["ok"]):
			sendToAll(g_joueurs, "Une partie de cadavre exquis est lancée, restez attentifs")
			g_etat="DEBUT_JEU"
		else:
			send(user, validation["error"])

	if(g_etat=="DEBUT_JEU"):
		print(">>>>>> etat : " + g_etat)
		g_g_tours_par_joueur = 2
		g_nb_mots_apparents = 5
		g_nb_g_tours = g_g_tours_par_joueur*len(g_joueurs)
		g_indice_joueur = 0
		g_mots = []
		g_tour=0
		message = ""
		g_etat="JEU_EN_COURS"

	if(g_etat=="JEU_EN_COURS"):
		print(">>>>>> etat : " + g_etat)

		g_tour = g_tour+1

		info_g_tour = "Tour " + str(g_tour) + "/" + str(g_nb_g_tours) + " : "
		if(g_tour==1):
			send(g_joueurs[g_indice_joueur], info_g_tour + "Commencez l'histoire :")
		elif(g_tour < g_nb_g_tours):
			send(g_joueurs[g_indice_joueur], info_g_tour + "Continuez l'histoire :")
		elif(g_tour==g_nb_g_tours):
			send(g_joueurs[g_indice_joueur], info_g_tour + "Finissez l'histoire :")

		if(message != ""):
			g_mots += message.split()

			if(g_tour<=g_nb_g_tours):
				qlqsMots=""
				for mot in g_mots[-g_nb_mots_apparents:]:
					qlqsMots += mot + ' '

				send(g_joueurs[g_indice_joueur], qlqsMots)
			else:
				g_etat="FIN_JEU"

		g_indice_joueur = (g_indice_joueur+1)%len(g_joueurs)

	if(g_etat=="FIN_JEU"):
		print(">>>>>> etat : " + g_etat)
		his=''
		for mot in g_mots:
			his += mot + ' '
		sendToAll(g_joueurs, "Histoire terminée : " + his)


def main():
	global g_etat, g_slack_users_list
	
	botInfos = g_bot.api_call("rtm.start", token=TOKEN)
	if botInfos['ok']:
		bot_id = botInfos['self']['id']
		print(bot_id)
		for member in botInfos['users']:
			g_slack_users_list.append(member['id'])
		
	if g_bot.rtm_connect():
		g_etat="CONNECTE"
		try:
			while True:
				messages = g_bot.rtm_read()
				if messages:
					for message in messages :
						print(message)
						if "type" in message and message['type'] == 'message':
							if message['user'] != bot_id:
								print(">> message reçu :" + str(message))
								process(message['user'], message['text'])

				else:
					time.sleep(0.01)
		except KeyboardInterrupt:
			pass
	else:
		print("connexion échouée")
		

main()
