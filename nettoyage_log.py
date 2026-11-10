from lecture_log import lire_fichiers, fichiers, ligne_en_dico

lignes= lire_fichiers(fichiers)

lignes_non_vides = filter(None, lignes) 

# TEST 4  : filter(None) -> les lignes vides sont enlevées
'''compteur = 0
for ligne in filter(None, lire_fichiers(fichiers)):
    print(ligne)
    compteur += 1
    if compteur == 5:
        break'''



lignes_valides = filter(lambda ligne: len(ligne.split(' | ')) == 7, lignes_non_vides)
#filter ne supprime rien, il laisse passer seulement les lignes qui ne sont pas
#  vides. Les lignes vides sont simplement ignorées :
#  elles ne sont pas transmises à la suite du programme. 
# Le fichier, lui, reste intact.
# lambda : on garde seulement les lignes complètes (7 morceaux)


# TEST 5 : lambda -> seulement les lignes complètes
compteur = 0
'''for ligne in filter(lambda ligne: len(ligne.split(' | ')) == 7, lire_fichiers(fichiers)):
    print(ligne)
    compteur += 1
    if compteur == 5:
        break'''







# Donne le 'chemin' de la transformation en dico 
logs = map(ligne_en_dico, lignes_valides)


def normaliser(log):
    match log:
        case {'date': str(date), 'connexion': (str(ip), int(port), str(protocole))}:
            log['niveau'] = log['niveau'].strip().upper()            
            log['utilisateur'] = log['utilisateur'].strip().lower()  
            return log
        case str():                                                  
            return ligne_en_dico(log)                                 
        case (ip, port, protocole):                                   
            return f'Connexion de {ip} sur le port {port} ({protocole})'  
        case _:
            return None



logs_propres = map(normaliser, logs)


# TEST 6 : map + normaliser -> les logs en dictionnaires propres
'''compteur = 0
for log in logs_propres:
    print(log)
    compteur += 1
    if compteur == 5:
        break'''






