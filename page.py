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
    st.write("************************************")


# Fonction pour afficher la page 2
def page2(user, direction_regionale):
    st.title("Page 2")
    st.write(f"Bienvenue sur la Page 2, {user[1]}")
    st.write("Afficher les jeux de données")


    #st.write(f"Filtré par direction: {direction_regionale[1]}")



# Fonction pour afficher la page 3
def page3():
    st.title("Paramètre de l'application")
    st.write("************************************************")
    formulaire_agent_collecte()
    st.write("************************************************")
    formulaire_equipe_technique()
    st.write("************************************************")
    formulaire_directeur()
    st.write("************************************************")
    formulaire_region()
    st.write("************************************************")
    formulaire_departement()
    st.write("************************************************")
    formulaire_sous_prefecture()
    st.write("************************************************")
    formulaire_indicateur()
    st.write("************************************************")
    formulaire_domaine()
    st.write("************************************************")




# Fonction pour afficher la page 4
def page4():
    st.subheader("Importer la liste des indicateurs")
    upload_file_excel_indicateur()
    if 'show_data' not in st.session_state:
        st.session_state['show_data'] = False
    if st.button("Afficher/Cacher les données"):
        st.session_state['show_data'] = not st.session_state['show_data']
        if st.session_state['show_data']:
            data.supprimer_doublons_indicateur()
        if st.session_state['show_data']:
            df = data.obtenir_indicateur()
            st.dataframe(df)
    st.subheader("Exportation de la base de données")
    df = data.obtenir_base_donne()
    st.write(df)



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






"""
Les données de page de configuration
"""


def formulaire_agent_collecte():
    st.header("Gestion des Agents de Collecte")

    # Formulaire de saisie
    st.subheader("Ajouter un nouvel agent de collecte")
    with st.form(key='add_agent_collecte'):
        nom_prenoms = st.text_input("Nom et Prénoms")
        email = st.text_input("Email")
        matricule = st.text_input("Matricule")
        numero = st.text_input("Numéro de téléphone")
        submit_button = st.form_submit_button(label="Enregistrer")

    if submit_button:
        data.enregistrer_agent_collecte(nom_prenoms, email, matricule, numero)
        st.success("Agent de collecte enregistré avec succès")

    # Formulaire de modification
    st.subheader("Modifier un agent de collecte existant")
    agent_id = st.number_input("ID de l'agent à modifier", min_value=1, step=1)
    with st.form(key='modify_agent_collecte'):
        nom_prenoms = st.text_input("Nom et Prénoms", key='modify_nom_prenoms')
        email = st.text_input("Email", key='modify_email')
        matricule = st.text_input("Matricule", key='modify_matricule')
        numero = st.text_input("Numéro de téléphone", key='modify_numero')
        modify_button = st.form_submit_button("Modifier")

    if modify_button:
        data.modifier_agent_collecte(agent_id, nom_prenoms, email, matricule, numero)
        st.success("Agent de collecte modifié avec succès")

    # Chargement de données par fichier Excel
    st.subheader("Importer des agents de collecte depuis un fichier Excel")
    uploaded_file = st.file_uploader("Choisir un fichier Excel", type="xlsx", key="agent_collecte_file")

    if uploaded_file is not None:
        try:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            sheet_name = st.selectbox("Choisir la feuille", sheet_names)
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

            st.dataframe(df)

            expected_columns = ["nom_prenoms", "email", "matricule", "numero"]
            if all(column in df.columns for column in expected_columns):
                if st.button("Enregistrer dans la base de données"):
                    try:
                        for index, row in df.iterrows():
                            data.enregistrer_agent_collecte(row['nom_prenoms'], row['email'], row['matricule'],
                                                       row['numero'])
                        st.success("Données enregistrées avec succès !")
                    except Exception as e:
                        st.error(f"Erreur lors de l'enregistrement: {e}")
            else:
                st.warning("Les colonnes attendues ne correspondent pas")
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier: {e}")



