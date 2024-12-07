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
    problem = Pls(propositions)
    if mode_to_use == "Solve models":
        solution = problem.solve()
        simplified_statements = problem.representation(simplify=True)
        st.write("##### Solutions:")
        if isinstance(solution, str):
            st.write(solution)
        else:
            st.dataframe(solution)

        expender = st.columns([3, 1])[0].expander("## Details")
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
                "✅ Tautology" if evaluted == r"\text{True}" else "🙅🏽 Impossible"
            )            
    elif mode_to_use == "Check Entailments":
        st.info("##### Vedict about entailment:")
        all_raw_statments = problem.representation()
        # col_result.latex(simplified_statements)
        if len(statement_entilment) > 0:
            entailment = statement_entilment.replace("=>", ">>").replace("<=", "<<")
            col_kb, col_entil, col_verdict = st.columns(
                [3, 1, 1], gap="small", vertical_alignment="top"
            )
            is_entilment = Pls.check_entailment(logical_statement, entailment)
            st.latex(all_raw_statments)
            if isinstance(is_entilment, str):
                st.latex(is_entilment)
                st.error("There is contraduction, beware of EXPLOSION")
            elif is_entilment:
                st.latex("\\models")
                st.latex(symbolize_expression(entailment)[0])
                st.success("Entailment is true")
            else:
                st.latex("\\not\\models")
                st.latex(symbolize_expression(entailment)[0])
                st.warning("Entailment is not true")

        else:
            st.warning("Please enter entailment")   
