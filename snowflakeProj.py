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
    
    bytes_data=file_upload.read()
    validate=st.button("Valider le téléchargement")
  
