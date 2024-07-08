import sqlite3

import pandas as pd


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
           CREATE TABLE IF NOT EXISTS equipe_technique (
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
            matricule_agent TEXT,
            matricule_dr TEXT,
            FOREIGN KEY (matricule_agent) REFERENCES agent_collecte(matricule),
            FOREIGN KEY (matricule_dr) REFERENCES directeur(matricule_dr)
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
        CREATE TABLE IF NOT EXISTS reponse (
            id_reponse INTEGER PRIMARY KEY AUTOINCREMENT,
            valeur_reponse TEXT,
            date_donnee TEXT,
            matricule_agent TEXT NOT NULL,
            id_indicateur INTEGER,
            id_region INTEGER,
            FOREIGN KEY (id_indicateur) REFERENCES indicateur(id_indicateur),
            FOREIGN KEY (id_region) REFERENCES region(id_region),
            FOREIGN KEY (matricule_agent) REFERENCES agent_collecte(matricule)
        )
    ''')

    conn.commit()
    conn.close()

# Appel de la fonction pour créer les tables
create_tables()


def statistique():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    query = '''
    SELECT 
        r.nom_region,
        r.nom_departement,
        r.nom_sous_prefecture,
        d.titre_domaine,
        i.libelle,
        re.valeur_reponse,
        re.date_donnee,
        a.nom_prenoms
    FROM 
        region r
    JOIN 
        reponse re ON r.id_region = re.id_region
    JOIN 
        indicateur i ON i.id_indicateur = re.id_indicateur
    JOIN 
        domaine d ON i.id_domaine = d.id_domaine
    JOIN 
        agent_collecte a ON re.matricule_agent = a.matricule
    '''

    c.execute(query)
    data = c.fetchall()

    df = pd.DataFrame(data,
                      columns=["Région", "Département", "Sous-préfecture", "Domaine", "Indicateur", "Valeur indicateur",
                               "Année de collecte", "Nom de l'agent"])

    conn.close()
    return df


### ********************************************************************* Enregistrer
def enregistrer_agent_collecte(nom_prenoms, email, matricule, numero, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO agent_collecte (nom_prenoms, email, matricule, numero, password)
        VALUES (?, ?, ?, ?, ?)
    ''', (nom_prenoms, email, matricule, numero, password))

    conn.commit()
    conn.close()

def enregistrer_equipe_technique(nom_prenoms, email, matricule, numero, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO equipe_technique (nom_prenoms, email, matricule, numero, password)
        VALUES (?, ?, ?, ?, ?)
    ''', (nom_prenoms, email, matricule, numero, password))

    conn.commit()
    conn.close()

def enregistrer_directeur(nom_prenoms, email, matricule_dr, numero):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO directeur (nom_prenoms, email, matricule_dr, numero)
        VALUES (?, ?, ?, ?)
    ''', (nom_prenoms, email, matricule_dr, numero))

    conn.commit()
    conn.close()

def enregistrer_direction_regionale(nom_direction, region, matricule_agent, matricule_dr):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO direction_regionale (nom_direction, region, matricule_agent, matricule_dr)
        VALUES (?, ?, ?, ?)
    ''', (nom_direction, region, matricule_agent, matricule_dr))

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

def enregistrer_reponse(valeur_reponse, date_donnee, matricule_agent, id_indicateur, id_region):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO reponse (valeur_reponse, date_donnee, matricule_agent, id_indicateur, id_region)
        VALUES (?, ?, ?, ?, ?)
    ''', (valeur_reponse, date_donnee, matricule_agent, id_indicateur, id_region))

    conn.commit()
    conn.close()

