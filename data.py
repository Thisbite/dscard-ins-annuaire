import sqlite3
import  pandas as pd

conn = sqlite3.connect('database.db')
c = conn.cursor()
#c.execute("DROP TABLE indicateur")
def create_tables():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS agent_collecte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_prenoms TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            matricule TEXT UNIQUE NOT NULL,
            numero TEXT NOT NULL
        )
    ''')

    c.execute('''
           CREATE TABLE IF NOT EXISTS equipe_technique (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nom_prenoms TEXT NOT NULL,
               email TEXT UNIQUE NOT NULL,
               matricule TEXT UNIQUE NOT NULL,
               numero TEXT NOT NULL
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
              id  INTEGER PRIMARY KEY AUTOINCREMENT,
              id_region INTEGER,
              nom_region TEXT NOT NULL,
              nom_departement TEXT NOT NULL,
              nom_sous_prefecture TEXT NOT NULL
          )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS indicateur (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_indicateur INTEGER,
            indicateur TEXT NOT NULL,
            type_indicateur TEXT NOT NULL,
            id_domaine INTEGER,
            FOREIGN KEY (id_domaine) REFERENCES domaine(id_domaine)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS domaine (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_domaine INTEGER NOT NULL,
            titre_domaine TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS reponse (
            id_reponse INTEGER PRIMARY KEY AUTOINCREMENT,
            valeur_reponse TEXT,
            date_collecte TEXT,
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

# Function to record agent_collecte entries
def enregistrer_agent_collecte(nom_prenoms, email, matricule, numero):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO agent_collecte (nom_prenoms, email, matricule, numero)
        VALUES (?, ?, ?, ?)
    ''', (nom_prenoms, email, matricule, numero))
    conn.commit()
    conn.close()

# Function to modify agent_collecte entries
def modifier_agent_collecte(id, nom_prenoms, email, matricule, numero):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        UPDATE agent_collecte
        SET nom_prenoms = ?, email = ?, matricule = ?, numero = ?
        WHERE id = ?
    ''', (nom_prenoms, email, matricule, numero, id))
    conn.commit()
    conn.close()

# Function to record equipe_technique entries
def enregistrer_equipe_technique(nom_prenoms, email, matricule, numero):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO equipe_technique (nom_prenoms, email, matricule, numero)
        VALUES (?, ?, ?, ?)
    ''', (nom_prenoms, email, matricule, numero))
    conn.commit()
    conn.close()

# Function to modify equipe_technique entries
def modifier_equipe_technique(id, nom_prenoms, email, matricule, numero):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        UPDATE equipe_technique
        SET nom_prenoms = ?, email = ?, matricule = ?, numero = ?
        WHERE id = ?
    ''', (nom_prenoms, email, matricule, numero, id))
    conn.commit()
    conn.close()

# Function to record directeur entries
def enregistrer_directeur(nom_prenoms, email, matricule_dr, numero):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO directeur (nom_prenoms, email, matricule_dr, numero)
        VALUES (?, ?, ?, ?)
    ''', (nom_prenoms, email, matricule_dr, numero))
    conn.commit()
    conn.close()

# Function to modify directeur entries
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

# Function to record direction_regionale entries
def enregistrer_direction_regionale(nom_direction, region, matricule_agent, matricule_dr):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO direction_regionale (nom_direction, region, matricule_agent, matricule_dr)
        VALUES (?, ?, ?, ?)
    ''', (nom_direction, region, matricule_agent, matricule_dr))
    conn.commit()
    conn.close()

# Function to modify direction_regionale entries
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

# Function to record region entries
def enregistrer_region(id_region, nom_region, nom_departement, nom_sous_prefecture):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO region (id_region, nom_region, nom_departement, nom_sous_prefecture)
        VALUES (?, ?, ?, ?)
    ''', (id_region, nom_region, nom_departement, nom_sous_prefecture))
    conn.commit()
    conn.close()

# Function to modify region entries
def modifier_region(id, id_region, nom_region, nom_departement, nom_sous_prefecture):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        UPDATE region
        SET id_region = ?, nom_region = ?, nom_departement = ?, nom_sous_prefecture = ?
        WHERE id = ?
    ''', (id_region, nom_region, nom_departement, nom_sous_prefecture, id))
    conn.commit()
    conn.close()



