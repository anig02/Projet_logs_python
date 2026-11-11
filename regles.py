"""Module 4 : moteur de règles de sécurité.

Une règle de sécurité est une fonction qui reçoit un log (dictionnaire)
et la configuration (dictionnaire). Elle renvoie une alerte (dictionnaire)
si le log est suspect, et None sinon.

Format d'un log (fourni par les modules 1 et 2) :
{'date': '2026-10-15 00:47:11', 'niveau': 'ERROR', 'utilisateur': 'user03',
 'message': 'Mot de passe incorrect', 'connexion': ('45.33.32.156', 22, 'SSH')}
"""

from collections import defaultdict

NIVEAUX_ALERTE: tuple = ('CRITICAL',)
MESSAGE_ECHEC: str = 'Mot de passe incorrect'


def creer_alerte(nom_regle: str, log: dict, detail: str) -> dict:
    """Construit une alerte, avec le même format pour toutes les règles."""
    ip, port, protocole = log['connexion']
    return {
        'regle': nom_regle,
        'date': log['date'],
        'ip': ip,
        'utilisateur': log['utilisateur'],
        'detail': f"{detail} (port {port}, {protocole})",
    }


# ----------------------------------------------------------------------
# Les règles de sécurité
# ----------------------------------------------------------------------

def regle_niveau_critique(log: dict, config: dict) -> dict | None:
    """Alerte si le niveau du log fait partie des niveaux surveillés."""
    niveaux = config.get('niveaux_alerte', NIVEAUX_ALERTE)
    if log['niveau'] in niveaux:
        return creer_alerte('niveau_critique', log,
                            f"Log {log['niveau']} : {log['message']}")
    return None


def regle_liste_noire(log: dict, config: dict) -> dict | None:
    """Alerte si l'adresse IP fait partie de la liste noire (frozenset)."""
    liste_noire = config.get('liste_noire', frozenset())
    ip = log['connexion'][0]
    if ip in liste_noire:
        return creer_alerte('liste_noire', log,
                            f"Activité d'une IP de la liste noire : {ip}")
    return None


def regle_echec_connexion(log: dict, config: dict) -> dict | None:
    """Alerte sur chaque mot de passe incorrect."""
    if log['message'] == MESSAGE_ECHEC:
        return creer_alerte('echec_connexion', log,
                            f"Mot de passe incorrect pour {log['utilisateur']}")
    return None


def regle_force_brute(log: dict, config: dict) -> dict | None:
    """Alerte si l'IP a mené une attaque par force brute (résultat du module 3)."""
    ips_force_brute = config.get('ips_force_brute', {})
    ip = log['connexion'][0]
    if ip in ips_force_brute:
        return creer_alerte('force_brute', log,
                            f"Activité d'une IP auteure d'une force brute : {ip}")
    return None


# ----------------------------------------------------------------------
# La fonction maître demandée par l'énoncé
# ----------------------------------------------------------------------

def apply_security_rules(*args, **kwargs):
    """Applique un nombre variable de règles à un flux de logs.

    *args    : les fonctions de règles (rassemblées dans un tuple).
    **kwargs : 'logs' (les logs à analyser) et la configuration
               (rassemblés dans un dictionnaire).

    C'est un générateur : les alertes sont produites une par une.
    """
    logs = kwargs.get('logs', [])

    # Tout ce qui n'est pas 'logs' est de la configuration
    config: dict = {}
    for cle, valeur in kwargs.items():
        if cle != 'logs':
            config[cle] = valeur

    for log in logs:
        for regle in args:
            try:
                alerte = regle(log, config)
            except (KeyError, IndexError, TypeError, ValueError):
                continue          # log incomplet : on passe à la règle suivante
            if alerte is not None:
                yield alerte


def enregistrer_alertes(alertes, chemin: str = 'alertes.txt') -> defaultdict:
    """Écrit les alertes dans un fichier, une par ligne, et les compte par règle."""
    compteur = defaultdict(int)
    try:
        with open(chemin, 'w', encoding='utf-8') as f:
            for alerte in alertes:
                compteur[alerte['regle']] += 1
                f.write(f"{alerte['date']} | {alerte['regle']} | {alerte['ip']}"
                        f" | {alerte['utilisateur']} | {alerte['detail']}\n")
    except IOError as e:
        print(f"Erreur d'écriture du fichier d'alertes : {e}")
    return compteur