###**************************************************Modifier
def modifier_agent_collecte(id, nom_prenoms, email, matricule, numero, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        UPDATE agent_collecte
        SET nom_prenoms = ?, email = ?, matricule = ?, numero = ?, password = ?
        WHERE id = ?
    ''', (nom_prenoms, email, matricule, numero, password, id))

    conn.commit()
    conn.close()

def modifier_equipe_technique(id, nom_prenoms, email, matricule, numero, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        UPDATE agent_collecte
        SET nom_prenoms = ?, email = ?, matricule = ?, numero = ?, password = ?
        WHERE id = ?
    ''', (nom_prenoms, email, matricule, numero, password, id))

    conn.commit()
    conn.close()

def modifier_directeur(id, nom_prenoms, email, matricule_dr, numero):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        UPDATE directeur
        SET nom_prenoms = ?, email = ?, matricule_dr = ?, numero = ?
        WHERE id = ?
    ''', (nom_prenoms, email, matricule_dr, numero, id))

    conn.commit()
    conn.close()

def modifier_direction_regionale(id, nom_direction, region, matricule_agent, matricule_dr):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        UPDATE direction_regionale
        SET nom_direction = ?, region = ?, matricule_agent = ?, matricule_dr = ?
        WHERE id = ?
    ''', (nom_direction, region, matricule_agent, matricule_dr, id))

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

def modifier_reponse(id_reponse, valeur_reponse, date_donnee, matricule_agent, id_indicateur, id_region):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        UPDATE reponse
        SET valeur_reponse = ?, date_donnee = ?, matricule_agent = ?, id_indicateur = ?, id_region = ?
        WHERE id_reponse = ?
    ''', (valeur_reponse, date_donnee, matricule_agent, id_indicateur, id_region, id_reponse))

    conn.commit()
    conn.close()

"""
# Enregistre trois agents de collecte
enregistrer_agent_collecte("AJohnn Doe", "john@example.com", "AAAG001", "1234567890", "password123")
enregistrer_agent_collecte("AJane M Smith", "jane@example.com", "AAAG002", "0987654321", "password456")
enregistrer_agent_collecte("AEmily Davis", "emily@example.com", "AAAG003", "1122334455", "password789")

# Enregistre trois membres de l'équipe technique
enregistrer_equipe_technique("Michael Brown", "michael@example.com", "ET001", "2233445566", "techpass123")
enregistrer_equipe_technique("Sarah Johnson", "sarah@example.com", "ET002", "3344556677", "techpass456")
enregistrer_equipe_technique("David Wilson", "david@example.com", "ET003", "4455667788", "techpass789")

# Enregistre trois directeurs
enregistrer_directeur("Alice Cooper", "alice@example.com", "DR001", "5566778899")
enregistrer_directeur("Bob Marley", "bob@example.com", "DR002", "6677889900")
enregistrer_directeur("Charlie Parker", "charlie@example.com", "DR003", "7788990011")

# Enregistre trois directions régionales
enregistrer_direction_regionale("Direction Nord", "Nord", "AG001", "DR001")
enregistrer_direction_regionale("Direction Sud", "Sud", "AG002", "DR002")
enregistrer_direction_regionale("Direction Est", "Est", "AG003", "DR003")

# Enregistre trois indicateurs
enregistrer_indicateur("Nombre de classe", "Type 1", 1)
enregistrer_indicateur("Nombre de lit", "Type 2", 2)
enregistrer_indicateur("Nombre de cas", "Type 3", 3)

# Enregistre trois domaines
enregistrer_domaine("Education ")
enregistrer_domaine("Santé ")
enregistrer_domaine("Transport")

# Enregistre trois régions
enregistrer_region("Poro", "Korhogo", "Kanoroba")
enregistrer_region("Poro", "M'Bengué", "Katiali")
enregistrer_region("Poro", "Sinematiali", "Bahouakaha")

# Enregistre trois réponses
enregistrer_reponse("Valeur 1", "2023-07-01", "AAG001", 1, 1)
enregistrer_reponse("Valeur 2", "2023-07-02", "AAG002", 2, 2)
enregistrer_reponse("Valeur 3", "2023-07-03", "AAG003", 3, 3)
"""