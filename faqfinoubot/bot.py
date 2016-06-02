import time

from slackclient import SlackClient
from config import TOKEN, BOT_ID


def send(joueur, message) :
	reponse = g_bot.api_call("chat.postMessage", as_user=True, channel=joueur, text=message)
	print(reponse)


def sendToAll(listeJoueurs, message) :
	for joueur in listeJoueurs:
		send(joueur, message)


def process(user, message):
	global g_etat, g_g_tours_par_joueur, g_nb_mots_apparents, g_joueurs, g_nb_g_tours, g_indice_joueur, g_mots, g_tour

	if(g_etat=="CONNECTE"):
		print(g_etat)
		print(user + " dit " + message)
		g_joueurs = [user]
		for joueur in message.split():
			g_joueurs.append(joueur[2:-1])

		print(g_joueurs)
		sendToAll(g_joueurs, "Une partie de cadavre exquis est lancée, restez attentifs")
		g_etat="DEBUT_JEU"

	if(g_etat=="DEBUT_JEU"):
		print(g_etat)
		g_g_tours_par_joueur = 2
		g_nb_mots_apparents = 5
		g_nb_g_tours = g_g_tours_par_joueur*len(g_joueurs)
		g_indice_joueur = 0
		g_mots = []
		g_tour=0
		message = ""
		g_etat="JEU_EN_COURS"

	if(g_etat=="JEU_EN_COURS"):
		print(g_etat)

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
		print(g_etat)
		his=''
		for mot in g_mots:
			his += mot + ' '
		sendToAll(g_joueurs, "Histoire terminée : " + his)

def main()
	g_etat = "INIT"
	g_joueurs=[]
	g_g_tours_par_joueur=0
	g_nb_mots_apparents=0
	g_nb_g_tours=0
	g_indice_joueur=0
	g_mots=[]
	g_tour=0

	g_bot = SlackClient(TOKEN)
	if g_bot.rtm_connect():
		g_etat="CONNECTE"
		try:
			while True:
				messages = g_bot.rtm_read()
				if messages:
					for message in messages :
						#print(message)
						if "type" in message and message['type'] == 'message':
							if message['user'] != BOT_ID: # id du bot
								print(message)
								process(message['user'], message['text'])

				else:
					time.sleep(1)
		except KeyboardInterrupt:
			pass
	else:
		print("connexion échouée")
