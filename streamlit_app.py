import streamlit as st
import pandas as pd

st.set_page_config(
    layout="wide",
    page_title="Wespilift",
    page_icon="logo_wespi.png",
)

st.sidebar.text('Powered by: ')
#image = Image.open('logo_wespi.png')
#st.sidebar.image(image)
st.sidebar.image('logo_wespi.png')

# -- page setup --
my_calculations = st.Page(
    #page = "views/my_calc.py",
    page = "my_calc.py",
    title = "My Calculations",
    icon = ":material/account_circle:",
    default = True,
)
new_calculations = st.Page(
    #page = "views/data_input.py",
    page = "new_calc.py",
    title = "Add New Calculation",
    icon = ":material/bar_chart:",
)
#ipr_curve = st.Page(
#    #page = "views/ipr_curve.py",
#    page = "ipr_curve.py",
#    title = "Calculation & IPR Curve",
#    icon = ":material/bar_chart:",
#)

# --- navigation setup (without sections) ---
#pg = st.navigation(pages=[my_calculations, new_calculations, ipr_curve])
pg = st.navigation(pages=[my_calculations, new_calculations])

# --- run navigation ---
pg.run()
