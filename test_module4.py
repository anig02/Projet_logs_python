"""Test du module 4 seul, avec quelques logs écrits à la main
au même format que ceux des modules 1 et 2."""

from regles import (apply_security_rules, enregistrer_alertes,
                    regle_niveau_critique, regle_liste_noire,
                    regle_echec_connexion, regle_force_brute)
from audit import exporter_audit

BLACKLIST: frozenset = frozenset({'84.203.17.92', '151.6.240.33',
                                  '198.51.100.23', '203.0.113.7'})


def creer_logs_de_test():
    """Générateur de faux logs propres."""
    yield {'date': '2026-10-15 00:47:11', 'niveau': 'ERROR', 'utilisateur': 'user03',
           'message': 'Mot de passe incorrect', 'connexion': ('45.33.32.156', 22, 'SSH')}
    yield {'date': '2026-10-15 00:47:12', 'niveau': 'ERROR', 'utilisateur': 'user03',
           'message': 'Mot de passe incorrect', 'connexion': ('45.33.32.156', 22, 'SSH')}
    yield {'date': '2026-10-15 00:48:02', 'niveau': 'CRITICAL', 'utilisateur': 'user01',
           'message': 'Serveur arrete', 'connexion': ('84.203.17.92', 443, 'HTTPS')}
    yield {'date': '2026-10-15 00:49:30', 'niveau': 'INFO', 'utilisateur': 'user02',
           'message': 'Connexion reussie', 'connexion': ('10.12.4.101', 80, 'HTTP')}
    yield {'date': '2026-10-15 00:50:00', 'niveau': 'INFO', 'utilisateur': 'user04'}  # incomplet


def lancer_demo() -> None:
    ips_force_brute = {'45.33.32.156': 6}    # en vrai : résultat du module 3

    alertes = apply_security_rules(
        regle_niveau_critique,                 # *args : les règles
        regle_liste_noire,
        regle_echec_connexion,
        regle_force_brute,
        logs=creer_logs_de_test(),             # **kwargs : les logs...
        liste_noire=BLACKLIST,                 # ... et la configuration
        ips_force_brute=ips_force_brute,
        niveaux_alerte=('CRITICAL',),
    )
    compteur = enregistrer_alertes(alertes, 'alertes.txt')

    print("Alertes par règle :")
    for regle, nombre in compteur.items():
        print(f"  {regle} : {nombre}")

    exporter_audit(globals(), locals(), 'rapport_audit.txt')
    print("Fichiers créés : alertes.txt et rapport_audit.txt")


lancer_demo()
