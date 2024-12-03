import stat

from sympy import Function, pprint, simplify, symbols, sympify
from sympy.logic.boolalg import And, Implies, simplify_logic
from sympy.logic.inference import satisfiable, valid
import z3


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


# from z3 import Int, And, Or, Not, Implies, Function, IntSort, BoolSort, ForAll, Exis

# # Define a function to parse and convert a string to a Z3 expression
# def z3_parse(expr_str):
#     # Define Z3 variables
#     x = Int('x')
#     G = Function('G', IntSort(), BoolSort())
#     H = Function('H', IntSort(), BoolSort())
#     M = Function('M', IntSort(), BoolSort())
    
#     # Replace logical operators in the string with Z3 functions
#     # expr_str = expr_str.replace(" & ", " And ")
#     # expr_str = expr_str.replace(" | ", " Or ")
#     # expr_str = expr_str.replace("=>", "Implies")
#     # expr_str = expr_str.replace("~", "Not")
    
#     # Use Python's eval() function to evaluate the string as a Z3 expression
#     expr = sympify(expr_str, {"x": x, "G": G, "H": H, "M": M, "And": And, "Or": Or, "Not": Not, "Implies": Implies})
#     return expr

# # Example usage
# expr_str = "H(x) => M(x)"
# z3_expr = z3_parse(expr_str)

# print(z3_expr)