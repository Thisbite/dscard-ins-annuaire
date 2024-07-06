import sqlite3
import sqlite3

def create_tables():
    conn = sqlite3.connect('base_donnee.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS agent_collecte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_prenoms TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            numero TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS directeur (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_prenoms TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            numero TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS direction_region (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_direction TEXT NOT NULL,
            region TEXT NOT NULL,
            id_agent_collecte INTEGER,
            id_directeur INTEGER,
            FOREIGN KEY (id_agent_collecte) REFERENCES agent_collecte(id),
            FOREIGN KEY (id_directeur) REFERENCES directeur(id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS indicateur (
            id_indicateur INTEGER PRIMARY KEY AUTOINCREMENT,
            libelle TEXT NOT NULL,
            type_indicateur TEXT NOT NULL,
            id_domaine INTEGER,
            FOREIGN KEY (id_domaine) REFERENCES domaine(id_domaine)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS domaine (
            id_domaine INTEGER PRIMARY KEY AUTOINCREMENT,
            titre_domaine TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS region (
            id_region INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_region TEXT NOT NULL,
            nom_departement TEXT NOT NULL,
            nom_sous_prefecture TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS reponse (
            id_reponse INTEGER PRIMARY KEY AUTOINCREMENT,
            valeur_reponse TEXT NOT NULL,
            date_donnee TEXT NOT NULL,
            nom_agent_collecte TEXT NOT NULL,
            id_indicateur INTEGER,
            id_region INTEGER,
            FOREIGN KEY (id_indicateur) REFERENCES indicateur(id_indicateur),
            FOREIGN KEY (id_region) REFERENCES region(id_region)
        )
    ''')

    conn.commit()
    conn.close()

# Appel de la fonction pour créer les tables
create_tables()
