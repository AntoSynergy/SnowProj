import os
import pandas as pd
import snowflake.connector
import streamlit as st
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns


def upload_to_snowflake(conn, df, table_name):
    cursor = conn.cursor()
    # Crée la table si elle n'existe pas
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {', '.join([f"{col} STRING" for col in df.columns])}
    )
    """
    cursor.execute(create_table_query)

    # Prépare les données pour l'insertion
    for i, row in df.iterrows():
        insert_query = f"""
        INSERT INTO {table_name} ({', '.join(df.columns)})
        VALUES ({', '.join(['%s'] * len(row))})
        """
        cursor.execute(insert_query, tuple(row))
    conn.commit()
    cursor.close()

# Interface utilisateur Streamlit
st.title("Bienvenue")

page = st.sidebar.selectbox("Veuillez choisir votre page:", ["Accueil", "Dépôt", "Analyse"])

if page == "Accueil":
    st.subheader("Bienvenue sur le dépôt officiel dédié à téléverser des fichiers sur Snowflake")
elif page == "Dépôt":
    st.subheader("Ici vous pouvez faire votre téléversement")
    
    file_upload = st.file_uploader("Sélectionnez le fichier CSV à uploader", type="csv")
    delimiter = st.selectbox("Choisissez le délimiteur du fichier", [",", ";", "_"])
    skip_rows = st.number_input("Nombre de lignes à ignorer au début", min_value=0, step=1, value=0)
    skip_blank_lines = st.checkbox("Ignorer les lignes blanches", value=True)
    
    if file_upload is not None:
        bytes_data = file_upload.read()
        s = str(bytes_data, 'utf-8')
        data = StringIO(s)
        
        try:
            df = pd.read_csv(
                data, 
                delimiter=delimiter, 
                skiprows=skip_rows,
                skip_blank_lines=skip_blank_lines,
                doublequote=True # Gérer les guillemets doubles correctement
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

if page == "Analyse":
    # Fonction d'analyse de la qualité des données
    def analyze_data_quality(df):
        st.subheader("Analyse de la qualité des données")
        
        # Création de deux colonnes pour afficher les tableaux côte à côte
        col1, col2 = st.columns(2)
        
        # Vérification des doublons par colonne
        with col1:
            st.write("Nombre de doublons par colonne :")
            for col in df.columns:
                duplicates = df[df.duplicated(subset=[col], keep=False)]
                duplicates_count = duplicates[col].value_counts()
                if len(duplicates_count) > 0:
                    st.write(f"Colonne '{col}' :")
                    st.write(duplicates_count)
                else:
                    st.write(f"Colonne '{col}' : Aucun doublon trouvé.")
        
        # Comptage des valeurs manquantes par colonne
        with col2:
            st.write("Nombre de valeurs manquantes par colonne :")
            missing_values_count = df.isnull().sum()
            st.write(missing_values_count)
            
            # Affichage de l'histogramme des valeurs manquantes par colonne
            st.write("Histogramme des valeurs manquantes par colonne :")
            fig, ax = plt.subplots()
            missing_values_count.plot(kind='bar', ax=ax)
            plt.title("Histogramme des valeurs manquantes par colonne")
            plt.xlabel("Colonnes")
            plt.ylabel("Nombre de valeurs manquantes")
            st.pyplot(fig)
            
            # Vérification de l'uniformité des données par colonne
            st.write("Distribution des valeurs par colonne :")
            for col in df.columns:
                st.write(f"Colonne '{col}' :")
                fig, ax = plt.subplots()
                df[col].value_counts().plot(kind='bar', ax=ax)
                st.pyplot(fig)
        
        # Autres analyses de qualité des données à ajouter selon vos besoins

    # Chargement du fichier CSV
    file_upload = st.file_uploader("Sélectionnez le fichier CSV à analyser", type="CSV")

    if file_upload is not None:
        df = pd.read_csv(file_upload)
        
        st.subheader("Aperçu des données")
        st.write(df)
        
