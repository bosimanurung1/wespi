import streamlit as st

st.set_page_config(layout="wide")

st.sidebar.text('Powered by: ')
#image = Image.open('logo_wespi.png')
st.sidebar.image('logo_wespi.png')

# -- page setup --
my_calculations = st.Page(
    #page = "views/my_calc.py",
    page = "my_calc.py",
    title = "My Calculations",
    icon = ":material/account_circle:",
    default = True,
)
input_page = st.Page(
    #page = "views/data_input.py",
    page = "data_input.py",
    title = "Data Input",
    icon = ":material/bar_chart:",
)
ipr_curve = st.Page(
    #page = "views/ipr_curve.py",
    page = "ipr_curve.py",
    title = "Calculation & IPR Curve",
    icon = ":material/bar_chart:",
)

# --- navigation setup (without sections) ---
pg = st.navigation(pages=[my_calculations, input_page, ipr_curve])

# --- run navigation ---
pg.run()
