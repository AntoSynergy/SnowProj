import os
import pandas as pd
import snowflake.connector
import streamlit as st
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns


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
