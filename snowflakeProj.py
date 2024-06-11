import os
import pandas as pd
import snowflake.connector
import streamlit as st
from io import StringIO

# Configuration de la connexion Snowflake
SNOWFLAKE_USER = os.getenv('SECRET_USER')
st.text(SNOWFLAKE_USER)
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

page = st.sidebar.selectbox("Veuillez choisir votre page:", ["Accueil", "Dépôt"])

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
