import streamlit as st
import importlib.util

# Set page configuration as the very first Streamlit command
st.set_page_config(page_title="Final Project - HENRY (Group 5)", page_icon=":taxi:", layout="wide")


st.title(":bar_chart: HENRY: Final Project - Group 5")
st.markdown("***")

st.image("Cover.jpg", caption="SmartANALYTICS")

# List of KPI page names
kpi_names = ["KPI 1", "KPI 2", "KPI 3", "KPI 4", "KPI 5"]

# Create a sidebar widget for selecting a KPI page
selected_kpi = st.selectbox("Select a KPI Page", kpi_names)

# Define a function to display the selected KPI page
def display_selected_kpi(selected_kpi):
    # Create the full import path for the selected KPI page
    import_path = f"Pages.{selected_kpi.replace(' ', '_')}"

    # Try to dynamically import the selected KPI page
    try:
        module = importlib.import_module(import_path)
        page_function = getattr(module, f"display_{selected_kpi.replace(' ', '_')}_page")
    except ModuleNotFoundError:
        st.error("Page not found.")
        return

    # Call the function to display the selected KPI page
    page_function()

# Use the function to display the selected KPI page
display_selected_kpi(selected_kpi)