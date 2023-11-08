import streamlit as st
import importlib.util

# Set page configuration as the very first Streamlit command
st.set_page_config(page_title="Final Project - HENRY (Group 5)", page_icon=":taxi:", layout="wide")

# List of KPI page names
kpi_names = ["KPI 1", "KPI 2", "KPI 3", "KPI 4", "KPI 5"]
ml_names = ["ML 1 Intro", "ML 2 Data Analysis", "ML 3 Model Results"]

# Add a title to the sidebar
st.sidebar.title("Select a Page")

# Create a sidebar select box for selecting a page
selected_page = st.sidebar.selectbox("Select a Page", ["Main Page", "KPIs"] + ml_names)

# Define a function to display the selected KPI page
def display_selected_kpi_page(selected_page):
    if selected_page == "Main Page":
        # Display the main page content
        st.title(":bar_chart: HENRY: Final Project - Group 5")
        st.image("Cover.jpg", caption="SmartANALYTICS")
    elif selected_page in kpi_names:
        # Display the selected KPI page
        import_path = f"Pages.{selected_page.replace(' ', '_')}"
        try:
            module = importlib.import_module(import_path)
            page_function = getattr(module, f"display_{selected_page.replace(' ', '_')}_page")
            page_function()
        except ModuleNotFoundError:
            st.error("Page not found.")

# Define a dictionary to map selected pages to their respective functions
ml_page_functions = {
    "ML 1 Intro": "display_ML_1_Intro_page",
    "ML 2 Data Analysis": "display_ML_2_Data_Analysis_page",
    "ML 3 Model Results": "display_ML_3_Model_Results_page"
}

# Define a function to display the selected ML page
def display_selected_ml_page(selected_page):
    import_path = f"ML_Pages.{selected_page.replace(' ', '_')}"
    if selected_page in ml_page_functions:
        try:
            module = importlib.import_module(import_path)
            page_function_name = ml_page_functions[selected_page]
            page_function = getattr(module, page_function_name)
            page_function()
        except ModuleNotFoundError:
            st.error("Page not found.")
    else:
        st.error("Page not found.")

# Call the function to display the selected page
if selected_page == "Main Page":
    display_selected_kpi_page(selected_page)
elif selected_page == "KPIs":
    selected_kpi_page = st.sidebar.selectbox("Select KPI Page", kpi_names)
    display_selected_kpi_page(selected_kpi_page)
else:
    display_selected_ml_page(selected_page)