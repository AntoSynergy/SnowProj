import os
import pandas as pd
import snowflake.connector
import streamlit as st
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns


# connection à snowflake 

conn=st.connection("snowflake")
session=conn.session()
df = conn.query("SELECT * from mytable;", ttl=600)

