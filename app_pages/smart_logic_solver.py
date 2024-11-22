from math import log
from narwhals import col
import sympy as sp
from sympy.logic.boolalg import simplify_logic, to_cnf
from sympy.logic.inference import satisfiable, valid, PropKB, entails

# from string import ascii_lowercase
import streamlit as st

# st.subheader("Logic :blue[cool] :sunglasses:")

col_kb, col_entails, _ = st.columns(
        [2,1,3], gap="small", vertical_alignment="bottom"
    )
logical_statement = col_kb.text_area(
        "*Building Knwoledge Base (KB) _Logical Statement_*",
        help="use '>>' for 'implies', '&' for 'and', '|' for 'or', '~' for 'not': don't use E, I, O, N, S, Q",
    )
logical_statement = logical_statement.replace("=>", ">>").replace("<=", "<<")
st.write(logical_statement)
if st.button("SOLVE"):
    container = st.container()
    expender = st.expander("## Details")
    col_sentence, col_result, col_validity = expender.columns(
            [2, 1, 3], gap="small", vertical_alignment="top"
        )
    col_sentence.write("_Statement:_")
    col_result.write("_Statement Evaluation:_")
    for statement in logical_statement.split("\n"):
        # display and List KB
        symp_statement = sp.sympify(statement)
        col_sentence.latex(sp.latex(symp_statement))
        col_result.latex(sp.latex(sp.simplify_logic(symp_statement)))
    col_sentence.write("---")
    col_result.write("---")
    col_sentence.write(".`.")


