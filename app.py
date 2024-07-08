import sqlite3
import streamlit as st

import data
import page as p

# Configuration de la page
st.set_page_config(page_title="Annuaire statistique", page_icon="📊", layout="wide")

# CSS pour styliser le contenu
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf, #2e7bff);
        color: white;
    }
    .sidebar .sidebar-content h2 {
        color: white;
    }
    .reportview-container {
        background: #f5f5f5;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2e7bcf;
    }
    </style>
    """, unsafe_allow_html=True)

# Afficher le logo de l'entreprise
st.image("other_file/images.png", width=75)  # Remplacez "images.png" par le chemin réel de votre logo

# Titre de l'application
st.title("Plateforme de saisie des données des Annuaires Statistiques")
st.write("------------------------------------------------------------")

# Sidebar menu
st.sidebar.title("Menu")
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def main():
    if not st.session_state['logged_in']:
        page = st.sidebar.selectbox("Choisir une page", ["Connexion"])
    else:
        if st.session_state['role'] == 'agent_collecte':
            page = st.sidebar.selectbox("Choisir une page", ["Page 1"])
        elif st.session_state['role'] == 'directeur':
            page = st.sidebar.selectbox("Choisir une page", ["Page 1", "Page 2"])
        elif st.session_state['role'] == 'equipe_technique':
            page = st.sidebar.selectbox("Choisir une page", ["Page 1", "Page 2", "Page 3", "Page 4"])

    if page == "Connexion":
        st.header("Connexion des Utilisateurs")

        with st.form("connexion_utilisateur"):
            email = st.text_input("Email")
            matricule = st.text_input("Matricule")
            submitted = st.form_submit_button("Se connecter")

            if submitted:
                role, user, direction_regionale = p.authenticate(email, matricule)
                if role:
                    st.session_state['logged_in'] = True
                    st.session_state['role'] = role
                    st.session_state['user'] = user
                    st.session_state['direction_regionale'] = direction_regionale
                    st.success(f"Connecté avec succès en tant que {role}")
                    st.experimental_rerun()
                else:
                    st.error("Identifiants incorrects")
    elif page == "Page 1":
        p.page1()
    elif page == "Page 2" and st.session_state['logged_in']:
        user = st.session_state['user']
        direction_regionale = st.session_state['direction_regionale']
        p.page2(user, direction_regionale)
    elif page == "Page 3" and st.session_state['logged_in']:
        p.page3()
    elif page == "Page 4" and st.session_state['logged_in']:
        p.page4()

    # Ajouter une fonctionnalité de déconnexion
    if st.session_state['logged_in']:
        if st.sidebar.button("Se déconnecter"):
            st.session_state['logged_in'] = False
            st.experimental_rerun()

if __name__ == '__main__':
    main()
