from dataclasses import dataclass, field
from fractions import Fraction

import sympy as sp


EPSILON = 1e-9
SUPERSCRIPT_TRANSLATION = str.maketrans(
    {
        "0": "⁰",
        "1": "¹",
        "2": "²",
        "3": "³",
        "4": "⁴",
        "5": "⁵",
        "6": "⁶",
        "7": "⁷",
        "8": "⁸",
        "9": "⁹",
        "-": "⁻",
        "/": "⁄",
        "(": "⁽",
        ")": "⁾",
    }
)


def _is_zero(value: float) -> bool:
    return abs(value) < EPSILON


def _is_integer(value: float) -> bool:
    return abs(value - round(value)) < EPSILON


def format_number(value: float) -> str:
    """Format numbers without trailing zero noise."""
    if _is_zero(value):
        return "0"
    if _is_integer(value):
        return str(int(round(value)))

    text = f"{value:.4f}".rstrip("0").rstrip(".")
    return text or "0"


def format_exponent(value: float) -> str:
    """Prefer fractions for clean power-rule output when possible."""
    if _is_zero(value):
        return "0"
    if _is_integer(value):
        return str(int(round(value)))

    fraction = Fraction(value).limit_denominator(24)
    if abs(float(fraction) - value) < EPSILON:
        return f"{fraction.numerator}/{fraction.denominator}"

    return f"{value:.4f}".rstrip("0").rstrip(".")


def _format_exponent_token(value: float) -> str:
    exponent = format_exponent(value)
    if "/" in exponent or exponent.startswith("-"):
        return f"({exponent})"
    return exponent


def format_variable_part(exponent: float) -> str:
    """Build the x-expression for a given exponent."""
    if _is_zero(exponent):
        return ""
    if abs(exponent - 1) < EPSILON:
        return "x"
    return f"x^{_format_exponent_token(exponent)}"


def _format_superscript(value: float) -> str:
    exponent = format_exponent(value)
    if "/" in exponent:
        exponent = f"({exponent})"
    return exponent.translate(SUPERSCRIPT_TRANSLATION)


def format_exponent_unicode(value: float) -> str:
    return _format_superscript(value)


def format_variable_part_unicode(exponent: float) -> str:
    if _is_zero(exponent):
        return ""
    if abs(exponent - 1) < EPSILON:
        return "x"
    return f"x{_format_superscript(exponent)}"


def _join_coefficient_and_body(coefficient: float, body: str) -> str:
    if not body:
        return format_number(coefficient)

    if abs(coefficient - 1) < EPSILON:
        return body
    if abs(coefficient + 1) < EPSILON:
        return f"-{body}"

    return f"{format_number(coefficient)}{body}"


def format_power_term(coefficient: float, exponent: float) -> str:
    return _join_coefficient_and_body(coefficient, format_variable_part(exponent))


def format_power_term_unicode(coefficient: float, exponent: float) -> str:
    return _join_coefficient_and_body(coefficient, format_variable_part_unicode(exponent))


@dataclass
class Term:
    """Represents a single term in an equation."""

    coefficient: float
    power: float = 1
    root: float | None = None
    derivative: str | None = field(default=None, init=False)

    def effective_power(self) -> float:
        if self.root is None:
            return self.power
        return self.power / self.root

    def standard_expression(self) -> str:
        return format_power_term(self.coefficient, self.effective_power())

    def standard_expression_unicode(self) -> str:
        return format_power_term_unicode(self.coefficient, self.effective_power())

    def display_expression(self) -> str:
        """Display the term in the same form used in the GUI builder."""
        if self.root is None:
            return format_power_term(self.coefficient, self.power)

        if _is_zero(self.power):
            return format_number(self.coefficient)

        if abs(self.root - 2) < EPSILON:
            radical_body = "sqrt(x)"
        elif abs(self.root - 3) < EPSILON:
            radical_body = "cbrt(x)"
        else:
            radical_body = f"root_{format_number(self.root)}(x)"

        if abs(self.power - 1) < EPSILON:
            return _join_coefficient_and_body(self.coefficient, radical_body)

        powered_body = f"({radical_body})^{_format_exponent_token(self.power)}"
        return _join_coefficient_and_body(self.coefficient, powered_body)

    def display_expression_unicode(self) -> str:
        if self.root is None:
            return format_power_term_unicode(self.coefficient, self.power)

        if _is_zero(self.power):
            return format_number(self.coefficient)

        if abs(self.root - 2) < EPSILON:
            radical_body = "√x"
        elif abs(self.root - 3) < EPSILON:
            radical_body = "∛x"
        else:
            radical_body = f"{format_number(self.root)}√x"

        if abs(self.power - 1) < EPSILON:
            return _join_coefficient_and_body(self.coefficient, radical_body)

        return _join_coefficient_and_body(self.coefficient, f"({radical_body}){_format_superscript(self.power)}")

    def differentiate(self) -> str:
        """Differentiate the term using the power rule."""
        derived_coefficient = self.coefficient * self.effective_power()
        if _is_zero(derived_coefficient):
            self.derivative = "0"
            return self.derivative

        derived_exponent = self.effective_power() - 1
        self.derivative = format_power_term(derived_coefficient, derived_exponent)
        return self.derivative

    def differentiate_unicode(self) -> str:
        derived_coefficient = self.coefficient * self.effective_power()
        if _is_zero(derived_coefficient):
            return "0"

        derived_exponent = self.effective_power() - 1
        return format_power_term_unicode(derived_coefficient, derived_exponent)

    def to_sympy_expression(self):
        x_symbol = sp.Symbol("x")
        coefficient = sp.nsimplify(self.coefficient)
        exponent = sp.nsimplify(self.effective_power())
        return sp.simplify(coefficient * x_symbol**exponent)
