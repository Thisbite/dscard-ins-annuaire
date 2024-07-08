import sqlite3
import streamlit as st

import data


# Connexion à la base de données
def connect_db():
    conn = sqlite3.connect('database.db')
    return conn


# Authentification de l'utilisateur
def authenticate(email, matricule):
    conn = connect_db()
    c = conn.cursor()

    c.execute('SELECT * FROM agent_collecte WHERE email = ? AND matricule = ?', (email, matricule))
    agent = c.fetchone()

    c.execute('SELECT * FROM directeur WHERE email = ? AND matricule_dr = ?', (email, matricule))
    directeur = c.fetchone()

    direction_regionale = None
    if directeur:
        c.execute('SELECT * FROM direction_regionale WHERE matricule_dr = ?', (matricule,))
        direction_regionale = c.fetchone()

    c.execute('SELECT * FROM equipe_technique WHERE email = ? AND matricule = ?', (email, matricule))
    tech = c.fetchone()

    conn.close()

    if agent:
        return "agent_collecte", agent, None
    elif directeur:
        return "directeur", directeur, direction_regionale
    elif tech:
        return "equipe_technique", tech, None
    else:
        return None, None, None
# Fonction pour afficher la page 1
def page1():
    st.title("Page 1")
    st.write("Bienvenue sur la Page 1")


# Fonction pour afficher la page 2
def page2(user, direction_regionale):
    st.title("Page 2")
    st.write(f"Bienvenue sur la Page 2, {user[1]}")


    df = data.statistique()
    st.write("Afficher les jeux de données")

    st.dataframe(df)
    #st.write(f"Filtré par direction: {direction_regionale[1]}")



# Fonction pour afficher la page 3
def page3():
    st.title("Page 3")
    st.write("Bienvenue sur la Page 3")



# Fonction pour afficher la page 4
def page4():
    st.title("Page 4")
    st.write("Bienvenue sur la Page 4")

