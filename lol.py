
nbTours=5
nbMotsApparents=3
histoire=""

for i in range(nbTours):
	
	print("\n"*10);
	
	print("tour " + str(i+1) + "/" + str(nbTours), end=" : ")
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