import os 
import pandas as pd 
import snowflake.connector
import streamlit as st 


Page=st.sidebar.selectbox("Veuillez choisir votre page:",["Accueil","Dépôt"])
if Page=="Accueil": 
  st.subheader("Bienvenue sur le dépôt officiel dédié à téléverser des fichiers sur Snowflake")
elif Page=="Dépôt": 
  st.subheader("Ici vous pouvez faire votre téléversement")
  file_upload=st.file_uploader("Selectionnez le fichier CSV à upload",type="CSV")
  delimiter=st.selectbox("Choisissez le delimiter du fichier",[",",";"," ","-","_"])
  if file_upload is not None:   
            # Charger le fichier CSV dans un DataFrame Pandas
    try:
      if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file, sep=delimiter)
      elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
      else:
        st.error("Format de fichier non pris en charge.")
        st.stop()
                
                # Afficher les premières lignes du DataFrame
    st.write("Aperçu des données :")
    st.write(df.head())
      
