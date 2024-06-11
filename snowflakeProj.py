import os 
import pandas as pd 
import snowflake.connector
import streamlit as st 


Page=st.sidebar.selectbox("Veuillez choisir votre page:",["Accueil","Dépôt"])
if Page=="Accueil": 
  st.title("Bienvenue sur le dépôt officiel dédié à téléverser des fichiers sur Snowflake")
elif Page=="Dépôt": 
  st.title("Ici vous pouvez faire votre téléversement")
