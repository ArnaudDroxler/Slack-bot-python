import time

from slackclient import SlackClient
from config import TOKEN, BOT_ID
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
	reponse = g_bot.api_call("chat.postMessage", as_user=True, channel=joueur, text=message)
	print(reponse)


def sendToAll(listeJoueurs, message) :
	for joueur in listeJoueurs:
		send(joueur, message)

def validate(user, message):
	global g_joueurs, g_tours_par_joueur, g_nb_mots_apparents
	
	print(">>>>>>>> validation du message : " + message)
	mots = message.split()
	print(">>>>>>>>>> mots : " + str(mots))
	if mots[0]=="start" and len(mots) > 3:
		g_joueurs = [user]
		for mot in mots[1:-2]:		# start <@U1DD1U6P4> <@U1DC8A7GW> 2 2 --> <@U1DD1U6P4> <@U1DC8A7GW>
			joueur = mot[2:-1] 		# <@U1DD1U6P4> --> U1DD1U6P4
			if joueur in g_slack_users_list:
				g_joueurs.append(joueur)
			else:
				return False
		
		try:
			g_tours_par_joueur = int(mots[-2])
		except ValueError:
			return False
		try:
			g_nb_mots_apparents = int(mots[-1])
		except ValueError:
			return False
			
		return True
	else:
		return False
		
		
		
def process(user, message):
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

				info_g_tour = "Tour " + str(g_tour) + "/" + str(g_nb_tours) + " : "
				if g_tour==1:
					send(g_joueurs[g_indice_joueur], info_g_tour + "Commencez l'histoire :")
				
				else:
					if g_tour < g_nb_tours:
						send(g_joueurs[g_indice_joueur], info_g_tour + "Continuez l'histoire :")
					elif g_tour==g_nb_tours:
						send(g_joueurs[g_indice_joueur], info_g_tour + "Finissez l'histoire :")

					g_mots += message.split()

					qlqsMots=""
					for mot in g_mots[-g_nb_mots_apparents:]:
						qlqsMots += mot + ' '

					send(g_joueurs[g_indice_joueur], qlqsMots)
					
					if g_tour>g_nb_tours:
						g_etat="FIN_JEU"
						
						
				g_joueur_courant = g_joueurs[g_indice_joueur]
				g_indice_joueur = (g_indice_joueur+1)%len(g_joueurs)
			
			else:
				send(user, "Ce n'est pas votre tour, "+getRandomCitation())
				#send(user, "Ce n'est pas votre tour, ")
		else:
			send(user, "Une partie est déjà en cours ¯\_(ツ)_/¯")

	if g_etat=="FIN_JEU":
		print(">>>>>> etat : " + g_etat)
		his=''
		for mot in g_mots:
			his += mot + ' '
		sendToAll(g_joueurs, "Histoire terminée : " + his)
		g_etat = "CONNECTE"


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
