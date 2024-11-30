import streamlit as st

st.set_page_config(page_title="Logic Tools", layout="wide")
st.header("Logic Solver", divider=True)

with st.sidebar:
    st.logo(image=r"./res/img/mylogo.jpeg")

pages = {
    "HOME": [st.Page("./app_pages/home.py", title="Home", icon="🏠")],
    "SYMBOLIC LOGIC SOLVER": [
        st.Page("./app_pages/propositional_logic.py", title="Propositional Logic", icon="🧠"),
        st.Page("./app_pages/predicated_logic.py", title="Predicated Logic", icon="🧠"),
        ],
}

pg = st.navigation(pages, position="sidebar")
pg.run()
