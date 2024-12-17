"""
A new module for first-order logic within sympy.logic.

This module introduces classes and functions to represent and manipulate 
first-order logic (FOL) constructs, including predicates, quantifiers, 
and functions. It is a starting point and may be extended for unification, 
theorem proving, and model checking.
"""

from sympy.core.symbol import Symbol
from sympy import sympify
from sympy.logic.boolalg import BooleanFunction

class Term:
    """Abstract base class for FOL terms (variables, constants, functions)."""
    def __new__(cls, *args, **kwargs):
        if cls is Term:
            raise TypeError("Term is an abstract class.")
        return object.__new__(cls)

class Variable(Term):
    """A variable in first-order logic."""
    __slots__ = ['name']
    def __init__(self, name):
        self.name = str(name)
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name
    def free_variables(self):
        return {self}

class Constant(Term):
    """A constant symbol."""
    __slots__ = ['name']
    def __init__(self, name):
        self.name = str(name)
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return isinstance(other, Constant) and self.name == other.name
    def free_variables(self):
        return set()

class Function(Term):
    """A function symbol with given arity."""
    __slots__ = ['name', 'args']
    def __init__(self, name, *args):
        self.name = str(name)
        self.args = args
    def __repr__(self):
        return f"{self.name}({', '.join(map(repr, self.args))})"
    def __eq__(self, other):
        return (isinstance(other, Function) and
                self.name == other.name and self.args == other.args)
    def free_variables(self):
        fvars = set()
        for arg in self.args:
            fvars |= arg.free_variables()
        return fvars

class Predicate(BooleanFunction):
    """A predicate symbol, extending BooleanFunction for logical predicates."""
    def __new__(cls, name, *args):
        # Ensure args are sympifiable
        sympy_args = [arg if isinstance(arg, Variable) else sympify(arg) for arg in args]
        obj = BooleanFunction.__new__(cls, *sympy_args)
        obj.name = str(name)
        return obj
    def __repr__(self):
        return f"{self.name}({', '.join(map(repr, self.args))})"
    def free_variables(self):
        fvars = set()
        for arg in self.args:
            if hasattr(arg, 'free_variables'):
                fvars |= arg.free_variables()
        return fvars

class Quantifier(BooleanFunction):
    """Abstract base class for quantifiers."""
    def __new__(cls, var, formula):
        if cls is Quantifier:
            raise TypeError("Quantifier is an abstract class.")
        return BooleanFunction.__new__(cls, var, formula)

    @property
    def variable(self):
        return self.args[0]

    @property
    def formula(self):
        return self.args[1]

    def free_variables(self):
        return self.formula.free_variables() - {self.variable}

class ForAll(Quantifier):
    """Universal quantification: ∀x φ."""
    def __repr__(self):
        return f"ForAll({self.variable}, {self.formula})"

class Exists(Quantifier):
    """Existential quantification: ∃x φ."""
    def __repr__(self):
        return f"Exists({self.variable}, {self.formula})"

def substitute(expr, var, term):
    """Substitute occurrences of var in expr with term."""
    if isinstance(expr, Variable):
        return term if expr == var else expr
    elif isinstance(expr, Constant):
        return expr
    elif isinstance(expr, Function):
        return Function(expr.name, *[substitute(arg, var, term) for arg in expr.args])
    elif isinstance(expr, Predicate):
        return Predicate(expr.name, *[substitute(arg, var, term) for arg in expr.args])
    elif isinstance(expr, Quantifier):
        # Avoid variable capture
        if expr.variable == var:
            # The bound variable shadows var, no substitution inside
            return expr
        else:
            return type(expr)(expr.variable, substitute(expr.formula, var, term))
    else:
        return expr

# Additional functionalities (e.g., Skolemization, Prenex normal form, 
# Unification) can be added here as needed.

if __name__ == "__main__":
    # Example tests and usage of the first-order logic module.

    # Create some variables
    x = Variable('x')
    y = Variable('y')
    z = Variable('z')

    # Create some constants
    a = Constant('a')
    b = Constant('b')

    # Create function symbols
    f = Function('f', x, a)
    g = Function('g', y, b)

    # Create predicates
    P = Predicate('P', x, f)
    Qe = Predicate('Qe', y, g)

    # Test representation
    print("Variables and constants:")
    print("x:", x)
    print("a:", a)
    print("f(x,a):", f)

    print("\nPredicates:")
    print("P(x,f(x,a)):", P)
    print("Qe(y,g(y,b)):", Qe)

    # Create quantified formulas
    phi = ForAll(x, P)       # ∀x P(x,f(x,a))
    psi = Exists(y, Qe)       # ∃y Q(y,g(y,b))

    print("\nQuantified Formulas:")
    print("ForAll(x, P(x,f(x,a))):", phi)
    print("Exists(y, Qe(y,g(y,b))):", psi)

    # Free variables tests
    print("\nFree variables:")
    print("Free vars in P:", P.free_variables())
    print("Free vars in Q:", Qe.free_variables())
    print("Free vars in ForAll(x, P(x,f(x,a))):", phi.free_variables())
    print("Free vars in Exists(y, Qe(y,g(y,b))):", psi.free_variables())

    # Substitution example
    print("\nSubstitution:")
    # Substitute x with a constant b in P(x,f(x,a))
    P_sub = substitute(P, x, b)
    print("Substitute x with b in P(x,f(x,a)):", P_sub)

    # Substitution inside a quantifier
    phi_sub = substitute(phi, x, b)  # Since x is bound in phi, no change expected
    print("Substitute x with b in ForAll(x, P(x,f(x,a))):", phi_sub)

    # Another substitution
    phi_new = ForAll(y, P)   # ∀y P(x,f(x,a)) – here x is free, y is bound
    phi_new_sub = substitute(phi_new, x, a)
    print("Substitute x with a in ForAll(y, P(x,f(x,a))):", phi_new_sub)
