# core/differentiator.py
from core.equation import Equation
from core.term import Term

def differentiate_term(term: Term) -> str:
    """Differentiate a single term."""
    return term.differentiate()

def differentiate_equation(terms: list, signs: list) -> str:
    """Differentiate a list of terms with signs."""
    equation = Equation()

    for index, term in enumerate(terms):
        sign = "+" if index == 0 else signs[index - 1]
        equation.add_signed_term(term, sign)

    return equation.differentiate()
