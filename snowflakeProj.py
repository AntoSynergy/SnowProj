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
    delimiter = st.selectbox("Choisissez le délimiteur du fichier", [",", ";","_"])
    quotechar = st.selectbox("Choisissez le caractère de citation", ['"', "'", ""])
    skip_rows = st.number_input("Nombre de lignes à ignorer au début", min_value=0, step=1, value=0)
    skip_blank_lines = st.checkbox("Ignorer les lignes blanches", value=True)
    
    if file_upload is not None:
        bytes_data = file_upload.read()
        s = str(bytes_data, 'utf-8')
        data = StringIO(s)
        
        # Afficher l'aperçu des données en fonction du délimiteur choisi
        try:
            df = pd.read_csv(
                data, 
                delimiter=delimiter, 
                quotechar=quotechar if quotechar else None,
                skiprows=skip_rows,
                skip_blank_lines=skip_blank_lines
            )
            st.write("Aperçu du fichier téléversé :")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {e}")
        
        table_name = st.text_input("Nom de la table dans Snowflake :")
        
        if st.button('Valider le téléchargement'):
            if table_name:
                conn = get_snowflake_connection()
                upload_to_snowflake(conn, df, table_name)
                st.success(f"Les données ont été téléversées dans la table {table_name} de Snowflake avec succès.")
            else:
                st.error("Veuillez saisir un nom de table.")