def formulaire_equipe_technique():
    st.header("Gestion de l'Équipe Technique")

    # Formulaire de saisie
    st.subheader("Ajouter un nouveau membre de l'équipe technique")
    with st.form(key='add_equipe_technique'):
        nom_prenoms = st.text_input("Nom et Prénoms")
        email = st.text_input("Email")
        matricule = st.text_input("Matricule")
        numero = st.text_input("Numéro de téléphone")
        submit_button = st.form_submit_button("Enregistrer")

    if submit_button:
        data.enregistrer_equipe_technique(nom_prenoms, email, matricule, numero)
        st.success("Membre de l'équipe technique enregistré avec succès")

    # Formulaire de modification
    st.subheader("Modifier un membre de l'équipe technique existant")
    equipe_id = st.number_input("ID du membre à modifier", min_value=1, step=1)
    with st.form(key='modify_equipe_technique'):
        nom_prenoms = st.text_input("Nom et Prénoms", key='modify_nom_prenoms12')
        email = st.text_input("Email", key='modify_emaila2')
        matricule = st.text_input("Matricule", key='modify_matricule')
        numero = st.text_input("Numéro de téléphone", key='modify_numero')
        modify_button = st.form_submit_button("Modifier",key="modi_equi_t1")

    if modify_button:
        data.modifier_equipe_technique(equipe_id, nom_prenoms, email, matricule, numero)
        st.success("Membre de l'équipe technique modifié avec succès")

    # Chargement de données par fichier Excel
    st.subheader("Importer des membres de l'équipe technique depuis un fichier Excel")
    uploaded_file = st.file_uploader("Choisir un fichier Excel", type="xlsx", key="equipe_technique_file")

    if uploaded_file is not None:
        try:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            sheet_name = st.selectbox("Choisir la feuille", sheet_names)
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

            st.dataframe(df)

            expected_columns = ["nom_prenoms", "email", "matricule", "numero"]
            if all(column in df.columns for column in expected_columns):
                if st.button("Enregistrer dans la base de données"):
                    try:
                        for index, row in df.iterrows():
                            data.enregistrer_equipe_technique(row['nom_prenoms'], row['email'], row['matricule'],
                                                         row['numero'])
                        st.success("Données enregistrées avec succès !")
                    except Exception as e:
                        st.error(f"Erreur lors de l'enregistrement: {e}")
            else:
                st.warning("Les colonnes attendues ne correspondent pas")
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier: {e}")


def formulaire_directeur():
    st.header("Gestion des Directeurs")

    # Formulaire de saisie
    st.subheader("Ajouter un nouveau directeur")
    with st.form(key='add_directeur'):
        nom_prenoms = st.text_input("Nom et Prénoms")
        email = st.text_input("Email")
        matricule_dr = st.text_input("Matricule")
        numero = st.text_input("Numéro de téléphone")
        submit_button = st.form_submit_button(label="Enregistrer")

        if submit_button:
            data.enregistrer_directeur(nom_prenoms, email, matricule_dr, numero)
            st.success("Directeur enregistré avec succès")

    # Formulaire de modification
    st.subheader("Modifier un directeur existant")
    directeur_id = st.number_input("ID du directeur à modifier", min_value=1, step=1)
    with st.form(key='modify_directeur'):
        nom_prenoms = st.text_input("Nom et Prénoms", key='modify_nom_prenoms')
        email = st.text_input("Email", key='modify_email')
        matricule_dr = st.text_input("Matricule", key='modify_matricule')
        numero = st.text_input("Numéro de téléphone", key='modify_numero')
        modify_button = st.form_submit_button(label="Modifier")

        if modify_button:
            data.modifier_directeur(directeur_id, nom_prenoms, email, matricule_dr, numero)
            st.success("Directeur modifié avec succès")

    # Chargement de données par fichier Excel
    st.subheader("Importer des directeurs depuis un fichier Excel")
    uploaded_file = st.file_uploader("Choisir un fichier Excel", type="xlsx", key="directeur_file")

    if uploaded_file is not None:
        try:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            sheet_name = st.selectbox("Choisir la feuille", sheet_names)
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

            st.dataframe(df)

            expected_columns = ["nom_prenoms", "email", "matricule_dr", "numero"]
            if all(column in df.columns for column in expected_columns):
                if st.button("Enregistrer dans la base de données"):
                    try:
                        for index, row in df.iterrows():
                            data.enregistrer_directeur(row['nom_prenoms'], row['email'], row['matricule_dr'], row['numero'])
                        st.success("Données enregistrées avec succès !")
                    except Exception as e:
                        st.error(f"Erreur lors de l'enregistrement: {e}")
            else:
                st.warning("Les colonnes attendues ne correspondent pas")
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier: {e}")


