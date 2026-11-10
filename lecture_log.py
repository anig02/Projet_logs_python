
'''lecture avec yield'''

def lire_fichier(nom_fichier):
    with open(nom_fichier, 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            # strip() enlève le saut de ligne invisible (\n) à la fin,
            # pour avoir une vraie ligne avec toutes les informations
            yield ligne.strip()


# TEST 1 : lecture avec yield -> on affiche les 5 premières lignes
'''compteur = 0
for ligne in lire_fichier('logs/logs_jour.txt'):
    print(ligne)
    compteur += 1
    if compteur == 5:
        break ''' 





'''lecture avec yield From '''

def lire_fichiers(list_fichier):
    for fichier in list_fichier:
        yield from lire_fichier(fichier)


fichiers = ['logs/logs_jour.txt']


# TEST 2 : lecture avec yield from -> pareil, avec la liste de fichiers
'''compteur = 0
for ligne in lire_fichiers(fichiers):
    print(ligne)
    compteur += 1
    if compteur == 5:
        break'''






''' Transforme UNE ligne de texte en dictionnaire'''

def ligne_en_dico(ligne):
    morceaux = ligne.split(' | ')
    date, niveau, ip, utilisateur, message, port, protocole = morceaux
    return {
        'date': date,
        'niveau': niveau,
        'utilisateur': utilisateur,
        'message': message,
        'connexion': (ip, int(port), protocole),
    }



# TEST 3 : chaque ligne devient un dictionnaire
'''compteur = 0
for ligne in lire_fichiers(fichiers):
    if ligne == '':      # on saute les lignes vides
        continue
    print(ligne_en_dico(ligne))
    compteur += 1
    if compteur == 5:
        break'''
