"""Module 4 : audit de l'exécution avec globals() et locals().

IMPORTANT : globals() et locals() décrivent l'endroit où ils sont appelés.
Il faut donc les appeler dans le code à auditer, puis les passer en
argument : exporter_audit(globals(), locals())
"""

import datetime


def nom_du_type(valeur) -> str:
    """Donne le nom du type d'une valeur, en français."""
    match valeur:
        case bool():
            return 'booléen'
        case int():
            return 'entier'
        case float():
            return 'décimal'
        case str():
            return 'texte'
        case tuple():
            return 'tuple'
        case list():
            return 'liste'
        case frozenset():
            return 'frozenset'
        case set():
            return 'set'
        case dict():
            return 'dictionnaire'
        case _:
            nom_classe = str(type(valeur))     # ex : "<class 'function'>"
            if nom_classe == "<class 'function'>":
                return 'fonction'
            if nom_classe == "<class 'generator'>":
                return 'générateur'
            return nom_classe


def taille(valeur) -> str:
    """Nombre d'éléments d'une valeur, ou '-' si cela n'a pas de sens."""
    try:
        return str(len(valeur))
    except TypeError:
        return '-'                       # un nombre ou une fonction n'a pas de len()


def apercu(valeur) -> str:
    """Début de la valeur, coupé à 50 caractères."""
    texte = str(valeur)
    if len(texte) > 50:
        texte = texte[:50] + '...'
    return texte


def est_a_auditer(nom: str, valeur) -> bool:
    """Écarte les variables internes de Python et les modules importés."""
    if nom[:2] == '__':
        return False
    if str(type(valeur)) == "<class 'module'>":
        return False
    return True


def decrire_portee(portee: dict) -> list:
    """Décrit les variables d'une portée (résultat de globals() ou locals())."""
    # list(...) fait une copie : la portée ne change pas pendant qu'on la parcourt
    variables = filter(lambda paire: est_a_auditer(paire[0], paire[1]),
                       list(portee.items()))
    description = []
    for nom, valeur in variables:
        description.append((nom, nom_du_type(valeur), taille(valeur), apercu(valeur)))
    return description


def exporter_audit(variables_globales: dict, variables_locales: dict,
                   chemin: str = 'rapport_audit.txt') -> tuple:
    """Écrit le rapport d'audit dans un fichier texte."""
    globales = decrire_portee(variables_globales)
    locales = decrire_portee(variables_locales)
    maintenant = datetime.datetime.now()

    try:
        with open(chemin, 'w', encoding='utf-8') as f:
            f.write(f"RAPPORT D'AUDIT - {maintenant}\n")
            for titre, liste in (('VARIABLES GLOBALES', globales),
                                 ('VARIABLES LOCALES', locales)):
                f.write(f"\n=== {titre} ({len(liste)}) ===\n")
                f.write("nom | type | taille | aperçu\n")
                for nom, type_valeur, nb_elements, debut in liste:
                    f.write(f"{nom} | {type_valeur} | {nb_elements} | {debut}\n")
    except IOError as e:
        print(f"Erreur d'écriture du rapport d'audit : {e}")

    return globales, locales