def formulaire_direction_regionale():
    st.header("Gestion des Directions Régionales")

    # Formulaire de saisie
    st.subheader("Ajouter une nouvelle direction régionale")
    with st.form(key='add_direction_regionale'):
        nom_direction = st.text_input("Nom de la direction")
        region = st.text_input("Région")
        matricule_agent = st.text_input("Matricule de l'agent")
        matricule_dr = st.text_input("Matricule du directeur")
        submit_button = st.form_submit_button(label="Enregistrer")

        if submit_button:
            data.enregistrer_direction_regionale(nom_direction, region, matricule_agent, matricule_dr)
            st.success("Direction régionale enregistrée avec succès")

    # Formulaire de modification
    st.subheader("Modifier une direction régionale existante")
    direction_regionale_id = st.number_input("ID de la direction régionale à modifier", min_value=1, step=1)
    with st.form(key='modify_direction_regionale'):
        nom_direction = st.text_input("Nom de la direction", key='modify_nom_direction')
        region = st.text_input("Région", key='modify_region')
        matricule_agent = st.text_input("Matricule de l'agent", key='modify_matricule_agent')
        matricule_dr = st.text_input("Matricule du directeur", key='modify_matricule_dr')
        modify_button = st.form_submit_button(label="Modifier")

        if modify_button:
            data.modifier_direction_regionale(direction_regionale_id, nom_direction, region, matricule_agent, matricule_dr)
            st.success("Direction régionale modifiée avec succès")

    # Chargement de données par fichier Excel
    st.subheader("Importer des directions régionales depuis un fichier Excel")
    uploaded_file = st.file_uploader("Choisir un fichier Excel", type="xlsx", key="direction_regionale_file")

    if uploaded_file is not None:
        try:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            sheet_name = st.selectbox("Choisir la feuille", sheet_names)
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

            st.dataframe(df)

            expected_columns = ["nom_direction", "region", "matricule_agent", "matricule_dr"]
            if all(column in df.columns for column in expected_columns):
                if st.button("Enregistrer dans la base de données"):
                    try:
                        for index, row in df.iterrows():
                            data.enregistrer_direction_regionale(row['nom_direction'], row['region'], row['matricule_agent'],
                                                            row['matricule_dr'])
                        st.success("Données enregistrées avec succès !")
                    except Exception as e:
                        st.error(f"Erreur lors de l'enregistrement: {e}")
            else:
                st.warning("Les colonnes attendues ne correspondent pas")
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier: {e}")




def formulaire_region():
    st.header("Gestion des Régions")

    # Formulaire de saisie
    st.subheader("Ajouter une nouvelle région")
    with st.form(key='add_region'):
        code_region = st.text_input("Code de la région")
        nom_region = st.text_input("Nom de la région")
        submit_button = st.form_submit_button(label="Enregistrer")

        if submit_button:
            data.enregistrer_region(code_region, nom_region)
            st.success("Région enregistrée avec succès")

    # Formulaire de modification
    st.subheader("Modifier une région existante")
    code_region = st.text_input("Code de la région à modifier", key='modify_code_region')
    with st.form(key='modify_region'):
        nom_region = st.text_input("Nom de la région", key='modify_nom_region')
        modify_button = st.form_submit_button(label="Modifier")

        if modify_button:
            data.modifier_region(code_region, nom_region)
            st.success("Région modifiée avec succès")

    # Chargement de données par fichier Excel
    st.subheader("Importer des régions depuis un fichier Excel")
    uploaded_file = st.file_uploader("Choisir un fichier Excel", type="xlsx", key="region_file")

    if uploaded_file is not None:
        try:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            sheet_name = st.selectbox("Choisir la feuille", sheet_names)
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

            st.dataframe(df)

            expected_columns = ["code_region", "nom_region"]
            if all(column in df.columns for column in expected_columns):
                if st.button("Enregistrer dans la base de données"):
                    try:
                        for index, row in df.iterrows():
                            data.enregistrer_region(row['code_region'], row['nom_region'])
                        st.success("Données enregistrées avec succès !")
                    except Exception as e:
                        st.error(f"Erreur lors de l'enregistrement: {e}")
            else:
                st.warning("Les colonnes attendues ne correspondent pas")
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier: {e}")




