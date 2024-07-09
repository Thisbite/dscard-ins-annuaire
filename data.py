import sqlite3
import  pandas as pd

conn = sqlite3.connect('database.db')
c = conn.cursor()

#c.execute("DROP TABLE reponse")

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
              code_region PRIMARY KEY,
                 nom_region

          )
    ''')

    c.execute('''
             CREATE TABLE IF NOT EXISTS departement (
                 code_departement  TEXT PRIMARY KEY,
                    nom_departement TEXT,
                    f_code_region TEXT,
                    FOREIGN KEY (f_code_region) REFERENCES region(code_region)

             )
       ''')
    c.execute('''
             CREATE TABLE IF NOT EXISTS sous_prefecture(
                 code_sous_prefecture  TEXT PRIMARY KEY,
                    nom_sous_prefecture TEXT,
                    f_code_departement TEXT,
                    FOREIGN KEY (f_code_departement) REFERENCES departement(code_departement)

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
            code_localite TEXT,
            f_code_indicateur TEXT,
            annee_collecte TEXT,
            valeur_globale TEXT,
            valeur_masculine TEXT,
            valeur_feminine TEXT,
            valeur_urbaine TEXT,
            valeur_rurale TEXT,
            f_matricule_agent TEXT,         
            FOREIGN KEY(f_code_indicateur) REFERENCES indicateur(id_indicateur)
            FOREIGN KEY (f_matricule_agent) REFERENCES agent_collecte(matricule)

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

def enregistrer_region(code_region, nom_region):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO region (code_region, nom_region)
        VALUES (?, ?)
    ''', (code_region, nom_region))
    conn.commit()
    conn.close()
def modifier_region(code_region, nom_region):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        UPDATE region
        SET nom_region = ?
        WHERE code_region = ?
    ''', (nom_region, code_region))
    conn.commit()
    conn.close()


def enregistrer_departement(code_departement, nom_departement, f_code_region):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO departement (code_departement, nom_departement, f_code_region)
        VALUES (?, ?, ?)
    ''', (code_departement, nom_departement, f_code_region))
    conn.commit()
    conn.close()

def modifier_departement(code_departement, nom_departement, f_code_region):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        UPDATE departement
        SET nom_departement = ?, f_code_region = ?
        WHERE code_departement = ?
    ''', (nom_departement, f_code_region, code_departement))
    conn.commit()
    conn.close()

def enregistrer_sous_prefecture(code_sous_prefecture, nom_sous_prefecture, f_code_departement):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO sous_prefecture (code_sous_prefecture, nom_sous_prefecture, f_code_departement)
        VALUES (?, ?, ?)
    ''', (code_sous_prefecture, nom_sous_prefecture, f_code_departement))
    conn.commit()
    conn.close()

def modifier_sous_prefecture(code_sous_prefecture, nom_sous_prefecture, f_code_departement):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        UPDATE sous_prefecture
        SET nom_sous_prefecture = ?, f_code_departement = ?
        WHERE code_sous_prefecture = ?
    ''', (nom_sous_prefecture, f_code_departement, code_sous_prefecture))
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
def enregistrer_reponse(code_localite, f_code_indicateur, annee_collecte, valeur_globale, valeur_masculine, valeur_feminine, valeur_urbaine, valeur_rurale, f_matricule_agent):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO reponse (
            code_localite, 
            f_code_indicateur, 
            annee_collecte, 
            valeur_globale, 
            valeur_masculine, 
            valeur_feminine, 
            valeur_urbaine, 
            valeur_rurale, 
            f_matricule_agent
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (code_localite, f_code_indicateur, annee_collecte, valeur_globale, valeur_masculine, valeur_feminine, valeur_urbaine, valeur_rurale, f_matricule_agent))
    conn.commit()
    conn.close()


def modifier_reponse(id_reponse, code_localite, f_code_indicateur, annee_collecte, valeur_globale, valeur_masculine, valeur_feminine, valeur_urbaine, valeur_rurale, f_matricule_agent):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        UPDATE reponse
        SET 
            code_localite = ?, 
            f_code_indicateur = ?, 
            annee_collecte = ?, 
            valeur_globale = ?, 
            valeur_masculine = ?, 
            valeur_feminine = ?, 
            valeur_urbaine = ?, 
            valeur_rurale = ?, 
            f_matricule_agent = ?
        WHERE 
            id_reponse = ?
    ''', (code_localite, f_code_indicateur, annee_collecte, valeur_globale, valeur_masculine, valeur_feminine, valeur_urbaine, valeur_rurale, f_matricule_agent, id_reponse))
    conn.commit()
    conn.close()


def obtenir_reponse():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM reponse')
    df=c.fetchall()
    df=pd.DataFrame(df)
    conn.commit()
    conn.close()
    return df

def obtenir_base_donne():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(
        '''
        SELECT 
            reg.nom_region,
            d.nom_departement,
            sp.nom_sous_prefecture,
            i.indicateur,
            r.annee_collecte,
            r.valeur_globale,
            r.valeur_masculine,
            r.valeur_feminine,
            r.valeur_urbaine,
            r.valeur_rurale
        FROM reponse r
        LEFT JOIN indicateur i ON r.f_code_indicateur = i.id_indicateur
        LEFT JOIN sous_prefecture sp ON r.code_localite = sp.code_sous_prefecture
        LEFT JOIN departement d ON 
            r.code_localite = d.code_departement OR
            sp.f_code_departement = d.code_departement
        LEFT JOIN region reg ON 
            r.code_localite = reg.code_region OR
            d.f_code_region = reg.code_region OR
            sp.f_code_departement = d.code_departement AND d.f_code_region = reg.code_region
        '''
    )
    df = c.fetchall()
    df = pd.DataFrame(df, columns=["Région", "Département", "Sous-préfecture", "Indicateur", "Année",
                                   "Valeur globale", "Valeur masculine", "Valeur féminine", "Valeur urbaine",
                                   "Valeur rurale"])
    conn.commit()
    conn.close()
    return df



create_tables()
#enregistrer_agent_collecte("Deom","demo@demo.com","demo123","0809090")

#enregistrer_sous_prefecture('SP001', 'Sous-Préfecture A', 'D001')
#enregistrer_sous_prefecture('SP002', 'Sous-Préfecture B', 'D002')
#enregistrer_sous_prefecture('SP003', 'Sous-Préfecture C', 'D003')
#enregistrer_departement('D001', 'Département A', 'R001')
#enregistrer_departement('D002', 'Département B', 'R002')
#enregistrer_departement('D003', 'Département C', 'R003')
#enregistrer_region('R001', 'Région A')
#enregistrer_region('R002', 'Région B')
#enregistrer_region('R003', 'Région C')
