
nbToursParJoueur=0
nbMotsApparents=0
histoire=""
listeJoueur=[]
ptr=0

while(len(listeJoueur) < 1):
	print("Entrez le pseudo des joueurs, séparés par des espaces")
	listeJoueur = input().split()


def getNumberInput(question):
	variable=0
	while(variable < 1):
		print(question)
		try:
			variable = int(input())
		except:
			variable = 0
	return variable		
			
nbToursParJoueur = getNumberInput("Combien de tours par joueur ?")
nbMotsApparents = getNumberInput("Combien de mots apparents ?")
	
nbTours = nbToursParJoueur*len(listeJoueur)

for i in range(nbTours):
	
	print("\n"*10);
	
	print(listeJoueur[ptr] + " - tour " + str(i+1) + "/" + str(nbTours), end=" : ")
	ptr = (ptr+1)%len(listeJoueur)
	
	if(i==0):
		print("Commencez l'histoire")
	elif(i==nbTours-1):
		print("Finissez l'histoire")
	else:
		print("Continuez l'histoire")
	
	mots = histoire.split();
	for mot in mots[-nbMotsApparents:]:
		print(mot,end=' ')
	
	histoire += input()
	
	if(histoire[-1]!=' '):
		histoire += ' '
		

print("\n\nHistoire : " + histoire)