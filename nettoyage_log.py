from lecture_log import lire_plusieurs_fichier, fichiers, ligne_en_dico

lignes= lire_plusieurs_fichier(fichiers)
lignes_non_vides = filter(None, lignes)  
#filter ne supprime rien, il laisse passer seulement les lignes qui ne sont pas
#  vides. Les lignes vides sont simplement ignorées :
#  elles ne sont pas transmises à la suite du programme. 
# Le fichier, lui, reste intact.

lignes_valides= filter(lambda ligne: ligne.split(' | ')[2]!= '', lignes_non_vides)
#Affiche pas les lignes sans adresse ip et sans saut de ligne 


# Donne le 'chemin' de la transformation en dico 
logs = map(ligne_en_dico, lignes_valides)

#for log in logs:
    #print(log)