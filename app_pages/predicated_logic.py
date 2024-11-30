from utils.logical_syllogism import symbolize_expression
from z3 import ForAll, Exists, Implies, Not, And, Or, solve

# from string import ascii_lowercase
import streamlit as st

# st.subheader("Logic :blue[cool] :sunglasses:")
with st.sidebar:
    mode_to_use = st.selectbox(
        "## Select Mode",
        options=["Solve models", "Check Entailments"],
        index=0,
    )

col_kb, col_entails = st.columns([1, 1], gap="small", vertical_alignment="bottom")
logical_statement = col_kb.text_area(
    "*Building Knwoledge Base (KB): _Logical Statement_*",
    help="use '>>' for 'implies', '&' for 'and', '|' for 'or', '~' for 'not', Exists for 'exists', ForAll for 'All': don't use E, I, O, N, S, Q",
    height=200,
    
)
statement_entilment = col_entails.text_input(
    "Conclusion to entile",
    help="use '>>' for 'implies', '&' for 'and', '|' for 'or', '~' for 'not', Exists for 'exists', ForAll for 'All': don't use E, I, O, N, S, Q",
    disabled=mode_to_use != "Check Entailments",
)

logical_statement = (
    logical_statement.replace("=>", ">>").replace("<=", "<<").split("\n")
)
def convert_to_z3(statements: list[str]) -> list:
    """Convert statements to Z3"""
    from z3 import Bool, And, Or, Not, Implies, ForAll, Exists
    z3_statements = []
    for statement in statements:
        statement = statement.replace("=>", ">>").replace("<=", "<<")
        # Create a dictionary of Boolean variables
        vars_dict = {var: Bool(var) for var in set(statement) if var.isalpha()}
        # Replace logical operators
        statement = statement.replace("&", "And").replace("|", "Or").replace("~", "Not")
        # Handle quantifiers
        if "ForAll" in statement:
            parts = statement.split("ForAll")
            vars = parts[1].split(",")[0].strip("()")
            body = parts[1].split(",", 1)[1].strip()
            statement = f"ForAll([{vars}], {body})"
        elif "Exists" in statement:
            parts = statement.split("Exists")
            vars = parts[1].split(",")[0].strip("()")
            body = parts[1].split(",", 1)[1].strip()
            statement = f"Exists([{vars}], {body})"
        # Evaluate the statement
        z3_statements.append(eval(statement, vars_dict))
    return z3_statements

# convert statements to Z3
z3_statements = convert_to_z3(logical_statement)
st.write("##### Logical Statement:")
st.write(z3_statements)

# if st.button("SOLVE"):
#     # solve model using predicated logic with z3
#     st.write("##### Solutions:")
#     if mode_to_use == "Solve models":
#         solve(z3_statements)
#     elif mode_to_use == "Check Entailments":
#         if len(statement_entilment) > 0:
#             entailment = statement_entilment.replace("=>", ">>").replace("<=", "<<")
#             print(entailment)
    
    