def formulaire_departement():
    st.header("Gestion des Départements")

    # Formulaire de saisie
    st.subheader("Ajouter un nouveau département")
    with st.form(key='add_departement'):
        code_departement = st.text_input("Code du département")
        nom_departement = st.text_input("Nom du département")
        f_code_region = st.text_input("Code de la région")
        submit_button = st.form_submit_button(label="Enregistrer")

        if submit_button:
            data.enregistrer_departement(code_departement, nom_departement, f_code_region)
            st.success("Département enregistré avec succès")

    # Formulaire de modification
    st.subheader("Modifier un département existant")
    code_departement = st.text_input("Code du département à modifier", key='modify_code_departement')
    with st.form(key='modify_departement'):
        nom_departement = st.text_input("Nom du département", key='modify_nom_departement')
        f_code_region = st.text_input("Code de la région", key='modify_f_code_region')
        modify_button = st.form_submit_button(label="Modifier")

        if modify_button:
            data.modifier_departement(code_departement, nom_departement, f_code_region)
            st.success("Département modifié avec succès")

    # Chargement de données par fichier Excel
    st.subheader("Importer des départements depuis un fichier Excel")
    uploaded_file = st.file_uploader("Choisir un fichier Excel", type="xlsx", key="departement_file")

    if uploaded_file is not None:
        try:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            sheet_name = st.selectbox("Choisir la feuille", sheet_names)
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

            st.dataframe(df)

            expected_columns = ["code_departement", "nom_departement", "f_code_region"]
            if all(column in df.columns for column in expected_columns):
                if st.button("Enregistrer dans la base de données"):
                    try:
                        for index, row in df.iterrows():
                            data.enregistrer_departement(row['code_departement'], row['nom_departement'], row['f_code_region'])
                        st.success("Données enregistrées avec succès !")
                    except Exception as e:
                        st.error(f"Erreur lors de l'enregistrement: {e}")
            else:
                st.warning("Les colonnes attendues ne correspondent pas")
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier: {e}")


def formulaire_sous_prefecture():
    st.header("Gestion des Sous-Préfectures")

    # Formulaire de saisie
    st.subheader("Ajouter une nouvelle sous-préfecture")
    with st.form(key='add_sous_prefecture'):
        code_sous_prefecture = st.text_input("Code de la sous-préfecture")
        nom_sous_prefecture = st.text_input("Nom de la sous-préfecture")
        f_code_departement = st.text_input("Code du département")
        submit_button = st.form_submit_button(label="Enregistrer")

        if submit_button:
            data.enregistrer_sous_prefecture(code_sous_prefecture, nom_sous_prefecture, f_code_departement)
            st.success("Sous-préfecture enregistrée avec succès")

    # Formulaire de modification
    st.subheader("Modifier une sous-préfecture existante")
    code_sous_prefecture = st.text_input("Code de la sous-préfecture à modifier", key='modify_code_sous_prefecture')
    with st.form(key='modify_sous_prefecture'):
        nom_sous_prefecture = st.text_input("Nom de la sous-préfecture", key='modify_nom_sous_prefecture')
        f_code_departement = st.text_input("Code du département", key='modify_f_code_departement')
        modify_button = st.form_submit_button(label="Modifier")

        if modify_button:
            data.modifier_sous_prefecture(code_sous_prefecture, nom_sous_prefecture, f_code_departement)
            st.success("Sous-préfecture modifiée avec succès")

    # Chargement de données par fichier Excel
    st.subheader("Importer des sous-préfectures depuis un fichier Excel")
    uploaded_file = st.file_uploader("Choisir un fichier Excel", type="xlsx", key="sous_prefecture_file")

    if uploaded_file is not None:
        try:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            sheet_name = st.selectbox("Choisir la feuille", sheet_names)
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

            st.dataframe(df)

            expected_columns = ["code_sous_prefecture", "nom_sous_prefecture", "f_code_departement"]
            if all(column in df.columns for column in expected_columns):
                if st.button("Enregistrer dans la base de données"):
                    try:
                        for index, row in df.iterrows():
                            data.enregistrer_sous_prefecture(row['code_sous_prefecture'], row['nom_sous_prefecture'], row['f_code_departement'])
                        st.success("Données enregistrées avec succès !")
                    except Exception as e:
                        st.error(f"Erreur lors de l'enregistrement: {e}")
            else:
                st.warning("Les colonnes attendues ne correspondent pas")
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier: {e}")


