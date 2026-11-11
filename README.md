# LogSentinel : analyse de logs et détection d'attaques en Python

Projet Python – ECE, Groupe 3 : Mariam Mahamma, Anais Akroud, Ani Guettab.

Programme qui lit des fichiers de logs de très grande taille **sans les charger
entièrement en mémoire** (générateurs `yield`), les nettoie, les analyse et
détecte les attaques par force brute.

## Installation

```bash
python -m venv venv
venv\Scripts\activate          # Windows
python -m pip install -r requirements.txt
```

## Lancement

```bash
python creation_log.py         # crée logs/logs_jour.txt (1 million de lignes)
python main.py                 # lance tout le programme, étape par étape
```

## Organisation

| Fichier | Rôle |
|---|---|
| `creation_log.py` | Création des fichiers de logs (avec erreurs et attaques) |
| `lecture_log.py` | Module 1 : lecture avec `yield` et `yield from` |
| `nettoyage_log.py` | Module 2 : `filter`, `lambda`, `map`, `match-case` |
| `aggregation.py` | Module 3 : `set`, `frozenset`, `defaultdict`, force brute |
| `regles.py`, `audit.py` | Module 4 : moteur de règles, `globals()` / `locals()` |
| `main.py` | Programme principal |
