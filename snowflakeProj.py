import os 
import pandas as pd 
import snowflake.connector
import streamlit as st 
from io import StringIO


page = st.sidebar.selectbox("Veuillez choisir votre page:", ["Accueil", "Dépôt"])

if page == "Accueil":
    st.subheader("Bienvenue sur le dépôt officiel dédié à téléverser des fichiers sur Snowflake")
elif page == "Dépôt":
    st.subheader("Ici vous pouvez faire votre téléversement")
    
    file_upload = st.file_uploader("Sélectionnez le fichier CSV à upload", type="csv")
    delimiter = st.selectbox("Choisissez le délimiteur du fichier", [",", ";", " ", "-", "_"])
    
    if file_upload is not None:
        bytes_data = file_upload.read()
        s = str(bytes_data, 'utf-8')
        data = StringIO(s)
        
        # Afficher l'aperçu des données en fonction du délimiteur choisi
        try:
            df = pd.read_csv(data, delimiter=delimiter)
            st.write("Aperçu du fichier téléversé :")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {e}")
        
        table_name = st.text_input("Nom de la table dans Snowflake :")
        
        if st.button('Confirmer le téléversement'):
            if table_name:
                try:
                    conn = get_snowflake_connection()
                    upload_to_snowflake(conn, df, table_name)
                    st.success(f"Les données ont été téléversées dans la table {table_name} de Snowflake avec succès.")
                except Exception as e:
                    st.error(f"Erreur lors du téléversement des données : {e}")
            else:
                st.error("Veuillez saisir un nom de table.")
