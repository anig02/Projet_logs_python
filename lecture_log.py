
'''lecture avec yield'''

# yield permet de lire le fichier ligne par ligne : il lit une ligne, la donne,
# fait une pause, puis lit la suivante. Il ne lit pas tout le fichier d'un coup,
# ce qui économise la mémoire (indispensable pour les très gros fichiers).
def lire_logs(nom_fichier):
    with open(nom_fichier, 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            # strip() enlève le saut de ligne invisible (\n) à la fin,
            # pour avoir une vraie ligne avec toutes les informations
            yield ligne.strip()



'''lecture avec yield From '''

def lire_plusieurs_fichier(list_fichier):
    for fichier in list_fichier:
        yield from lire_logs(fichier)

#test

fichiers = ['logs/logs_jour1.txt', 'logs/logs_jour2.txt',
            'logs/logs_jour3.txt', 'logs/logs_jour4.txt']

'''for ligne in lire_plusieurs_fichier(fichiers):
    print(ligne)'''


# Transforme UNE ligne de texte en dictionnaire
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


# Lit un fichier et donne chaque ligne sous forme de dictionnaire
def transformation_ligne_dico(nom_fichier):
    for ligne in lire_logs(nom_fichier):
        yield ligne_en_dico(ligne)


def lire_plusieurs_fichier_bis(list_fichier):
    for fichier in list_fichier:
        yield from transformation_ligne_dico(fichier)