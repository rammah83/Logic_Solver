import streamlit as st

st.set_page_config(page_title="Logic Tools", layout="wide")
st.header("Logic Solver", divider=True)

with st.sidebar:
    st.logo(image=r"./res/img/mylogo.jpeg")

pages = {
    "HOME": [st.Page("./app_pages/home.py", title="Home", icon="🏠")],
    "SYMBOLIC LOGIC SOLVER": [
        st.Page("./app_pages/logic_solver.py", title="Propositional Logic", icon="🧠"),
        st.Page("./app_pages/smart_logic_solver.py", title="Smart Logic", icon="🧠"),
        ],
}

pg = st.navigation(pages, position="sidebar")
pg.run()
