"""
This module defines the FOPredicate class and a function to compose predicate expressions.
"""

from sympy import Function, Symbol, simplify, symbols, sympify, pprint


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

if __name__ == "__main__":
    STATEMENT = "P(x) & Qi(x) >> R(x)"
    pprint(compose_predicate_expr(STATEMENT))
    
