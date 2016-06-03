from time import sleep
from slackclient import SlackClient
from config import TOKEN
from patience import getRandomCitation

class Faqfinoubot:
	def __init__(self, token):
		self.etat = "INIT"
		self.joueurs=[]
		self.tours_par_joueur=0
		self.nb_mots_apparents=0
		self.nb_tours=0
		self.indice_joueur=0
		self.mots=[]
		self.tour=0
		self.bot = SlackClient(TOKEN)
		self.slack_users_list=[]
		self.joueur_courant=""
		self.tutoriel="Pour commencez une partie, écrivez :\nstart @joueur1 @joueur2 @joueur3 etc... [nombre de tour par joueur] [nombre de mots apparents]\nPar Exemple :\nstart @bob @bill @mileyCirus 3 5"
		
		botInfos = self.bot.api_call("rtm.start", token=TOKEN)
		if botInfos['ok']:
			self.bot_id = botInfos['self']['id']
			for member in botInfos['users']:
				self.slack_users_list.append(member['id'])

		
	def send(self, joueur, message) :
		"""Envoie le message message au joueur joueur"""
		reponse = self.bot.api_call("chat.postMessage", as_user=True, channel=joueur, text=message)


	def sendToAll(self, listeJoueurs, message) :
		"""Envoie le message message à tous les joueurs contenus dans listeJoueurs"""
		for joueur in listeJoueurs:
			self.send(joueur, message)

	def validate(self, user, message):
		"""Retourne un booléen qui confirme ou non la syntaxe à la création d'une partie"""
		
		if not len(message): return False
		
		action, *params = message.split()

		if action=="start" and len(params) > 2:

			#réinitialise la liste de joueurs en forçant l'ajout du joueur qui lance la partie
			self.joueurs = [user]

			# itère sur les paramètres sauf les 2 derniers qui sont censé être 2 entiers
			for param in params[:-2]:
				joueur = param[2:-1] # <@U1DD1U6P4> --> U1DD1U6P4

				if joueur in self.slack_users_list:
					self.joueurs.append(joueur)
				else:
					return False

			try:
				self.tours_par_joueur = int(params[-2])
			except ValueError:
				return False
			try:
				self.nb_mots_apparents = int(params[-1])
			except ValueError:
				return False

			return True
		else:
			return False		
		
		
	def process(self, user, message):
		"""Machine d'état qui traite le message reçu en fonction de l'état d'avancement de la partie"""

		if self.etat=="CONNECTE":
			if self.validate(user, message):
				self.etat="DEBUT_JEU"
				self.sendToAll(self.joueurs, "Une partie de cadavre exquis est lancée, restez attentifs")
			else:
				self.send(user, self.tutoriel)

		if self.etat=="DEBUT_JEU":
			self.nb_tours = self.tours_par_joueur*len(self.joueurs)
			self.indice_joueur = 0
			self.mots = []
			self.tour=0
			self.etat="JEU_EN_COURS"
			print("jeu en cours")
			self.joueur_courant=user
			message = ""

		if self.etat=="JEU_EN_COURS":
			if user in self.joueurs:
				if self.joueur_courant==user:
					self.tour += 1
					
					msg_a_envoyer = "_Tour " + str(self.tour) + "/" + str(self.nb_tours) + " : "
					if self.tour==1:
						msg_a_envoyer += "Commencez l'histoire :_"
						self.send(self.joueurs[self.indice_joueur], msg_a_envoyer)
					else:
						if self.tour < self.nb_tours:
							msg_a_envoyer += "Continuez l'histoire :_\n"
						elif self.tour==self.nb_tours:
							msg_a_envoyer += "Finissez l'histoire :_\n"

						# si on est pas au tour un, c'est que le message contient le début ou la suite de l'histoire
						self.mots += message.split()

						# affiche les n dernier mots à l'utilisateur
						qlqsMots=""
						for mot in self.mots[-self.nb_mots_apparents:]:
							qlqsMots += mot + ' '

						msg_a_envoyer += qlqsMots

						if self.tour>self.nb_tours:
							self.etat="FIN_JEU"
						else:
							self.send(user, "_Bien reçu, patientez pendant que les autres joueurs complètent l'histoire_")
							self.send(self.joueurs[self.indice_joueur], msg_a_envoyer)

					self.joueur_courant = self.joueurs[self.indice_joueur]
					self.indice_joueur = (self.indice_joueur+1)%len(self.joueurs)

				else:
					self.send(user, "Ce n'est pas votre tour, "+getRandomCitation())
			else:
				self.send(user, "Une partie est déjà en cours ¯\_(ツ)_/¯\nAttendez la v2 pour pouvoir lancer plusieurs parties simultanées")

		if self.etat=="FIN_JEU":
			his=''
			for mot in self.mots:
				his += mot + ' '
			self.sendToAll(self.joueurs, "_Histoire terminée :_\n" + his)
			self.etat = "CONNECTE"

			
			
			
			
	def run(self):
		"""Point d'entrée du programme, écoute constament les messages en provenence de slack et appelle la méthode process s'il s'agit d'un message texte d'un utilisateur"""

		if self.bot.rtm_connect():
			self.etat="CONNECTE"
			print("connecté à Slack")
			try:
				while True:
					messages = self.bot.rtm_read()
					if messages:
						for message in messages :
							if "type" in message and message['type'] == 'message':
								if message['user'] != self.bot_id:
									self.process(message['user'], message['text'])

					else:
						sleep(0.01)
			except KeyboardInterrupt:
				pass
		else:
			print("connexion échouée")

			
			
			
if __name__ == "__main__":
	bot = Faqfinoubot(TOKEN)
	bot.run()
