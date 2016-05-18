def getNumberInput(question):
	"""demande à l'utilisateur un entier plus grand que 0"""
	retour=0
	while(retour < 1):
		print(question)
		try:
			retour = int(input())
		except:
			retour = 0
	return retour		

"""initialisation des variables"""
nbToursParJoueur=0
nbMotsApparents=0
listeJoueur=[]
joueurDontCEstLeTour=0
histoire=[]

"""configuration de la partie"""
while(len(listeJoueur) < 1):
	print("Entrez le pseudo des joueurs, séparés par des espaces")
	listeJoueur = input().split()
nbToursParJoueur = getNumberInput("Combien de tours par joueur ?")
nbMotsApparents = getNumberInput("Combien de mots apparents ?")

nbTours = nbToursParJoueur*len(listeJoueur)

for tour in range(1,nbTours+1):
	print("\n"*10);
	
	print(listeJoueur[joueurDontCEstLeTour] + " - tour " + str(tour) + "/" + str(nbTours), end=" : ")
	"""chacun son tour, j1 puis j2 puis j3 puis à nouveau j1 etc..."""
	joueurDontCEstLeTour = (joueurDontCEstLeTour+1)%len(listeJoueur)
	
	"""selon l'avancement du jeu, on informe le joueur de ce qu'il doit faire"""
	if(tour==1):
		print("Commencez l'histoire")
	elif(tour==nbTours):
		print("Finissez l'histoire")
	else:
		print("Continuez l'histoire")
	
	"""on affiche les quelques derniers mots de l'histoire"""
	for mot in histoire[-nbMotsApparents:]:
		print(mot,end=' ')
	
	"""ajoute à l'histoire les nouveaux mots entrés par le joueur"""
	histoire += input().split()

	
"""affiche l'histoire finie"""
print("\n\nHistoire : ")
for mot in histoire:
	print(mot,end=' ')