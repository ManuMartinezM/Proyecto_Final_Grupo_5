import streamlit as st
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="KPI 1", page_icon=":taxi:", layout="wide")

st.header("KPI: 5% increase in demand in airport taxi rides")
st.markdown("***")

# Replace these values with your database information
host = 'database-1.cb8vqbpvimzr.us-east-2.rds.amazonaws.com'
user = 'admin'
password = 'adminadmin'
database = 'NYC_TAXIS'

# Establish a connection to the database
connection = pymysql.connect(host=host, user=user, password=password, database=database)
cursor = connection.cursor()