# Function to record indicateur entries




def enregistrer_indicateur(id_indicateur, indicateur, type_indicateur, id_domaine):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO indicateur (id_indicateur, indicateur, type_indicateur, id_domaine)
        VALUES (?, ?, ?, ?)
    ''', (id_indicateur, indicateur, type_indicateur, id_domaine))
    conn.commit()
    conn.close()

# Function to modify indicateur entries
def modifier_indicateur(id, id_indicateur, indicateur, type_indicateur, id_domaine):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        UPDATE indicateur
        SET id_indicateur = ?, indicateur = ?, type_indicateur = ?, id_domaine = ?
        WHERE id = ?
    ''', (id_indicateur, indicateur, type_indicateur, id_domaine, id))
    conn.commit()
    conn.close()



def supprimer_doublons_indicateur():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    try:
        # Select unique rows based on specific columns and store them in a temporary table
        cursor.execute('''
            CREATE TEMPORARY TABLE indicateur_temp AS
            SELECT MIN(id) as id, id_indicateur, indicateur, type_indicateur, id_domaine
            FROM indicateur
            GROUP BY id_indicateur, indicateur, type_indicateur, id_domaine
        ''')

        # Delete all rows from the original table
        cursor.execute('DELETE FROM indicateur')

        # Re-insert unique rows back into the original table
        cursor.execute('''
            INSERT INTO indicateur (id, id_indicateur, indicateur, type_indicateur, id_domaine)
            SELECT id, id_indicateur, indicateur, type_indicateur, id_domaine
            FROM indicateur_temp
        ''')

        # Drop the temporary table
        cursor.execute('DROP TABLE indicateur_temp')

        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()



def obtenir_indicateur():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT
                        id,
                        id_domaine,
                        id_indicateur,
                        indicateur,
                        type_indicateur

                    FROM indicateur''')
    data=cursor.fetchall()
    df=pd.DataFrame(data,columns=["ID","ID domaine","ID indicateur","Indicateur","Type indicateur"])
    return df






# Function to record domaine entries
def enregistrer_domaine(id_domaine, titre_domaine):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO domaine (id_domaine, titre_domaine)
        VALUES (?, ?)
    ''', (id_domaine, titre_domaine))
    conn.commit()
    conn.close()

# Function to modify domaine entries
def modifier_domaine(id, id_domaine, titre_domaine):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        UPDATE domaine
        SET id_domaine = ?, titre_domaine = ?
        WHERE id = ?
    ''', (id_domaine, titre_domaine, id))
    conn.commit()
    conn.close()

# Function to record reponse entries
def enregistrer_reponse(valeur_reponse, date_collecte, matricule_agent, id_indicateur, id_region):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO reponse (valeur_reponse, date_collecte, matricule_agent, id_indicateur, id_region)
        VALUES (?, ?, ?, ?, ?)
    ''', (valeur_reponse, date_collecte, matricule_agent, id_indicateur, id_region))
    conn.commit()
    conn.close()

# Function to modify reponse entries
def modifier_reponse(id_reponse, valeur_reponse, date_collecte, matricule_agent, id_indicateur, id_region):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        UPDATE reponse
        SET valeur_reponse = ?, date_collecte = ?, matricule_agent = ?, id_indicateur = ?, id_region = ?
        WHERE id_reponse = ?
    ''', (valeur_reponse, date_collecte, matricule_agent, id_indicateur, id_region, id_reponse))
    conn.commit()
    conn.close()

# Call to create tables
create_tables()
#enregistrer_agent_collecte("Deom","demo@demo.com","demo123","0809090")