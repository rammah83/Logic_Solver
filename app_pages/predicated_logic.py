
from z3 import *

def check_entailment(kb, conclusion):
    s = Solver()
    s.add(Not(conclusion))
    for statement in kb:
        s.add(statement)
    return s.check() == unsat

def solve_model(kb):
    s = Solver()
    for statement in kb:
        s.add(statement)
    if s.check() == sat:
        return s.model()
    else:
        return None

def parse_expression(expr):
    # This function will parse the logical expressions from string to z3 expressions
    if '->' in expr:
        left, right = expr.split('->')
        return Implies(parse_expression(left.strip()), parse_expression(right.strip()))
    elif '<-' in expr:
        left, right = expr.split('<-')
        return Implies(parse_expression(right.strip()), parse_expression(left.strip()))
    elif 'and' in expr:
        parts = expr.split('and')
        return And(*[parse_expression(part.strip()) for part in parts])
    elif 'or' in expr:
        parts = expr.split('or')
        return Or(*[parse_expression(part.strip()) for part in parts])
    elif 'not' in expr:
        return Not(parse_expression(expr.replace('not', '').strip()))
    elif expr.startswith('forall'):
        var, inner_expr = expr[6:].split('.', 1)
        return ForAll([Symbol(var.strip())], parse_expression(inner_expr.strip()))
    elif expr.startswith('exists'):
        var, inner_expr = expr[6:].split('.', 1)
        return Exists([Symbol(var.strip())], parse_expression(inner_expr.strip()))
    else:
        # Assume the expression is a predicate
        return Symbol(expr.strip())

def main():
    import streamlit as st

    st.subheader("First-Order Predicate Logic")
    with st.sidebar:
        mode_to_use = st.selectbox(
            "## Select Mode",
            options=["Solve models", "Check Entailments"],
            index=0,
        )

    col_kb, col_entails = st.columns([1, 1], gap="small")
    logical_statement = col_kb.text_area(
        "*Building Knowledge Base (KB): _Logical Statement_*",
        help="Use predicates and logical connectives.",
        height=200,
    )

    statement_entailment = col_entails.text_input(
        "Conclusion to entail",
        help="Use predicates and logical connectives.",
        disabled=mode_to_use != "Check Entailments",
    )

    if st.button("SOLVE"):
        kb = []
        for stmt in logical_statement.split('\n'):
            if stmt.strip():
                kb.append(parse_expression(stmt.strip()))

        if mode_to_use == "Solve models":
            model = solve_model(kb)
            if model:
                st.write("#### Model:")
                st.write(model)
            else:
                st.write("No model found.")

        elif mode_to_use == "Check Entailments":
            if statement_entailment:
                conclusion = parse_expression(statement_entailment.strip())
                is_entailment = check_entailment(kb, conclusion)
                if is_entailment:
                    st.success("Entailment is true")
                else:
                    st.warning("Entailment is not true")
            else:
                st.warning("Please enter entailment")


main()
