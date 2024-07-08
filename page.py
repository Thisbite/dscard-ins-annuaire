import sqlite3
import streamlit as st
import pandas as pd
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
    st.title("Saisie ou importation des données")
    st.write("Bienvenue sur la page d'importation")
    upload_file_excel_indicateur()
    df=data.obtenir_indicateur()
    if 'show_data' not in st.session_state:
        st.session_state['show_data'] = False

    if st.button("Afficher/Cacher les données"):
        st.session_state['show_data'] = not st.session_state['show_data']
        if st.session_state['show_data']:
            data.supprimer_doublons_indicateur()
        if st.session_state['show_data']:
            df=data.obtenir_indicateur()
            st.dataframe(df)


# Fonction pour afficher la page 2
def page2(user, direction_regionale):
    st.title("Page 2")
    st.write(f"Bienvenue sur la Page 2, {user[1]}")
    st.write("Afficher les jeux de données")


    #st.write(f"Filtré par direction: {direction_regionale[1]}")



# Fonction pour afficher la page 3
def page3():
    st.title("Page 3")
    st.write("Bienvenue sur la Page 3")



# Fonction pour afficher la page 4
def page4():
    st.title("Page 4")
    st.write("Bienvenue sur la Page 4")




def process_excel_file_indicateur(df):
    for index, row in df.iterrows():
        data.enregistrer_indicateur(
            row['id_indicateur'],
            row['indicateur'],
            row['type_indicateur'],
            row['id_domaine']

        )

def upload_file_excel_indicateur():
    st.write("Charger la liste des indicateurs")

    uploaded_file = st.file_uploader("Choisir la feuille Excel", type="xlsx", key="indfile1212")

    if uploaded_file is not None:
        try:
            # Load the Excel file
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            sheet_name = st.selectbox("Choisir la feuille", sheet_names, key="indica2")
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

            # Display the dataframe
            st.dataframe(df)

            # Define the expected columns
            expected_columns = ["indicateur","id_indicateur", "id_domaine", "type_indicateur" ]

            # Check if the expected columns are present in the dataframe
            missing_columns = [column for column in expected_columns if column not in df.columns]

            if not missing_columns:
                if st.button("Enregistrer", key="indicateur_b12"):
                    try:
                        process_excel_file_indicateur(df)
                        st.success("Enregistrement avec succès !")
                    except Exception as e:
                        st.error(f"Une erreur d'enregsitrement: {e}")
            else:
                st.warning(f"Les colonnes suivantes sont manquantes : {', '.join(missing_columns)}")

        except Exception as e:
            st.error(f"Erreur avec le fichier Excel: {e}")
    return