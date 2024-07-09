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
    formulaire_reponse()
    st.subheader("Importer la liste des indicateurs")
    upload_file_excel_indicateur()
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


"""
Ensemble des elements de la pade 1
"""

def process_excel_file_indicateur(df):
    for index, row in df.iterrows():
        data.enregistrer_indicateur(
            row['id_indicateur'],
            row['indicateur'],
            row['type_indicateur'],
            row['id_domaine']

        )

def upload_file_excel_indicateur():
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


# Function to process the Excel file and save data
def process_excel_file_reponse(df):
    expected_columns = ["code localité", "code indicateur", "année de collecte", "valeur globale",
                                "valeur masculine", "valeur feminine", "valeur urbaine", "valeur rurale",
                                "matricule agent"]
    # Normalize the column names to avoid issues with spaces or hidden characters
    df.columns = [col.strip().lower() for col in df.columns]
    normalized_expected_columns = [col.strip().lower() for col in expected_columns]

    # Create a mapping of expected column names to actual column names in the DataFrame
    column_mapping = {}
    for expected_col in normalized_expected_columns:
        for actual_col in df.columns:
            if expected_col == actual_col:
                column_mapping[expected_col] = actual_col

    # Check if all expected columns are present in the DataFrame
    if all(col in column_mapping for col in normalized_expected_columns):
        for index, row in df.iterrows():
            data.enregistrer_reponse(
                row[column_mapping['code localité']],
                row[column_mapping['code indicateur']],
                row[column_mapping['année de collecte']],
                row[column_mapping['valeur globale']],
                row[column_mapping['valeur masculine']],
                row[column_mapping['valeur feminine']],
                row[column_mapping['valeur urbaine']],
                row[column_mapping['valeur rurale']],
                row[column_mapping['matricule agent']]
            )
    else:
        missing_columns = [col for col in normalized_expected_columns if col not in column_mapping]
        raise ValueError(f"Les colonnes suivantes sont manquantes dans le fichier : {', '.join(missing_columns)}")


def formulaire_reponse():
    st.header("Gestion des données")

    st.subheader("Importer les données du questionnaire")
    uploaded_file = st.file_uploader("Choisir un fichier Excel", type="xlsx")

    if uploaded_file is not None:
        try:
            # Load the Excel file
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            sheet_name = st.selectbox("Choisir la feuille", sheet_names)
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

            # Display the dataframe
            st.dataframe(df)

            # Define the expected columns
            expected_columns = ["code localité", "code indicateur", "année de collecte", "valeur globale",
                                "valeur masculine", "valeur feminine", "valeur urbaine", "valeur rurale",
                                "matricule agent"]

            # Normalize column names to avoid issues with spaces or hidden characters
            df.columns = [col.strip().lower() for col in df.columns]
            normalized_expected_columns = [col.strip().lower() for col in expected_columns]

            # Check if the expected columns are present in the dataframe
            if all(col in df.columns for col in normalized_expected_columns):
                if st.button("Enregistrer dans la base de données"):
                    try:
                        process_excel_file_reponse(df)
                        st.success("Données enregistrées avec succès !")
                    except Exception as e:
                        st.error(f"Erreur lors de l'enregistrement: {e}")
            else:
                missing_columns = [col for col in normalized_expected_columns if col not in df.columns]
                st.warning(
                    f"Les colonnes attendues ne correspondent pas. Colonnes manquantes : {', '.join(missing_columns)}")
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier: {e}")

    # Form for modifying an existing entry
    if st.checkbox("Modifier une réponse",key="page1_mod_repon"):
        df=data.obtenir_base_donne()
        st.write(df)
        formulaire_modifier_une_reponse()

    return


def formulaire_modifier_une_reponse():
    st.header("Modifier une Réponse")
    id_reponse = st.number_input("ID Réponse", min_value=1, step=1)
    code_localite = st.text_input("Code Localité")
    f_code_indicateur = st.text_input("Code Indicateur")
    annee_collecte = st.text_input("Année de Collecte")
    valeur_globale = st.text_input("Valeur Globale")
    valeur_masculine = st.text_input("Valeur Masculine")
    valeur_feminine = st.text_input("Valeur Féminine")
    valeur_urbaine = st.text_input("Valeur Urbaine")
    valeur_rurale = st.text_input("Valeur Rurale")
    f_matricule_agent = st.text_input("Matricule Agent")

    if st.button("Modifier"):
        try:
            data.modifier_reponse(id_reponse, code_localite, f_code_indicateur, annee_collecte, valeur_globale,
                                  valeur_masculine, valeur_feminine, valeur_urbaine, valeur_rurale, f_matricule_agent)
            st.success("Réponse modifiée avec succès")
        except Exception as e:
            st.error(f"Erreur lors de la modification: {e}")


"""
Fin du bloc page 1
"""


