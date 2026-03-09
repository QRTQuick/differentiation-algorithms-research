import sympy as sp

from core.term import Term


class Equation:
    """Represents an equation composed of multiple terms."""

    def __init__(self):
        self.terms = []
        self.signs = []

    def add_term(self, term: Term):
        self.terms.append(term)

    def add_signed_term(self, term: Term, sign: str = "+"):
        if sign not in {"+", "-"}:
            raise ValueError("Use '+' or '-' to join terms.")

        if self.terms:
            self.signs.append(sign)
        elif sign == "-":
            term.coefficient *= -1

        self.terms.append(term)

    def remove_term(self, index: int):
        if index < 0 or index >= len(self.terms):
            raise IndexError("Term index out of range.")

        if len(self.terms) == 1:
            self.clear()
            return

        if index == 0:
            self.terms.pop(0)
            leading_sign = self.signs.pop(0)
            if leading_sign == "-":
                self.terms[0].coefficient *= -1
            return

        if index == len(self.terms) - 1:
            self.terms.pop(index)
            self.signs.pop()
            return

        self.terms.pop(index)
        self.signs[index - 1] = self.signs[index]
        self.signs.pop(index)

    def clear(self):
        self.terms.clear()
        self.signs.clear()

    def set_signs(self, signs):
        if isinstance(signs, str):
            parsed_signs = list(signs.replace(" ", ""))
        else:
            parsed_signs = list(signs)

        if any(sign not in {"+", "-"} for sign in parsed_signs):
            raise ValueError("Signs must only contain '+' or '-'.")

        expected = max(0, len(self.terms) - 1)
        if len(parsed_signs) != expected:
            raise ValueError(
                f"Expected {expected} sign(s) for {len(self.terms)} term(s), got {len(parsed_signs)}."
            )

        self.signs = parsed_signs

    def has_terms(self) -> bool:
        return bool(self.terms)

    def has_roots(self) -> bool:
        return any(term.root is not None for term in self.terms)

    def display_expression(self) -> str:
        return self._compose([term.display_expression() for term in self.terms])

    def display_expression_unicode(self) -> str:
        return self._compose([term.display_expression_unicode() for term in self.terms])

    def standard_expression(self) -> str:
        return self._compose([term.standard_expression() for term in self.terms])

    def standard_expression_unicode(self) -> str:
        return self._compose([term.standard_expression_unicode() for term in self.terms])

    def differentiate(self):
        """Differentiate all terms and return a simplified derivative string."""
        if not self.terms:
            raise ValueError("Add at least one term before differentiating.")

        expected = max(0, len(self.terms) - 1)
        if len(self.signs) != expected:
            raise ValueError("Equation structure is incomplete. Review the terms and signs.")

        derivatives = [term.differentiate() for term in self.terms]
        return self._compose(derivatives, drop_zero_terms=True)

    def differentiate_unicode(self) -> str:
        if not self.terms:
            raise ValueError("Add at least one term before differentiating.")

        expected = max(0, len(self.terms) - 1)
        if len(self.signs) != expected:
            raise ValueError("Equation structure is incomplete. Review the terms and signs.")

        derivatives = [term.differentiate_unicode() for term in self.terms]
        return self._compose(derivatives, drop_zero_terms=True)

    def to_sympy_expression(self):
        expression = sp.Integer(0)

        for index, term in enumerate(self.terms):
            term_expression = term.to_sympy_expression()
            if index == 0:
                expression += term_expression
                continue

            if self.signs[index - 1] == "+":
                expression += term_expression
            else:
                expression -= term_expression

        return sp.simplify(expression)

    def _compose(self, pieces, drop_zero_terms: bool = False) -> str:
        if not pieces:
            return "No terms added yet."

        composed_parts = []

        for index, piece in enumerate(pieces):
            sign = "+" if index == 0 else self.signs[index - 1]
            normalized_sign, normalized_piece = self._normalize_piece(sign, piece)

            if drop_zero_terms and normalized_piece == "0":
                continue

            composed_parts.append((normalized_sign, normalized_piece))

        if not composed_parts:
            return "0"

        first_sign, first_piece = composed_parts[0]
        result = first_piece if first_sign == "+" else f"-{first_piece}"

        for sign, piece in composed_parts[1:]:
            result += f" {sign} {piece}"

        return result

    @staticmethod
    def _normalize_piece(sign: str, piece: str):
        if piece.startswith("-"):
            return ("-" if sign == "+" else "+"), piece[1:]
        return sign, piece
