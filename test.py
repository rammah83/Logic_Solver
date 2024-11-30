import stat
from sympy import symbols, Function, sympify, pprint, simplify
from sympy.logic.boolalg import And, Implies, simplify_logic
from sympy.logic.inference import satisfiable, valid


def parse_logical_expression(expression):
    # Define the variable
    x = symbols("x")

    # Define the mapping for logical operators
    operator_mapping = {"&": "And", "=>": "Implies"}

    if "=>" in expression:
        expression.find("=>")
        logic_expr = Implies()

    # Parse the modified expression
    parsed_expression = sympify(expression)

    return parsed_expression


# Example usage
statement = "H(x) => M(x)"
terms = statement.split("=>")
logic_expr = Implies(terms[0], terms[1])
pprint(valid(logic_expr))
for model in satisfiable(logic_expr, all_models=True):
    if model:
        print(model)