def formulaire_indicateur():
    st.header("Gestion des Indicateurs")

    # Formulaire de saisie
    st.subheader("Ajouter un nouvel indicateur")
    with st.form(key='add_indicateur'):
        id_indicateur = st.text_input("ID Indicateur")
        indicateur = st.text_input("Indicateur")
        type_indicateur = st.text_input("Type Indicateur")
        id_domaine = st.text_input("ID Domaine")
        submit_button = st.form_submit_button(label="Enregistrer")

        if submit_button:
            data.enregistrer_indicateur(id_indicateur, indicateur, type_indicateur, id_domaine)
            st.success("Indicateur enregistré avec succès")

    # Formulaire de modification
    st.subheader("Modifier un indicateur existant")
    id = st.text_input("ID de l'indicateur à modifier", key='modify_id')
    with st.form(key='modify_indicateur'):
        id_indicateur = st.text_input("ID Indicateur", key='modify_id_indicateur')
        indicateur = st.text_input("Indicateur", key='modify_indicateur')
        type_indicateur = st.text_input("Type Indicateur", key='modify_type_indicateur')
        id_domaine = st.text_input("ID Domaine", key='modify_id_domaine')
        modify_button = st.form_submit_button(label="Modifier")

        if modify_button:
            data.modifier_indicateur(id, id_indicateur, indicateur, type_indicateur, id_domaine)
            st.success("Indicateur modifié avec succès")

    # Chargement de données par fichier Excel
    st.subheader("Importer des indicateurs depuis un fichier Excel")
    uploaded_file = st.file_uploader("Choisir un fichier Excel", type="xlsx", key="indicateur_file")

    if uploaded_file is not None:
        try:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            sheet_name = st.selectbox("Choisir la feuille", sheet_names)
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

            st.dataframe(df)

            expected_columns = ["id_indicateur", "indicateur", "type_indicateur", "id_domaine"]
            if all(column in df.columns for column in expected_columns):
                if st.button("Enregistrer dans la base de données"):
                    try:
                        for index, row in df.iterrows():
                            data.enregistrer_indicateur(row['id_indicateur'], row['indicateur'], row['type_indicateur'], row['id_domaine'])
                        st.success("Données enregistrées avec succès !")
                    except Exception as e:
                        st.error(f"Erreur lors de l'enregistrement: {e}")
            else:
                st.warning("Les colonnes attendues ne correspondent pas")
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier: {e}")



def formulaire_domaine():
    st.header("Gestion des Domaines")

    # Formulaire de saisie
    st.subheader("Ajouter un nouveau domaine")
    with st.form(key='add_domaine'):
        id_domaine = st.text_input("ID Domaine")
        titre_domaine = st.text_input("Titre Domaine")
        submit_button = st.form_submit_button(label="Enregistrer")

        if submit_button:
            data.enregistrer_domaine(id_domaine, titre_domaine)
            st.success("Domaine enregistré avec succès")

    # Formulaire de modification
    st.subheader("Modifier un domaine existant")
    id = st.text_input("ID du domaine à modifier", key='modify_id')
    with st.form(key='modify_domaine'):
        id_domaine = st.text_input("ID Domaine", key='modify_id_domaine')
        titre_domaine = st.text_input("Titre Domaine", key='modify_titre_domaine')
        modify_button = st.form_submit_button(label="Modifier")

        if modify_button:
            data.modifier_domaine(id, id_domaine, titre_domaine)
            st.success("Domaine modifié avec succès")

    # Chargement de données par fichier Excel
    st.subheader("Importer des domaines depuis un fichier Excel")
    uploaded_file = st.file_uploader("Choisir un fichier Excel", type="xlsx", key="domaine_file")

    if uploaded_file is not None:
        try:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            sheet_name = st.selectbox("Choisir la feuille", sheet_names)
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

            st.dataframe(df)

            expected_columns = ["id_domaine", "titre_domaine"]
            if all(column in df.columns for column in expected_columns):
                if st.button("Enregistrer dans la base de données"):
                    try:
                        for index, row in df.iterrows():
                            data.enregistrer_domaine(row['id_domaine'], row['titre_domaine'])
                        st.success("Données enregistrées avec succès !")
                    except Exception as e:
                        st.error(f"Erreur lors de l'enregistrement: {e}")
            else:
                st.warning("Les colonnes attendues ne correspondent pas")
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier: {e}")

"""
Fin
"""


