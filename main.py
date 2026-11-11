"""LogSentinel : programme principal.

Enchaîne les 4 modules du projet sur le fichier de logs, étape par étape,
avec une pause entre chaque étape pour la présentation.
"""

import time

from lecture_log import lire_fichier, ligne_en_dico                       # module 1
from nettoyage_log import normaliser                                       # module 2
from aggregation import (BLACKLIST, analyser_logs,                         # module 3
                         operations_ensembles, detecter_force_brute)
from regles import (apply_security_rules, enregistrer_alertes,             # module 4
                    regle_niveau_critique, regle_liste_noire,
                    regle_echec_connexion, regle_force_brute)
from audit import exporter_audit

CHEMIN_LOGS: str = 'logs/logs_jour.txt'


def pause() -> None:
    """Attend qu'on appuie sur Entrée avant de passer à l'étape suivante."""
    input('\n   [Entrée pour continuer]\n')


def titre(texte: str) -> None:
    print('=' * 70)
    print(texte)
    print('=' * 70)


def logs_propres(chemin: str):
    """Modules 1 et 2 : lecture puis nettoyage, une ligne à la fois.
    La chaîne est recréée à chaque appel, car un générateur ne se parcourt qu'une fois."""
    lignes = lire_fichier(chemin)                                         # yield
    lignes_non_vides = filter(None, lignes)                               # lignes vides
    lignes_valides = filter(lambda ligne: len(ligne.split('|')) == 7,     # lignes coupées
                            lignes_non_vides)
    logs = map(ligne_en_dico, lignes_valides)                             # dictionnaires
    return filter(None, map(normaliser, logs))                            # normalisation


def main() -> None:
    titre('LOGSENTINEL : analyse de logs et détection d\'attaques')
    print(f'Fichier analysé : {CHEMIN_LOGS}')
    pause()

    # ---------------------------------------------------------------
    titre('MODULE 1 : lecture ligne par ligne avec yield')
    debut = time.perf_counter()
    for i, ligne in enumerate(lire_fichier(CHEMIN_LOGS)):
        if i == 5:
            break                                # le reste du fichier n'est pas lu
        print('  ', ligne)
    print(f'\n   5 premières lignes lues en {time.perf_counter() - debut:.4f} seconde')
    print('\n   Une ligne transformée en dictionnaire :')
    exemple = next(filter(lambda ligne: len(ligne.split('|')) == 7,
                          filter(None, lire_fichier(CHEMIN_LOGS))))
    print('   AVANT :', exemple)
    print('   APRÈS :', ligne_en_dico(exemple))
    pause()

    # ---------------------------------------------------------------
    titre('MODULE 2 : nettoyage (filter, lambda, map, match-case)')
    nb_depart = sum(1 for _ in lire_fichier(CHEMIN_LOGS))
    nb_non_vides = sum(1 for _ in filter(None, lire_fichier(CHEMIN_LOGS)))
    nb_propres = sum(1 for _ in logs_propres(CHEMIN_LOGS))
    print(f'   Lignes au départ            : {nb_depart}')
    print(f'   Après filter(None)          : {nb_non_vides}  ({nb_depart - nb_non_vides} lignes vides enlevées)')
    print(f'   Après filter + lambda, map  : {nb_propres}  ({nb_non_vides - nb_propres} lignes incomplètes enlevées)')
    print('\n   Le match-case reconnaît aussi les autres formes :')
    print('   tuple ->', normaliser(('45.33.32.156', 22, 'SSH')))
    print('   42    ->', normaliser(42))
    pause()

    # ---------------------------------------------------------------
    titre('MODULE 3 : analyse (set, frozenset, defaultdict, force brute)')
    resultats = analyser_logs(logs_propres(CHEMIN_LOGS))

    print('   Opérations avec la liste noire (frozenset) :')
    for nom, valeur in operations_ensembles(resultats['ips_actives']).items():
        print(f'     {nom} : {sorted(valeur)}')

    print('\n   Logs par niveau (defaultdict) :')
    for niveau, nombre in resultats['par_niveau'].items():
        print(f'     {niveau} : {nombre}')

    print()
    suspects = detecter_force_brute(resultats['echecs_par_ip'])
    print('\n   Attaques par force brute détectées :')
    for ip, serie in suspects.items():
        print(f'     {ip} : {serie} échecs consécutifs')
    pause()

    # ---------------------------------------------------------------
    titre('MODULE 4 : moteur de règles (*args, **kwargs) et audit')
    alertes = apply_security_rules(
        regle_niveau_critique,                   # *args : les règles
        regle_liste_noire,
        regle_echec_connexion,
        regle_force_brute,
        logs=logs_propres(CHEMIN_LOGS),          # **kwargs : les logs...
        liste_noire=BLACKLIST,                   # ... et la configuration
        ips_force_brute=suspects,
        niveaux_alerte=('CRITICAL',),
    )
    compteur = enregistrer_alertes(alertes, 'alertes.txt')

    print('   Alertes par règle :')
    for regle, nombre in compteur.items():
        print(f'     {regle} : {nombre}')

    exporter_audit(globals(), locals(), 'rapport_audit.txt')
    print('\n   Fichiers créés : alertes.txt et rapport_audit.txt')
    print('\nFin de l\'analyse.')


if __name__ == '__main__':
    main()
