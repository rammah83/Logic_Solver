from narwhals import col
import sympy as sp
from utils.logical_syllogism import symbolize_expression
from utils.logical_syllogism import PropositionalLogicSyllogism as Pls
from sympy.logic.boolalg import simplify_logic, to_cnf
from sympy.logic.inference import satisfiable, valid, PropKB, entails

# from string import ascii_lowercase
import streamlit as st

# st.subheader("Logic :blue[cool] :sunglasses:")

col_kb, col_entails = st.columns([1, 1], gap="small", vertical_alignment="bottom")
logical_statement = col_kb.text_area(
    "*Building Knwoledge Base (KB) _Logical Statement_*",
    help="use '>>' for 'implies', '&' for 'and', '|' for 'or', '~' for 'not': don't use E, I, O, N, S, Q",
)
check_entilments = col_entails.text_input(
    "Entailments", help="use '>>' for 'implies', '&' for 'and', '|' for 'or', '~' for 'not': don't use E, I, O, N, S, Q"
)

logical_statement = logical_statement.replace("=>", ">>").replace("<=", "<<").split("\n")
st.info(logical_statement)
if st.button("SOLVE"):
    # solve model
    problem = Pls(logical_statement)
    solution = problem.solve()
    st.write("##### Solutions:")
    if isinstance(solution, str):
        st.write(solution)
    else:
        st.dataframe(solution)

    expender = st.columns([3,1])[0].expander("## Details")
    col_sentence, col_result, col_validity = expender.columns(
        [3, 2, 1], gap="small", vertical_alignment="top"
    )
    col_sentence.write("_Statement:_")
    col_result.write("_Statement Evaluation:_")
    col_validity.write("_Validity:_")
    for statement in logical_statement:
        # display and List statment
        sym_stmt, evaluted = symbolize_expression(statement)
        col_sentence.latex(sym_stmt)
        col_result.latex(evaluted)
        col_validity.latex(
            "✅ Tautology" if evaluted == r"\text{True}"
            else "🙅🏽 Impossible" if evaluted == r"\text{False}"
            else "🧐 It\space depends"
        )
    col_sentence.write("---")
    col_result.write("---")
    
    # col_sentence.latex(problem.representation())
    col_result.latex(problem.representation(simplify=True))
    
