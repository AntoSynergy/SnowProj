import os
import pandas as pd
import snowflake.connector
import streamlit as st
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns


# Configuration de la connexion Snowflake
SNOWFLAKE_USER = 'Anto'
SNOWFLAKE_PASSWORD = 'votre_mot_de_passe'
SNOWFLAKE_ACCOUNT = 'TCNMJLT.PZ12020'
SNOWFLAKE_DATABASE = 'SNOWPROJ'
SNOWFLAKE_SCHEMA = 'PUBLIC'
SNOWFLAKE_WAREHOUSE = 'COMPUTE_WH'

# Fonction pour se connecter à Snowflake
#def get_snowflake_connection():
#    conn = snowflake.connector.connect(
#        user=SNOWFLAKE_USER,
#        password=SNOWFLAKE_PASSWORD,
#        account=SNOWFLAKE_ACCOUNT,
#        database=SNOWFLAKE_DATABASE,
#        schema=SNOWFLAKE_SCHEMA,
#        warehouse=SNOWFLAKE_WAREHOUSE
#    )
#    return conn

# Fonction pour téléverser un DataFrame dans Snowflake
#def upload_to_snowflake(conn, df, table_name):
#    cursor = conn.cursor()
#    # Crée la table si elle n'existe pas
#    create_table_query = f"""
#    CREATE TABLE IF NOT EXISTS {table_name} (
#        {', '.join([f"{col} STRING" for col in df.columns])}
#    )
#    """
#    cursor.execute(create_table_query)

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
st.title('Téléversement de fichiers vers Snowflake')

uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    # Lire le fichier téléversé en DataFrame
    bytes_data = uploaded_file.read()
    s = str(bytes_data, 'utf-8')
    data = StringIO(s)
    df = pd.read_csv(data)
    
    st.write("Aperçu du fichier téléversé :")
    st.dataframe(df)
    
    table_name = st.text_input("Nom de la table dans Snowflake :")
    
    if st.button('Téléverser vers Snowflake'):
        if table_name:
            conn = get_snowflake_connection()
            upload_to_snowflake(conn, df, table_name)
            st.success(f"Les données ont été téléversées dans la table {table_name} de Snowflake avec succès.")
        else:
            st.error("Veuillez saisir un nom de table.")
