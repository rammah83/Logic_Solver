from sympy import Symbol, Function, And, Or, Not, Implies
from sympy.core.expr import Expr

class ForAll(Expr):
    def __new__(cls, variable, formula):
        if not isinstance(variable, Symbol):
            raise TypeError("Variable must be a sympy.Symbol")
        if not isinstance(formula, Expr):
            raise TypeError("Formula must be a sympy expression")
        obj = super().__new__(cls, variable, formula)
        return obj

    @property
    def variable(self):
        return self.args[0]

    @property
    def formula(self):
        return self.args[1]

    def _sympystr(self, printer):
        return f"ForAll({printer._print(self.variable)}, {printer._print(self.formula)})"

class Exists(Expr):
    def __new__(cls, variable, formula):
        if not isinstance(variable, Symbol):
            raise TypeError("Variable must be a sympy.Symbol")
        if not isinstance(formula, Expr):
            raise TypeError("Formula must be a sympy expression")
        obj = super().__new__(cls, variable, formula)
        return obj

    @property
    def variable(self):
        return self.args[0]

    @property
    def formula(self):
        return self.args[1]

    def _sympystr(self, printer):
        return f"Exists({printer._print(self.variable)}, {printer._print(self.formula)})"

def string_to_fol(statement):
    """
    Converts a string representation of a First-Order Logic statement
    to a sympy-compatible symbolic expression.

    Supported elements:
    - Variables: e.g., 'x', 'y'
    - Predicates: e.g., 'p(x)', 'Q1(x, y)' (case-sensitive function names)
    - Logical connectives: '=>' (implies), '&' (and), '|' (or), '~' (not)
    - Quantifiers: 'ForAll(variable, formula)', 'Exists(variable, formula)'

    Example:
    string_to_fol("ForAll(x, p(x) => Q1(x))")
    """
    # 1. Basic String Cleaning and Preparation
    statement = statement.strip()

    # 2. Helper Function to Parse Predicates
    def parse_predicate(predicate_str):
        if '(' in predicate_str and predicate_str.endswith(')'):
            name = predicate_str[:predicate_str.index('(')]
            args_str = predicate_str[predicate_str.index('(') + 1:-1]
            args = [Symbol(arg.strip()) for arg in args_str.split(',') if arg.strip()]
            return Function(name)(*args)
        else:
            raise ValueError(f"Invalid predicate format: {predicate_str}")

    # 3. Recursive Parsing Function
    def parse_formula(formula_str):
        formula_str = formula_str.strip()

        # Handle Quantifiers
        if formula_str.startswith("ForAll("):
            content = formula_str[7:-1].strip()
            if ',' not in content:
                raise ValueError(f"Invalid ForAll syntax: {formula_str}")
            var_str, rest_formula_str = content.split(',', 1)
            variable = Symbol(var_str.strip())
            sub_formula = parse_formula(rest_formula_str)
            return ForAll(variable, sub_formula)
        elif formula_str.startswith("Exists("):
            content = formula_str[7:-1].strip()
            if ',' not in content:
                raise ValueError(f"Invalid Exists syntax: {formula_str}")
            var_str, rest_formula_str = content.split(',', 1)
            variable = Symbol(var_str.strip())
            sub_formula = parse_formula(rest_formula_str)
            return Exists(variable, sub_formula)

        # Handle Negation
        elif formula_str.startswith("~"):
            sub_formula = parse_formula(formula_str[1:].strip())
            return Not(sub_formula)

        # Handle Implications
        elif "=>" in formula_str:
            parts = [p.strip() for p in formula_str.split("=>", 1)]
            if len(parts) != 2:
                raise ValueError(f"Invalid implication syntax: {formula_str}")
            left = parse_formula(parts[0])
            right = parse_formula(parts[1])
            return Implies(left, right)

        # Handle And
        elif "&" in formula_str:
            parts = [parse_formula(p.strip()) for p in formula_str.split("&")]
            return And(*parts)

        # Handle Or
        elif "|" in formula_str:
            parts = [parse_formula(p.strip()) for p in formula_str.split("|")]
            return Or(*parts)

        # Handle Parentheses (for order of operations)
        elif formula_str.startswith("(") and formula_str.endswith(")"):
            return parse_formula(formula_str[1:-1])

        # Handle Predicates (or single symbols)
        elif '(' in formula_str:
            return parse_predicate(formula_str)
        else:
            return Symbol(formula_str)  # Could be a single variable

    return parse_formula(statement)

# Example Usage
statement = "ForAll(x, p(x) => Q1(x))"
sympified_statement = string_to_fol(statement)
print(f"Original statement: {statement}")
print(f"Sympified statement: {sympified_statement}")

statement2 = "Exists(y, R(y) & ~S(y))"
sympified_statement2 = string_to_fol(statement2)
print(f"Original statement: {statement2}")
print(f"Sympified statement: {sympified_statement2}")

statement3 = "(A | B) => C"
sympified_statement3 = string_to_fol(statement3)
print(f"Original statement: {statement3}")
print(f"Sympified statement: {sympified_statement3}")

statement4 = "P(a, b) & Q1(c)"
sympified_statement4 = string_to_fol(statement4)
print(f"Original statement: {statement4}")
print(f"Sympified statement: {sympified_statement4}")

# Example of nested quantifiers
statement5 = "ForAll(x, Exists(y, P(x, y)))"
sympified_statement5 = string_to_fol(statement5)
print(f"Original statement: {statement5}")
print(f"Sympified statement: {sympified_statement5}")

# Example with mixed connectives and quantifiers
statement6 = "ForAll(x, p(x) => Exists(y, Q1(x, y) & R(y)))"
sympified_statement6 = string_to_fol(statement6)
print(f"Original statement: {statement6}")
print(f"Sympified statement: {sympified_statement6}")