from sympy import Function, Symbol, pprint, latex, simplify, simplify_logic, sympify
from sympy.logic import inference
import streamlit as st
from utils.logical_syllogism import symbolize_expression
from utils.logical_syllogism import PropositionalLogicSyllogism as Pls
from sympy.logic.boolalg import And, Not


# Define the Predicate class
class FOPredicate(Function):
    def __init__(self, name):
        self.name = name

    def __call__(self, *args):
        args_str = ",".join(map(str, args))
        return Symbol(f"{self.name}({args_str})")

    def __repr__(self) -> str:
        return f"{self.name}"

    def __str__(self) -> str:
        return f"{self.name}"


def compose_predicate_expr(statement):
    raw_str = (
        statement.replace("~", "")
        .replace(">>", "+")
        .replace("|", "+")
        .replace("&", "+")
    )
    raw_str = sympify(raw_str)
    funcs_names = set(f.name for f in raw_str.atoms(Function))
    vars_names = raw_str.atoms(Symbol)

    for func in funcs_names:
        exec(f"{func} = FOPredicate('{func}')")
    for var in vars_names:
        exec(f"{var} = Symbol('{var}', bool=True)")

    return simplify(eval(statement))


st.subheader("Propositional Logic is so :blue[cool] :sunglasses:")
with st.sidebar:
    mode_to_use = st.selectbox(
        "## Select Mode",
        options=["Solve models", "Check Entailments"],
        index=0,
    )

col_kb, col_entails = st.columns([1, 1], gap="small", vertical_alignment="bottom")
logical_statement = col_kb.text_area(
    "*Building Knwoledge Base (KB): _Logical Statement_*",
    help="use '>>' for 'implies', '&' for 'and', '|' for 'or', '~' for 'not': don't use E, I, O, N, S, Q",
    height=200,
)

statement_entilment = col_entails.text_input(
    "Conclusion to entile",
    help="use '>>' for 'implies', '&' for 'and', '|' for 'or', '~' for 'not': don't use E, I, O, N, S, Q",
    disabled=mode_to_use != "Check Entailments",
)

# propositions = [
#  Ex(g)
# "Ex(g) => (Op(g) &  Os(g) & Ob(g))
# (Ob(g) & Op(g) & Os(g)) => ~Ex(Ev)
# ~Ex(Ev)"
#                 ]
# st.write(propositions)

logical_statement = (
    logical_statement.replace("=>", ">>").replace("<=", "<<").split("\n")
)

# st.info(logical_statement)
used_atoms = set()
propositions = []
for statement in logical_statement:
    expr_simplified = compose_predicate_expr(statement)
    used_atoms |= expr_simplified.atoms()
    propositions.append(expr_simplified)
st.info(used_atoms)
if st.button("SOLVE"):
    st.info(propositions)
    global_statement = And(*propositions)
    simplified_statement = simplify_logic(global_statement)
    st.latex(latex(simplified_statement))
    st.write(isinstance(simplified_statement, And))
