from random import choice

patience = [
	{"auteur": "Jean-Pierre Jarroux", "citation":"Pas de patience, pas de science."},
	{"auteur": "Philip Massinger", "citation": "La patience est la vertu des mendiants."},
	{"auteur": "André Pronovost ", "citation": "La patience est presque l'amour."},
	{"auteur": "Jean Anglade", "citation": "Les meilleures choses ont besoin de patience."},
	{"auteur": "Alessandro Morandotti", "citation": "La patience est une vertu qui s'acquiert avec de la patience."},
	{"auteur": "Mahomet", "citation": "La patience est la clé du bien-être."},
	{"auteur": "Proverbe oriental ", "citation": "On vient à bout de ses desseins avec la patience."},
	{"auteur": "Abi Taleb ", "citation": "Un instant de patience est déjà une victoire."},
	{"auteur": "Hafiz", "citation": "Le découragement est beaucoup plus douloureux que la patience."},
	{"auteur": "Bouddha", "citation": "La patience est la plus grande des prières."},
	{"auteur": "Philippe Obrecht", "citation": "La patience est le sourire de l'âme."},
	{"auteur": "auteur inconnu", "citation": "Le papier a plus de patience que les gens."},
	{"auteur": "Horace / Odes ", "citation":"La patience adoucit tout mal sans remède."},
	{"auteur": "Horace / Odes ", "citation":"La patience adoucit tout mal sans remède."},
	{"auteur": "Niro", "citation":"Un peu de patience bientôt j'envoie la purée."}
]

def getRandomCitation():
	citation = choice(patience)
	return "\n_\"" +  citation["citation"] + "\"_ de " + citation["auteur"]
