import sympy as sp

from sympy.logic.boolalg import And, Not
from sympy.logic import inference


class PropositionalLogicSyllogism:
    """Docstring for PropositionalLogicSyllogism

    :var global_statement: Description
    :vartype global_statement: None
    :var simplified_statement: Description
    :vartype simplified_statement: None"""

    global_statement = None
    simplified_statement = None

    def __init__(self, propositions):
        # check if proposition symbols are sympy symbols compatible
        if not all([isinstance(prop, sp.Symbol) for prop in propositions]):
            self.propositions = propositions
            self.global_statement = And(*sp.sympify(self.propositions))
            self.simplified_statement = sp.simplify_logic(
                self.global_statement, force=False
            )
        else:
            raise ValueError("Propositions must be sympy symbols")

        # display(self.global_statement, "<=>", self.simplified_statement)
        # print("---"*50)
        # display(list(inference.satisfiable(self.simplified_statement, all_models=True)))

    def representation(self, simplify=False):
        if simplify:
            return sp.latex(self.simplified_statement)
        else:
            return sp.latex(self.global_statement)

    @property
    def symbols(self):
        return self.global_statement.atoms() | self.global_statement.free_symbols

    def solve(self, negate=False):
        """sumary_line

        Keyword arguments:
        argument -- description
        Return: return_description
        """

        statement = (
            Not(self.simplified_statement)
            if negate
            else self.simplified_statement.copy()
        )
        # check if all possible assignments are valid
        if inference.valid(statement):
            return "Tautology: Valid in all Possible Worlds ✅"

        models = list(inference.satisfiable(statement, algorithm=None, all_models=True))
        if not any(models):
            return "Invalid in all Possible Worlds: contraduction 🙅🏽"
        n_worlds = f"{len(models)} world{'s' if len(models) > 1 else ''}"
        print(f"Valid in {n_worlds}: satifiable")
        return [model for model in models]

    @staticmethod
    def check_entailment(premises, conclusion) -> bool | str:
        """_summary_

        Args:
            premises (_type_): _description_
            conclusion (_type_): _description_

        Returns:
            bool | str: _description_
        """
        # print(sp.sympify(premises, evaluate=True))
        know_base: inference.PropKB = inference.PropKB()
        [know_base.tell(premise) for premise in sp.sympify(premises)]
        print(f"{premises} ⊨ {conclusion} is:")
        if not sp.simplify_logic(And(*sp.sympify(premises))):
            return "Invalid Premises: Contradiction"
        return know_base.ask(conclusion)


def symbolize_expression(statement):
    try:
        statement = sp.sympify(statement)
    except Exception as e:
        print(f"Error: {e}")
        return (None, None)
    else:
        return (sp.latex(statement), sp.latex(sp.simplify_logic(statement, force=True)))


def print_satisfaible_worlds(valid_worlds: dict | str) -> None:
    if isinstance(valid_worlds, str):
        print(valid_worlds)
        return
    print("-------logic is satisfiable in some possible worlds--------")
    for k in sorted(valid_worlds[0].keys(), key=lambda x: str(x)):
        print(f"{str(k):^10}", end="")
    print("\n", f"{'-'*9*len(valid_worlds[0])}")
    for world in valid_worlds:
        world = dict(sorted(world.items(), key=lambda x: str(x)))
        for value in world.values():
            print(f"{value:^10}", end="")
        print()


if __name__ == "__main__":
    propositions = [
        "G & ~Ev",
        "~Ev",
        "~G >> R",
        "~C & D >> G",
        "G >> ~R",
    ]

    problem = PropositionalLogicSyllogism(propositions)
    sp.pprint(problem.representation(simplify=True))
    valid_worlds: list[dict] = problem.solve(negate=False)
    sp.pprint(valid_worlds)
    print_satisfaible_worlds(valid_worlds)
