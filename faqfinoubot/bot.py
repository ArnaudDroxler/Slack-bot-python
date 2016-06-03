import time

from slackclient import SlackClient
from config import TOKEN
from patience import getRandomCitation

g_etat = "INIT"
g_joueurs=[]
g_tours_par_joueur=0
g_nb_mots_apparents=0
g_nb_tours=0
g_indice_joueur=0
g_mots=[]
g_tour=0
g_bot = SlackClient(TOKEN)
g_slack_users_list=[]
g_joueur_courant=""


def send(joueur, message) :
	"""Envoie le message message au joueur joueur"""
	reponse = g_bot.api_call("chat.postMessage", as_user=True, channel=joueur, text=message)
	print(reponse)


def sendToAll(listeJoueurs, message) :
	"""Envoie le message message à tous les joueurs contenus dans listeJoueurs"""
	for joueur in listeJoueurs:
		send(joueur, message)

def validate(user, message):
	"""Retourne un booléen qui confirme ou non la syntaxe à la création d'une partie"""
	global g_joueurs, g_tours_par_joueur, g_nb_mots_apparents

	print(">>>>>>>> validation du message : " + message)

	action, *params = message.split()

	print(">>>>>>>>>> params : " + str(params))
	if action=="start" and len(params) > 2:

		#réinitialise la liste de joueurs en forçant l'ajout du joueur qui lance la partie
		g_joueurs = [user]

		# itère sur les paramètres sauf les 2 derniers qui sont censé être 2 entiers
		for param in params[:-2]:
			joueur = param[2:-1] # <@U1DD1U6P4> --> U1DD1U6P4

			if joueur in g_slack_users_list:
				g_joueurs.append(joueur)
			else:
				return False

		try:
			g_tours_par_joueur = int(params[-2])
		except ValueError:
			return False
		try:
			g_nb_mots_apparents = int(params[-1])
		except ValueError:
			return False

		return True
	else:
		return False



def process(user, message):
	"""Machine d'état qui traite le message reçu en fonction de l'état d'avancement de la partie"""
	global g_etat, g_tours_par_joueur, g_nb_mots_apparents, g_joueurs, g_nb_tours, g_indice_joueur, g_mots, g_tour, g_joueur_courant

	print(">>>> PROCESSING")
	print(">>>> user : " + user + "  -- message : " + message + " -- etat : " + g_etat)

	if g_etat=="CONNECTE":
		print(">>>>>> etat : " + g_etat)

		tutoriel="Pour commencez une partie, écrivez :\nstart @joueur1 @joueur2 @joueur3 etc... _[nombre de tour par joueur]_ _[nombre de mots apparents]_\nPar Exemple :\nstart @bob @bill @mileyCirus 3 5"

		if validate(user, message):
			g_etat="DEBUT_JEU"
			sendToAll(g_joueurs, "Une partie de cadavre exquis est lancée, restez attentifs")
		else:
			return send(user, tutoriel)

		print(">>>>>>>> CONFIGURATION : joueurs :" + str(g_joueurs) + " -- nb mots apparents : " + str(g_nb_mots_apparents) + " -- nb tours par joueurs : " + str(g_tours_par_joueur))


	if g_etat=="DEBUT_JEU":
		print(">>>>>> etat : " + g_etat)
		g_nb_tours = g_tours_par_joueur*len(g_joueurs)
		g_indice_joueur = 0
		g_mots = []
		g_tour=0
		message = ""
		g_etat="JEU_EN_COURS"
		g_joueur_courant=user

	if g_etat=="JEU_EN_COURS":
		print(">>>>>> etat : " + g_etat)

		if user in g_joueurs:
			if g_joueur_courant==user:
				g_tour = g_tour+1
				
				msg_a_envoyer = "_Tour " + str(g_tour) + "/" + str(g_nb_tours) + " : "
				if g_tour==1:
					msg_a_envoyer += "Commencez l'histoire :_"
					send(g_joueurs[g_indice_joueur], msg_a_envoyer)
				else:
					if g_tour < g_nb_tours:
						msg_a_envoyer += "Continuez l'histoire :_\n"
					elif g_tour==g_nb_tours:
						msg_a_envoyer += "Finissez l'histoire :_\n"

					# si on est pas au tour un, c'est que le message contient le début ou la suite de l'histoire
					g_mots += message.split()

					# affiche les n dernier mots à l'utilisateur
					qlqsMots=""
					for mot in g_mots[-g_nb_mots_apparents:]:
						qlqsMots += mot + ' '

					msg_a_envoyer += qlqsMots

					if g_tour>g_nb_tours:
						g_etat="FIN_JEU"
					else:
						send(user, "_Bien reçu, patientez pendant que les autres joueurs complètent l'histoire_")
						send(g_joueurs[g_indice_joueur], msg_a_envoyer)

				g_joueur_courant = g_joueurs[g_indice_joueur]
				g_indice_joueur = (g_indice_joueur+1)%len(g_joueurs)

			else:
				send(user, "Ce n'est pas votre tour, "+getRandomCitation())
		else:
			send(user, "Une partie est déjà en cours ¯\_(ツ)_/¯\nAttendez la v2 pour pouvoir lancer plusieurs parties simultanées")

	if g_etat=="FIN_JEU":
		print(">>>>>> etat : " + g_etat)
		his=''
		for mot in g_mots:
			his += mot + ' '
		sendToAll(g_joueurs, "_Histoire terminée :_\n" + his)
		g_etat = "CONNECTE"


def main():
	"""Point d'entrée du programme, écoute constament les messages en provenence de slack et appelle la méthode process s'il s'agit d'un message texte d'un utilisateur"""
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
