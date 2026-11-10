from lecture_log import lire_fichiers, fichiers, ligne_en_dico

lignes= lire_fichiers(fichiers)

lignes_non_vides = filter(None, lignes) 
# TEST 4 : filter(None) -> combien de lignes vides enlevées
'''total = 0
for ligne in lire_fichiers(fichiers):
    total += 1

non_vides = 0
for ligne in filter(None, lire_fichiers(fichiers)):
    non_vides += 1

print(f"Lignes au départ : {total}")
print(f"Lignes après filter(None) : {non_vides}")
print(f"Lignes vides enlevées : {total - non_vides}")'''



lignes_valides = filter(lambda ligne: len(ligne.split(' | ')) == 7, lignes_non_vides)
#filter ne supprime rien, il laisse passer seulement les lignes qui ne sont pas
#  vides. Les lignes vides sont simplement ignorées :
#  elles ne sont pas transmises à la suite du programme. 
# Le fichier, lui, reste intact.
# lambda : on garde seulement les lignes complètes (7 morceaux)


# TEST 5 : lambda -> combien de lignes incomplètes enlevées
'''non_vides = 0
for ligne in filter(None, lire_fichiers(fichiers)):
    non_vides += 1

completes = 0
for ligne in filter(lambda ligne: len(ligne.split(' | ')) == 7, filter(None, lire_fichiers(fichiers))):
    completes += 1

print(f"Lignes non vides : {non_vides}")
print(f"Lignes complètes après le lambda : {completes}")
print(f"Lignes incomplètes enlevées : {non_vides - completes}")

# quelques exemples de lignes rejetées
exemples = 0
for ligne in filter(lambda ligne: len(ligne.split(' | ')) != 7, filter(None, lire_fichiers(fichiers))):
    print("Rejetée :", ligne)
    exemples += 1
    if exemples == 3:
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


# TEST 6 : normaliser -> combien de logs corrigés + exemples avant / après
'''corriges = 0
for ligne in filter(lambda ligne: len(ligne.split(' | ')) == 7, filter(None, lire_fichiers(fichiers))):
    log = ligne_en_dico(ligne)
    avant = (log['niveau'], log['utilisateur'])   # on garde l'ancienne version AVANT normaliser
    log = normaliser(log)
    apres = (log['niveau'], log['utilisateur'])
    if avant != apres:
        corriges += 1
        if corriges <= 5:
            print(f"Avant : {avant}  ->  Après : {apres}")

print(f"Logs corrigés par normaliser : {corriges}")'''






