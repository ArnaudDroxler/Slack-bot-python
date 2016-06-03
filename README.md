# Faqfinoucha 

## But
Implémenter le jeu du [cadavre exquis](https://fr.wikipedia.org/wiki/Cadavre_exquis_(jeu)) à l'aide d'un bot Slack.

## Fonctionnement
1. Un joueur "admin" veux lancer une partie, il en informe le bot
2. Pour configurer la partie, le bot demande à l'admin :
 * une liste de joueurs
 * le nombre de tour par joueur
 * le nombre de mots apparents à chaque tour*
 * (le temps de timeout, au bout duquel le bot passe le tour d'un joueur inactif) ?
3. Le bot contacte chaque joueur pour l'informer qu'il est dans le jeu
4. (Le joueur peut refuser de faire partie du jeu) ?
4. Le bot demande aux joueurs de compléter l'histoire chacun leur tour. A chaque tour, il répète :
  * montrer au joueur courant les qlqs derniers mots de l'histoire (selon la configuration de la partie)
  * ajouter les mots entrés par le joueur dans l'histoire
  * passer au joueur suivant
5. Le bot montre l'histoire finie à tous les joueurs
