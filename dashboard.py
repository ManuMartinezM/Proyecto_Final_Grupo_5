import streamlit as st
import importlib.util

# Set page configuration as the very first Streamlit command
st.set_page_config(page_title="Final Project - HENRY (Group 5)", page_icon=":taxi:", layout="wide")

# List of KPI page names
kpi_names = ["KPI 1", "KPI 2", "KPI 3", "KPI 4", "KPI 5"]

# Add a title to the sidebar
st.sidebar.title("Select a Page")

# Create a sidebar select box for selecting a page
selected_page = st.sidebar.selectbox("Choose a Page", ["Main Page"] + kpi_names)

# Define a function to display the selected KPI page
def display_selected_page(selected_page):
    if selected_page == "Main Page":
        # Display the main page content
        st.title(":bar_chart: HENRY: Final Project - Group 5")
        st.markdown("***")
        st.image("Cover.jpg", caption="SmartANALYTICS")
    else:
        # Display the selected KPI page
        import_path = f"Pages.{selected_page.replace(' ', '_')}"
        try:
            module = importlib.import_module(import_path)
            page_function = getattr(module, f"display_{selected_page.replace(' ', '_')}_page")
        except ModuleNotFoundError:
            st.error("Page not found.")
            return
        page_function()

# Use the function to display the selected page
display_selected_page(selected_page)