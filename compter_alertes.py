"""Calcule les vrais nombres d'alertes du module 4 sur le gros fichier de logs.

Ce fichier refait la même chaîne que les modules 1 et 2 (lecture, nettoyage),
puis applique les règles du module 4. Il utilise les résultats du module 3
(liste noire et adresses de force brute), recopiés depuis le rapport.
"""

from regles import (apply_security_rules, enregistrer_alertes,
                    regle_niveau_critique, regle_liste_noire,
                    regle_echec_connexion, regle_force_brute)
from audit import exporter_audit
from lecture_log import lire_fichier                                    # module 1
from aggregation import BLACKLIST, analyser_logs, detecter_force_brute  # module 3

CHEMIN_LOGS: str = 'logs/logs_jour.txt'

def ligne_en_dico(ligne: str) -> dict | None:
    """Transforme une ligne en dictionnaire propre (modules 1 et 2)."""
    morceaux = ligne.split('|')
    try:
        date, niveau, ip, utilisateur, message, port, protocole = morceaux
        return {
            'date': date.strip(),
            'niveau': niveau.strip().upper(),
            'utilisateur': utilisateur.strip().lower(),
            'message': message.strip(),
            'connexion': (ip.strip(), int(port), protocole.strip()),
        }
    except ValueError:
        return None


def logs_propres(chemin: str):
    """Chaîne lecture + nettoyage. On la recrée à chaque fois qu'on en a besoin,
    car un générateur ne peut être parcouru qu'une seule fois."""
    lignes_non_vides = filter(None, lire_fichier(chemin))
    lignes_valides = filter(lambda ligne: len(ligne.split('|')) == 7 and ligne.split('|')[2].strip() != '', lignes_non_vides)
    logs = map(ligne_en_dico, lignes_valides)
    return filter(None, logs)


def lancer() -> None:
    # 1er parcours : vérifier qu'on a bien les mêmes logs que le module 2
    nb_logs = 0
    for log in logs_propres(CHEMIN_LOGS):
        nb_logs += 1
    print(f"Logs propres : {nb_logs}   (attendu : 996180)")

    # Module 3 : on calcule les IP de force brute (au lieu de les recopier)
    resultats = analyser_logs(logs_propres(CHEMIN_LOGS))
    suspects = detecter_force_brute(resultats['echecs_par_ip'])

    # 2e parcours : le moteur de règles
    alertes = apply_security_rules(
        regle_niveau_critique,
        regle_liste_noire,
        regle_echec_connexion,
        regle_force_brute,
        logs=logs_propres(CHEMIN_LOGS),
        liste_noire=BLACKLIST,
        ips_force_brute=suspects,
        niveaux_alerte=('CRITICAL',),
    )
    compteur = enregistrer_alertes(alertes, 'alertes.txt')

    print("\nAlertes par règle :")
    for regle, nombre in compteur.items():
        print(f"  {regle} : {nombre}")

    exporter_audit(globals(), locals(), 'rapport_audit.txt')
    print("\nFichiers créés : alertes.txt et rapport_audit.txt")


if __name__ == '__main__':
    lancer()
