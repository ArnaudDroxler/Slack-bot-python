import time

from slackclient import SlackClient
from config import TOKEN


def send(joueur, message) :
	reponse = bot.api_call("chat.postMessage", as_user=True, channel=joueur, text=message)
	print(reponse)


def sendToAll(listeJoueurs, message) :
	for joueur in listeJoueurs:
		send(joueur, message)



def jeu(nbToursParJoueur, nbMotsApparents, joueurs, input):
	joueurDontCEstLeTour=0
	histoire=[]

	nbTours = nbToursParJoueur*len(joueurs)
	
	for tour in range(1,nbTours+1):
		send(joueurs[joueurDontCEstLeTour], "tour " + str(tour) + "/" + str(nbTours) + " : ")
		"""chacun son tour, j1 puis j2 puis j3 puis à nouveau j1 etc..."""
		joueurDontCEstLeTour = (joueurDontCEstLeTour+1)%len(joueurs)
		
		"""selon l'avancement du jeu, on informe le joueur de ce qu'il doit faire"""
		if(tour==1):
			send(joueurs[joueurDontCEstLeTour], "Commencez l'histoire")
		elif(tour==nbTours):
			send(joueurs[joueurDontCEstLeTour], "Finissez l'histoire")
		else:
			send(joueurs[joueurDontCEstLeTour], "Continuez l'histoire")
		
		"""on affiche les quelques derniers mots de l'histoire"""
		for mot in histoire[-nbMotsApparents:]:
			send(joueurs[joueurDontCEstLeTour],mot + ' ')
		
		"""ajoute à l'histoire les nouveaux mots entrés par le joueur"""
		histoire += input.split()

	"""affiche l'histoire finie"""
	sendToAll(joueurs, "Histoire : " + str(histoire))
	
	

def process(user, message):
	global ETAT, NB_TOURS_PAR_JOUEUR, NB_MOTS_APPARENTS, LISTE_JOUEURS, NB_TOURS, JOUEUR_I, HISTOIRE, TOUR
		
	if(ETAT=="CONNECTE"):
		print(ETAT)	
		print(user + " dit " + message)
		LISTE_JOUEURS = [user]
		for joueur in message.split():
			LISTE_JOUEURS.append(joueur[2:-1])
		
		print(LISTE_JOUEURS)
		sendToAll(LISTE_JOUEURS, "Une partie de cadavre exquis est lancée, restez attentifs")
		ETAT="DEBUT_JEU"
		
	if(ETAT=="DEBUT_JEU"):
		print(ETAT)	
		NB_TOURS_PAR_JOUEUR = 3
		NB_MOTS_APPARENTS = 5
		NB_TOURS = NB_TOURS_PAR_JOUEUR*len(LISTE_JOUEURS)
		JOUEUR_I = 0
		HISTOIRE = []
		TOUR=1
		message = ""
		ETAT="JEU_EN_COURS"
		
	if(ETAT=="JEU_EN_COURS"):
		print(ETAT)	
		send(LISTE_JOUEURS[JOUEUR_I], "tour " + str(TOUR) + "/" + str(NB_TOURS) + " : ")
		if(TOUR==1):
			send(LISTE_JOUEURS[JOUEUR_I], "Commencez l'histoire")
		elif(TOUR==NB_TOURS):
			send(LISTE_JOUEURS[JOUEUR_I], "Finissez l'histoire")
			ETAT="FIN_JEU"
		else:
			send(LISTE_JOUEURS[JOUEUR_I], "Continuez l'histoire")
		
		if(message != ""):
			HISTOIRE += message.split()
			qlqsMots=""
			for mot in HISTOIRE[-NB_MOTS_APPARENTS:]:
				qlqsMots += mot + ' '
				
			send(LISTE_JOUEURS[JOUEUR_I], qlqsMots)

			
		TOUR = TOUR+1
		JOUEUR_I = (JOUEUR_I+1)%len(LISTE_JOUEURS)
		
	if(ETAT=="FIN_JEU"):
		print(ETAT)	
		sendToAll(LISTE_JOUEURS, "Histoire : " + str(HISTOIRE))
		
		
ETAT = "INIT"
LISTE_JOUEURS=[]
NB_TOURS_PAR_JOUEUR=0
NB_MOTS_APPARENTS=0
NB_TOURS=0
JOUEUR_I=0
HISTOIRE=[]
TOUR=0

bot = SlackClient(TOKEN)
if bot.rtm_connect():
	ETAT="CONNECTE"
	try:
		while True:
			messages = bot.rtm_read()
			if messages:
				for message in messages :
					#print(message)
					if "type" in message and message['type'] == 'message':
						if message['user'] != 'U1BU2CA1G': # id du bot
							print(message)
							process(message['user'], message['text'])
								
			else:
				time.sleep(1)
	except KeyboardInterrupt:
		pass
else:
	print("connexion échouée")
