
#Prend en entrée l'itérateur de logs propres (module 2) et produit :
- les IP uniques en erreur (set) et les opérations avec la blacklist (frozenset) ;
- des compteurs par niveau et par utilisateur (defaultdict) ;
- la détection d'attaques par force brute (while / for / break / continue / else).
"""
import datetime
from collections import defaultdict

NIVEAUX_ERREUR = {'ERROR', 'CRITICAL'}
MESSAGE_ECHEC = 'Mot de passe incorrect'
SEUIL_FORCE_BRUTE = 5      # nombre d'échecs rapprochés pour parler d'attaque
ECART_MAX_SECONDES = 5     # deux échecs sont "rapprochés" s'ils sont à <= 5 s

# Liste noire immuable : elle ne doit pas changer pendant l'analyse
BLACKLIST: frozenset = frozenset({
    '84.203.17.92', '151.6.240.33', '198.51.100.23', '203.0.113.7',
})


def convertir_date(texte: str) -> datetime.datetime:
    """Transforme '2026-10-12 08:00:01' en objet datetime."""
    jour, heure = texte.split(' ')
    annee, mois, num_jour = jour.split('-')
    h, minute, seconde = heure.split(':')
    return datetime.datetime(int(annee), int(mois), int(num_jour),
                             int(h), int(minute), int(seconde))


def analyser_logs(logs) -> dict:
    """Parcourt les logs UNE seule fois et remplit toutes les structures."""
    ips_erreur: set = set()
    ips_actives: set = set()
    par_niveau = defaultdict(int)
    par_utilisateur = defaultdict(int)
    # Pour chaque IP : la liste des dates de ses échecs de connexion
    echecs_par_ip = defaultdict(list)

    for log in logs:
        try:
            ip = log['connexion'][0]
            niveau = log['niveau']
            utilisateur = log['utilisateur']
            message = log['message']
            date = log['date']
        except KeyError:
            continue  # clé manquante : on ignore ce log
        except TypeError:
            continue  # log vide (None) : on l'ignore

        ips_actives.add(ip)
        par_niveau[niveau] += 1
        par_utilisateur[utilisateur] += 1
        if niveau in NIVEAUX_ERREUR:
            ips_erreur.add(ip)

        if message == MESSAGE_ECHEC:
            try:
                echecs_par_ip[ip].append(convertir_date(date))
            except ValueError:
                continue  # date illisible : on ignore cet échec

    return {
        'ips_erreur': ips_erreur,
        'ips_actives': ips_actives,
        'par_niveau': par_niveau,
        'par_utilisateur': par_utilisateur,
        'echecs_par_ip': echecs_par_ip,
    }


def operations_ensembles(ips_actives: set, blacklist: frozenset = BLACKLIST) -> dict:
    """Opérations mathématiques entre IP actives et IP blacklistées."""
    return {
        'union (|)': ips_actives | blacklist,
        'intersection (&) : blacklistées ET actives': ips_actives & blacklist,
        'actives non blacklistées (-)': ips_actives - blacklist,
        'blacklistées inactives (-)': blacklist - ips_actives,
        'différence symétrique (^)': ips_actives ^ blacklist,
    }


def detecter_force_brute(echecs_par_ip: dict, seuil: int = SEUIL_FORCE_BRUTE,
                         ecart_max: int = ECART_MAX_SECONDES) -> dict:
    """Renvoie {ip: longueur de la série} pour les IP ayant au moins `seuil`
    échecs de connexion consécutifs, chacun à moins de `ecart_max` secondes
    du précédent."""
    suspects = {}
    ips_saines = 0
    ecart_limite = datetime.timedelta(seconds=ecart_max)

    for ip, echecs in echecs_par_ip.items():
        i = 0
        while i < len(echecs):
            # Mesure la série d'échecs rapprochés qui commence en i
            serie = 1
            for j in range(i + 1, len(echecs)):
                if echecs[j] - echecs[j - 1] > ecart_limite:
                    break              # trop de temps écoulé : la série s'arrête
                serie += 1

            if serie < seuil:
                i += serie             # série trop courte : on passe à la suivante
                continue

            suspects[ip] = serie       # attaque trouvée
            break                      # inutile de continuer pour cette IP
        else:
            # Le while est allé au bout sans break : tous les échecs de cette
            # IP ont été examinés et aucune attaque n'a été trouvée
            ips_saines += 1

    print(f"[force brute] {ips_saines} IP examinées entièrement sans attaque")
    return suspects


def main() -> None:
    from nettoyage_log import logs_propres  # module 2 (adapter le nom du fichier)

    resultats = analyser_logs(logs_propres)

    print("IP uniques en erreur :", resultats['ips_erreur'])

    print("\nOpérations avec la blacklist :")
    for nom, valeur in operations_ensembles(resultats['ips_actives']).items():
        print(f"  {nom} : {valeur}")

    print("\nLogs par niveau :")
    for niveau, nombre in resultats['par_niveau'].items():
        print(f"  {niveau} : {nombre}")

    print("\nLogs par utilisateur :")
    for utilisateur, nombre in resultats['par_utilisateur'].items():
        print(f"  {utilisateur} : {nombre}")

    suspects = detecter_force_brute(resultats['echecs_par_ip'])
    print("\nAttaques par force brute détectées :")
    for ip, serie in suspects.items():
        print(f"  {ip} : {serie} échecs consécutifs")


# Évite que main() se lance quand un autre fichier (ex : main.py) importe ce module
if __name__ == '__main__':
    main()
