import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

st.set_page_config(page_title="KPI 1", page_icon=":taxi:", layout="wide")

st.title("KPI: 5% increase in demand for the type of service contracted")
st.markdown("***")

st.sidebar.header("Filter here:")