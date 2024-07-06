import sqlite3
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
#c.execute("DROP TABLE directeur")

def create_tables():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS agent_collecte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_prenoms TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            matricule TEXT UNIQUE NOT NULL,
            numero TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS directeur (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_prenoms TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            matricule_dr TEXT UNIQUE NOT NULL,
            numero TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS direction_regionale (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_direction TEXT NOT NULL,
            region TEXT NOT NULL,
            matricule_agent INTEGER,
            matricule_dr TEXT,
            FOREIGN KEY (matricule_agent) REFERENCES agent_collecte(matricule),
            FOREIGN KEY (matricule_dr) REFERENCES directeur(matricule_dr)
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
            valeur_reponse TEXT ,
            date_donnee TEXT ,
            matricule_agent TEXT NOT NULL,
            id_indicateur INTEGER,
            id_region INTEGER,
            FOREIGN KEY (id_indicateur) REFERENCES indicateur(id_indicateur),
            FOREIGN KEY (id_region) REFERENCES region(id_region),
            FOREIGN KEY (matricule_agent) REFERENCES  agent_collecte(matricule)
        )
    ''')

    conn.commit()
    conn.close()

# Appel de la fonction pour créer les tables
create_tables()

### ********************************************************************* Enregistrer
def enregistrer_agent_collecte(nom_prenoms, email,matricule, numero, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO agent_collecte (nom_prenoms, email,matricule, numero, password)
        VALUES (?, ?, ?, ?)
    ''', (nom_prenoms, email,matricule, numero, password))

    conn.commit()
    conn.close()


def enregistrer_directeur(nom_prenoms, email, numero):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO directeur (nom_prenoms, email, numero)
        VALUES (?, ?, ?)
    ''', (nom_prenoms, email, numero))

    conn.commit()
    conn.close()


def enregistrer_direction_region(nom_direction, region, id_agent_collecte, id_directeur):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO direction_region (nom_direction, region, id_agent_collecte, id_directeur)
        VALUES (?, ?, ?, ?)
    ''', (nom_direction, region, id_agent_collecte, id_directeur))

    conn.commit()
    conn.close()


def enregistrer_indicateur(libelle, type_indicateur, id_domaine):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO indicateur (libelle, type_indicateur, id_domaine)
        VALUES (?, ?, ?)
    ''', (libelle, type_indicateur, id_domaine))

    conn.commit()
    conn.close()


def enregistrer_domaine(titre_domaine):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO domaine (titre_domaine)
        VALUES (?)
    ''', (titre_domaine,))

    conn.commit()
    conn.close()


def enregistrer_region(nom_region, nom_departement, nom_sous_prefecture):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO region (nom_region, nom_departement, nom_sous_prefecture)
        VALUES (?, ?, ?)
    ''', (nom_region, nom_departement, nom_sous_prefecture))

    conn.commit()
    conn.close()


def enregistrer_reponse(valeur_reponse, date_donnee, nom_agent_collecte, id_indicateur, id_region):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO reponse (valeur_reponse, date_donnee, nom_agent_collecte, id_indicateur, id_region)
        VALUES (?, ?, ?, ?, ?)
    ''', (valeur_reponse, date_donnee, nom_agent_collecte, id_indicateur, id_region))

    conn.commit()
    conn.close()

###**************************************************Modifier
def modifier_agent_collecte(id, nom_prenoms, email,matricule, numero, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        UPDATE agent_collecte
        SET nom_prenoms = ?, email = ?,matricule = ?, numero = ?, password = ?
        WHERE id = ?
    ''', (nom_prenoms, email,matricule, numero, password, id))

    conn.commit()
    conn.close()


def modifier_directeur(id, nom_prenoms, email, numero):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        UPDATE directeur
        SET nom_prenoms = ?, email = ?, numero = ?
        WHERE id = ?
    ''', (nom_prenoms, email, numero, id))

    conn.commit()
    conn.close()


def modifier_direction_region(id, nom_direction, region, id_agent_collecte, id_directeur):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        UPDATE direction_region
        SET nom_direction = ?, region = ?, id_agent_collecte = ?, id_directeur = ?
        WHERE id = ?
    ''', (nom_direction, region, id_agent_collecte, id_directeur, id))

    conn.commit()
    conn.close()


def modifier_indicateur(id_indicateur, libelle, type_indicateur, id_domaine):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        UPDATE indicateur
        SET libelle = ?, type_indicateur = ?, id_domaine = ?
        WHERE id_indicateur = ?
    ''', (libelle, type_indicateur, id_domaine, id_indicateur))

    conn.commit()
    conn.close()


def modifier_domaine(id_domaine, titre_domaine):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        UPDATE domaine
        SET titre_domaine = ?
        WHERE id_domaine = ?
    ''', (titre_domaine, id_domaine))

    conn.commit()
    conn.close()


def modifier_region(id_region, nom_region, nom_departement, nom_sous_prefecture):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        UPDATE region
        SET nom_region = ?, nom_departement = ?, nom_sous_prefecture = ?
        WHERE id_region = ?
    ''', (nom_region, nom_departement, nom_sous_prefecture, id_region))

    conn.commit()
    conn.close()


def modifier_reponse(id_reponse, valeur_reponse, date_donnee, nom_agent_collecte, id_indicateur, id_region):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        UPDATE reponse
        SET valeur_reponse = ?, date_donnee = ?, nom_agent_collecte = ?, id_indicateur = ?, id_region = ?
        WHERE id_reponse = ?
    ''', (valeur_reponse, date_donnee, nom_agent_collecte, id_indicateur, id_region, id_reponse))

    conn.commit()
    conn.close()

