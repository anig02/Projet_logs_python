# LogSentinel – Security log analysis in Python

**Team project (3 students) – ECE Paris, 2026–2027**
Mariam Mahamma, Anais Akroud, Ani Guettab

LogSentinel reads very large server log files **without loading them into memory**
(Python generators), cleans the data, and automatically detects **brute-force attacks**.

**Key results**
- Generated realistic synthetic logs with injected errors and attacks, up to **15 GB (188 million lines)**
- Full pass over 1 million lines using only **~0.16 MB of memory**
- Cleaning pipeline (filter, map, normalisation): **996,180 valid logs** kept out of 1,056,173 lines
- Detected **all 6 attacker IPs with no false positives**, using a time-window rule (≥ 5 failed logins, ≤ 5 s apart)
- Modular security rule engine: adding a new rule only requires writing a new function

**Tech:** Python, generators (`yield`), `set` / `frozenset`, `defaultdict`, `match-case`, Git

**Run:** `python creation_log.py` then `python main.py`

---

*Version française ci-dessous / French version below*

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
