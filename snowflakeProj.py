import os
import pandas as pd
import snowflake.connector
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# Configuration de la connexion Snowflake
SNOWFLAKE_USER = os.getenv('SECRET_USER')
SNOWFLAKE_PASSWORD = os.getenv('SECRET_PASSWORD')
SNOWFLAKE_ACCOUNT = os.getenv('SECRET_ACCOUNT')
SNOWFLAKE_DATABASE = 'SNOWPROJ'
SNOWFLAKE_SCHEMA = 'PUBLIC'
SNOWFLAKE_WAREHOUSE = 'COMPUTE_WH'

# Fonction pour se connecter à Snowflake
def get_snowflake_connection():
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
        warehouse=SNOWFLAKE_WAREHOUSE
    )
    return conn

# Fonction pour téléverser un DataFrame dans Snowflake
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
                doublequote=True  # Gérer les guillemets doubles correctement
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

elif page == "Analyse":
    st.subheader("Analyse des données")

    # Chargement du fichier CSV pour l'analyse
    file_upload = st.file_uploader("Sélectionnez le fichier CSV à analyser", type="csv")
    
    if file_upload is not None:
        df = pd.read_csv(file_upload)
        
        st.subheader("Aperçu des données")
        st.write(df)
        
        st.subheader("Analyse de la qualité des données")
        
        # Analyse des doublons par colonne
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Nombre de doublons par colonne")
            duplicates_info = {col: df[col].duplicated().sum() for col in df.columns}
            st.write(duplicates_info)
            
            st.write("Détails des doublons par colonne")
            for col in df.columns:
                duplicated_values = df[df.duplicated([col], keep=False)][col].value_counts()
                st.write(f"{col} - Valeurs dupliquées")
                st.write(duplicated_values)
                
        with col2:
            # Analyse des valeurs manquantes
            st.write("Nombre de valeurs manquantes par colonne")
            missing_values = df.isnull().sum()
            st.write(missing_values)
            
            # Visualisation des valeurs manquantes
            st.write("Histogramme des valeurs manquantes")
            fig, ax = plt.subplots()
            missing_values.plot(kind='bar', ax=ax)
            ax.set_title("Valeurs manquantes par colonne")
            ax.set_xlabel("Colonnes")
            ax.set_ylabel("Nombre de valeurs manquantes")
            st.pyplot(fig)
            
        # Autres analyses possibles de la qualité des données
        st.write("Analyse de l'uniformité des données")
        uniformity_info = {col: df[col].value_counts(normalize=True).max() for col in df.columns}
        st.write(uniformity_info)

        # Visualisation de l'uniformité
        st.write("Histogramme de l'uniformité des données")
        uniformity_series = pd.Series(uniformity_info)
        fig, ax = plt.subplots()
        uniformity_series.plot(kind='bar', ax=ax)
        ax.set_title("Uniformité des données par colonne")
        ax.set_xlabel("Colonnes")
        ax.set_ylabel("Proportion de la valeur la plus fréquente")
        st.pyplot(fig)
