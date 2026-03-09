import re

import sympy as sp
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

from core.equation import Equation
from core.term import EPSILON, Term, format_exponent, format_exponent_unicode, format_number
from .input_widgets import TermInputWidget
from .result_widgets import ResultDisplayWidget, ScrollableValueBox


def _is_zero(value: float) -> bool:
    return abs(value) < EPSILON


def _join_coefficient_and_body(coefficient: float, body: str, formatter=format_number) -> str:
    if _is_zero(coefficient):
        return "0"

    if not body:
        return formatter(coefficient)

    if abs(coefficient - 1) < EPSILON:
        return body
    if abs(coefficient + 1) < EPSILON:
        return f"-{body}"

    return f"{formatter(coefficient)}{body}"


def _power_body(base_text: str, exponent: float) -> str:
    exponent_text = format_exponent(exponent)
    if base_text == "x":
        if exponent_text == "1":
            return "x"
        return f"x^({exponent_text})" if "/" in exponent_text or exponent_text.startswith("-") else f"x^{exponent_text}"

    return f"({base_text})^({exponent_text})"


def _power_body_unicode(base_text: str, exponent: float) -> str:
    exponent_text = format_exponent_unicode(exponent)
    if base_text == "x":
        return "x" if abs(exponent - 1) < EPSILON else f"x{exponent_text}"
    return f"({base_text}){exponent_text}"


def _format_linear_expression(variable_coefficient: float, constant: float) -> str:
    parts = []

    if not _is_zero(variable_coefficient):
        if abs(variable_coefficient - 1) < EPSILON:
            parts.append("x")
        elif abs(variable_coefficient + 1) < EPSILON:
            parts.append("-x")
        else:
            parts.append(f"{format_number(variable_coefficient)}x")

    if not _is_zero(constant):
        constant_text = format_number(abs(constant))
        if parts:
            sign = "+" if constant > 0 else "-"
            parts.append(f"{sign} {constant_text}")
        else:
            parts.append(format_number(constant))

    return " ".join(parts) if parts else "0"


def _combine_with_constant(head_expression: str, constant: float) -> str:
    if _is_zero(constant):
        return head_expression

    constant_text = format_number(abs(constant))
    sign = "+" if constant > 0 else "-"

    if not head_expression:
        return format_number(constant)

    return f"{head_expression} {sign} {constant_text}"


def _radical_name(root_degree: int) -> str:
    if root_degree == 2:
        return "sqrt"
    if root_degree == 3:
        return "cbrt"
    return f"root_{root_degree}"


PARSER_TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


def _create_scroll_column():
    scroll_area = QScrollArea()
    scroll_area.setObjectName("ColumnScrollArea")
    scroll_area.setWidgetResizable(True)
    scroll_area.setFrameShape(QFrame.NoFrame)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    container = QWidget()
    container.setObjectName("ScrollColumn")

    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(22)
    layout.setAlignment(Qt.AlignTop)

    scroll_area.setWidget(container)
    return scroll_area, layout


def _pretty_math_text(expression, label: str | None = None) -> str:
    pretty = sp.pretty(sp.simplify(expression), use_unicode=True, wrap_line=False)
    if label is None:
        return pretty
    if "\n" in pretty:
        return f"{label} =\n{pretty}"
    return f"{label} = {pretty}"


def _radical_sympy_expression(inputs):
    x_symbol = sp.Symbol("x")
    root_degree = inputs["root_degree"]
    outer_coefficient = sp.nsimplify(inputs["outer_coefficient"])
    inner_x_coefficient = sp.nsimplify(inputs["inner_x_coefficient"])
    inner_constant = sp.nsimplify(inputs["inner_constant"])
    outer_constant = sp.nsimplify(inputs["outer_constant"])

    inner_expression = inner_x_coefficient * x_symbol + inner_constant
    equation = sp.simplify(outer_coefficient * inner_expression ** sp.Rational(1, root_degree) + outer_constant)
    derivative = sp.simplify(sp.diff(equation, x_symbol))
    return equation, derivative


def _normalize_expression_text(text: str) -> str:
    normalized = text.strip()
    normalized = normalized.replace("−", "-").replace("×", "*").replace("÷", "/")
    normalized = re.sub(r"^\s*y\s*=\s*", "", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"∛\s*\(([^()]*)\)", r"cbrt(\1)", normalized)
    normalized = re.sub(r"∛\s*([A-Za-z0-9_]+)", r"cbrt(\1)", normalized)
    normalized = re.sub(r"√\s*\(([^()]*)\)", r"sqrt(\1)", normalized)
    normalized = re.sub(r"√\s*([A-Za-z0-9_]+)", r"sqrt(\1)", normalized)
    return normalized


def _parse_mixed_expression(text: str):
    normalized = _normalize_expression_text(text)
    if not normalized:
        raise ValueError("Enter an expression before differentiating.")

    x_symbol = sp.Symbol("x")
    expression = parse_expr(
        normalized,
        transformations=PARSER_TRANSFORMATIONS,
        local_dict={
            "x": x_symbol,
            "sqrt": sp.sqrt,
            "cbrt": lambda value: sp.Pow(value, sp.Rational(1, 3)),
        },
        evaluate=True,
    )

    invalid_symbols = expression.free_symbols - {x_symbol}
    if invalid_symbols:
        raise ValueError("Only the variable x is supported in this tab.")

    return normalized, sp.simplify(expression), x_symbol


class PolynomialWorkspace(QWidget):
    status_message = Signal(str, int)
    workspace_title = "Polynomial"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.equation = Equation()
        self._build_ui()
        self._refresh_equation_view()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        left_scroll, left_column = _create_scroll_column()
        right_scroll, right_column = _create_scroll_column()
        layout.addWidget(left_scroll, 4)
        layout.addWidget(right_scroll, 6)

        left_column.addWidget(self._build_builder_card())
        left_column.addWidget(self._build_examples_card())
        right_column.addWidget(self._build_workspace_card(), 5)

        self.result_widget = ResultDisplayWidget()
        right_column.addWidget(self.result_widget, 4)
        left_column.addStretch()
        right_column.addStretch()

    def _build_builder_card(self):
        card, layout = self._create_card(
            "Polynomial builder",
            "Compose multiple polynomial terms one by one. The app tracks signs automatically so the final equation stays consistent.",
        )

        self.term_input = TermInputWidget()
        self.term_input.coeff_input.returnPressed.connect(self.add_term)
        self.term_input.power_input.returnPressed.connect(self.add_term)
        layout.addWidget(self.term_input)

        button_row = QHBoxLayout()
        button_row.setSpacing(12)

        self.add_term_btn = QPushButton("Add Polynomial Term")
        self.add_term_btn.setObjectName("PrimaryButton")
        self.add_term_btn.clicked.connect(self.add_term)

        self.reset_form_btn = QPushButton("Reset Fields")
        self.reset_form_btn.setObjectName("SecondaryButton")
        self.reset_form_btn.clicked.connect(self.reset_term_builder)

        button_row.addWidget(self.add_term_btn)
        button_row.addWidget(self.reset_form_btn)
        layout.addLayout(button_row)

        helper_text = QLabel(
            "Use negative powers for reciprocal terms and power 0 for constants. Each term should be in the form ax^n."
        )
        helper_text.setObjectName("MutedText")
        helper_text.setWordWrap(True)
        layout.addWidget(helper_text)
        return card

    def _build_examples_card(self):
        card, layout = self._create_card(
            "Quick examples",
            "Load a sample equation to test the interface faster.",
        )

        example_row = QHBoxLayout()
        example_row.setSpacing(10)

        sample_one = QPushButton("Load x⁴ + 3x² − 7")
        sample_one.setObjectName("SecondaryButton")
        sample_one.clicked.connect(lambda: self._load_example([(Term(1, 4), "+"), (Term(3, 2), "+"), (Term(7, 0), "-")]))

        sample_two = QPushButton("Load 2x³ − x + 5")
        sample_two.setObjectName("SecondaryButton")
        sample_two.clicked.connect(lambda: self._load_example([(Term(2, 3), "+"), (Term(1, 1), "-"), (Term(5, 0), "+")]))

        example_row.addWidget(sample_one)
        example_row.addWidget(sample_two)
        layout.addLayout(example_row)

        note = QLabel("Polynomial mode is best for equations like y = 4x³ − 2x + 1.")
        note.setObjectName("MutedText")
        note.setWordWrap(True)
        layout.addWidget(note)
        return card

    def _build_workspace_card(self):
        card, layout = self._create_card(
            "Workspace",
            "Review the current equation and manage the term list before differentiating.",
        )

        preview_title = QLabel("Equation preview")
        preview_title.setObjectName("SectionLabel")
        self.equation_preview = ScrollableValueBox("PreviewValue")
        self.equation_preview.setMaximumHeight(110)
        self.equation_preview.set_value("No terms added yet.")

        self.term_list = QListWidget()
        self.term_list.setObjectName("TermList")
        self.term_list.setMinimumHeight(220)
        self.term_list.itemSelectionChanged.connect(self._update_action_state)

        action_row = QHBoxLayout()
        action_row.setSpacing(12)

        self.remove_term_btn = QPushButton("Remove Selected")
        self.remove_term_btn.setObjectName("SecondaryButton")
        self.remove_term_btn.clicked.connect(self.remove_selected_term)

        self.clear_btn = QPushButton("Clear Equation")
        self.clear_btn.setObjectName("DangerButton")
        self.clear_btn.clicked.connect(self.clear_equation)

        self.differentiate_btn = QPushButton("Differentiate Polynomial")
        self.differentiate_btn.setObjectName("PrimaryButton")
        self.differentiate_btn.clicked.connect(self.show_derivative)

        action_row.addWidget(self.remove_term_btn)
        action_row.addWidget(self.clear_btn)
        action_row.addStretch()
        action_row.addWidget(self.differentiate_btn)

        layout.addWidget(preview_title)
        layout.addWidget(self.equation_preview)
        layout.addWidget(self.term_list, 1)
        layout.addLayout(action_row)
        return card

    def _create_card(self, title_text: str, subtitle_text: str):
        card = QFrame()
        card.setObjectName("Card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(16)

        title = QLabel(title_text)
        title.setObjectName("CardTitle")
        subtitle = QLabel(subtitle_text)
        subtitle.setObjectName("MutedText")
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        return card, layout

    def add_term(self):
        try:
            sign, coefficient, power, root = self.term_input.get_term_data()
            term = Term(coefficient, power, root)
            self.equation.add_signed_term(term, sign)
        except ValueError as error:
            QMessageBox.warning(self, "Invalid term", str(error))
            return

        self._refresh_equation_view(reset_result=True)
        self.term_input.clear_inputs()
        self.term_input.focus_coefficient()
        self.status_message.emit(f"Added polynomial term: {term.display_expression_unicode()}", 4000)

    def reset_term_builder(self):
        self.term_input.clear_inputs()
        self.term_input.focus_coefficient()
        self.status_message.emit("Polynomial term form reset.", 3000)

    def remove_selected_term(self):
        selected_row = self.term_list.currentRow()
        if selected_row < 0:
            QMessageBox.information(self, "Select a term", "Choose a term before removing it.")
            return

        removed_term = self.equation.terms[selected_row].display_expression_unicode()
        self.equation.remove_term(selected_row)
        self._refresh_equation_view(reset_result=True)
        self.status_message.emit(f"Removed polynomial term: {removed_term}", 4000)

    def clear_equation(self):
        if not self.equation.has_terms():
            return

        self.equation.clear()
        self._refresh_equation_view(reset_result=True)
        self.status_message.emit("Polynomial equation cleared.", 4000)

    def show_derivative(self):
        try:
            derivative = self.equation.differentiate()
        except ValueError as error:
            QMessageBox.warning(self, "Cannot differentiate", str(error))
            return

        self.result_widget.set_result(
            _pretty_math_text(self.equation.to_sympy_expression(), "y"),
            f"y = {self.equation.standard_expression_unicode()}",
            f"y′ = {self.equation.differentiate_unicode()}",
            self.equation.has_roots(),
            "Polynomial mode applies the power rule term by term with clearer symbols for powers and roots.",
        )
        self.status_message.emit("Polynomial derivative updated.", 4000)

    def _load_example(self, term_specs):
        self.equation.clear()
        for term, sign in term_specs:
            self.equation.add_signed_term(term, sign)

        self._refresh_equation_view(reset_result=True)
        self.show_derivative()
        self.status_message.emit("Polynomial example loaded.", 4000)

    def _refresh_equation_view(self, reset_result: bool = False):
        self.term_list.clear()

        if self.equation.has_terms():
            for index, term in enumerate(self.equation.terms):
                prefix = "" if index == 0 else f"{self.equation.signs[index - 1]} "
                self.term_list.addItem(f"{prefix}{term.display_expression_unicode()}")

            self.equation_preview.set_value(f"y = {self.equation.display_expression_unicode()}")
        else:
            self.equation_preview.set_value("No terms added yet.")

        self.term_input.set_first_term_mode(not self.equation.has_terms())
        self._update_action_state()

        if reset_result:
            self.result_widget.clear_result()

    def _update_action_state(self):
        has_terms = self.equation.has_terms()
        has_selection = self.term_list.currentRow() >= 0

        self.remove_term_btn.setEnabled(has_selection)
        self.clear_btn.setEnabled(has_terms)
        self.differentiate_btn.setEnabled(has_terms)

    def solve_workspace(self):
        self.show_derivative()

    def reset_workspace(self):
        self.clear_equation()
        self.reset_term_builder()
        self.result_widget.clear_result()


class ExpressionWorkspace(QWidget):
    status_message = Signal(str, int)
    workspace_title = "Expressions"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self._reset_preview()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        left_scroll, left_column = _create_scroll_column()
        right_scroll, right_column = _create_scroll_column()
        layout.addWidget(left_scroll, 4)
        layout.addWidget(right_scroll, 6)

        left_column.addWidget(self._build_builder_card())
        left_column.addWidget(self._build_examples_card())
        right_column.addWidget(self._build_preview_card(), 4)

        self.result_widget = ResultDisplayWidget()
        self.result_widget.set_section_titles(
            "Expression entered",
            "Normalized interpretation",
            "Derivative",
        )
        right_column.addWidget(self.result_widget, 5)
        left_column.addStretch()
        right_column.addStretch()

    def _build_builder_card(self):
        card, layout = self._create_card(
            "Mixed expression builder",
            "Use this tab for worksheet-style expressions that combine roots, reciprocal powers, and shifted terms.",
        )

        self.expression_input = QTextEdit()
        self.expression_input.setObjectName("ExpressionInput")
        self.expression_input.setPlaceholderText(
            "Examples:\n"
            "√x − 3\n"
            "∛(x + 2)\n"
            "4*x - 1/x^2\n"
            "(x - 1)^5\n"
            "2*x^4 + √x"
        )
        self.expression_input.setMinimumHeight(120)
        self.expression_input.setMaximumHeight(180)
        self.expression_input.textChanged.connect(self._update_preview)
        layout.addWidget(self.expression_input)

        button_row = QHBoxLayout()
        button_row.setSpacing(12)

        self.solve_expression_btn = QPushButton("Differentiate Expression")
        self.solve_expression_btn.setObjectName("PrimaryButton")
        self.solve_expression_btn.clicked.connect(self.solve_expression)

        self.reset_expression_btn = QPushButton("Reset Fields")
        self.reset_expression_btn.setObjectName("SecondaryButton")
        self.reset_expression_btn.clicked.connect(self.reset_expression)

        button_row.addWidget(self.solve_expression_btn)
        button_row.addWidget(self.reset_expression_btn)
        layout.addLayout(button_row)

        helper_text = QLabel(
            "You can type ^ or ** for powers, sqrt(...) for square root, cbrt(...) for cube root, or even paste symbols like √x and ∛(x + 2)."
        )
        helper_text.setObjectName("MutedText")
        helper_text.setWordWrap(True)
        layout.addWidget(helper_text)
        return card

    def _build_examples_card(self):
        card, layout = self._create_card(
            "Examples from the worksheet style",
            "These examples are broader than the structured polynomial and root tabs.",
        )

        example_texts = (
            "sqrt(x) - 3",
            "cbrt(x + 2)",
            "4*x - 1/x^2",
            "sqrt(x) - x^2",
            "(x - 1)^5",
            "2*x^4 + sqrt(x)",
        )

        for example_text in example_texts:
            display_text = (
                example_text.replace("sqrt", "√")
                .replace("cbrt", "∛")
                .replace(" - ", " − ")
                .replace("^4", "⁴")
                .replace("^2", "²")
            )
            button = QPushButton(f"Load {display_text}")
            button.setObjectName("SecondaryButton")
            button.clicked.connect(lambda checked=False, text=example_text: self._load_example(text))
            layout.addWidget(button)

        note = QLabel(
            "This mode uses a symbolic parser, so it can handle many worksheet forms that the guided tabs intentionally simplify."
        )
        note.setObjectName("MutedText")
        note.setWordWrap(True)
        layout.addWidget(note)
        return card

    def _build_preview_card(self):
        card, layout = self._create_card(
            "Parser preview",
            "This shows the normalized expression the app will differentiate before you run the final step.",
        )

        self.normalized_preview = ScrollableValueBox("PreviewValue")
        self.normalized_preview.setMaximumHeight(110)

        self.interpreted_preview = ScrollableValueBox("PreviewValue")
        self.interpreted_preview.setMaximumHeight(110)

        self.preview_note = QLabel()
        self.preview_note.setObjectName("MutedText")
        self.preview_note.setWordWrap(True)

        layout.addWidget(QLabel("Typed expression"))
        layout.addWidget(self.normalized_preview)
        layout.addWidget(QLabel("Normalized interpretation"))
        layout.addWidget(self.interpreted_preview)
        layout.addWidget(self.preview_note)
        layout.addStretch()
        return card

    def _create_card(self, title_text: str, subtitle_text: str):
        card = QFrame()
        card.setObjectName("Card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(16)

        title = QLabel(title_text)
        title.setObjectName("CardTitle")
        subtitle = QLabel(subtitle_text)
        subtitle.setObjectName("MutedText")
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        return card, layout

    def _load_example(self, expression_text: str):
        self.expression_input.setPlainText(expression_text)
        self.solve_expression()
        self.status_message.emit("Mixed expression example loaded.", 4000)

    def _reset_preview(self):
        self.normalized_preview.set_value("Type or paste an expression to preview it here.")
        self.interpreted_preview.set_value("The normalized interpretation will appear here.")
        self.preview_note.setText("Use x as the variable. Constants, roots, shifted powers, and reciprocal powers are supported.")

    def reset_expression(self):
        self.expression_input.clear()
        self.result_widget.clear_result()
        self._reset_preview()
        self.status_message.emit("Mixed expression form reset.", 3000)

    def _update_preview(self):
        raw_text = self.expression_input.toPlainText()
        if not raw_text.strip():
            self._reset_preview()
            return

        try:
            normalized_text, expression, _ = _parse_mixed_expression(raw_text)
        except Exception:
            self.normalized_preview.set_value("The expression could not be parsed yet.")
            self.interpreted_preview.set_value("Check brackets, powers, and root syntax.")
            self.preview_note.setText("Examples: sqrt(x) - 3, cbrt(x + 2), 4*x - 1/x^2, (x - 1)^5")
            return

        self.normalized_preview.set_value(f"y = {normalized_text}")
        self.interpreted_preview.set_value(_pretty_math_text(expression, "y"))
        self.preview_note.setText("The parser has recognized the expression and converted it into mathematical symbols.")

    def solve_expression(self):
        try:
            normalized_text, expression, x_symbol = _parse_mixed_expression(self.expression_input.toPlainText())
        except Exception as error:
            QMessageBox.warning(self, "Invalid expression", str(error))
            return

        derivative = sp.simplify(sp.diff(expression, x_symbol))
        self.result_widget.set_result(
            f"y = {normalized_text}",
            _pretty_math_text(expression, "y"),
            _pretty_math_text(derivative, "y′"),
            True,
            "Mixed expression mode uses SymPy to render real mathematical symbols for radicals, powers, and derivatives.",
        )
        self.status_message.emit("Mixed expression derivative updated.", 4000)

    def solve_workspace(self):
        self.solve_expression()

    def reset_workspace(self):
        self.reset_expression()


class RadicalWorkspace(QWidget):
    status_message = Signal(str, int)
    workspace_title = "Roots"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self._set_default_inputs()
        self._update_preview()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        left_scroll, left_column = _create_scroll_column()
        right_scroll, right_column = _create_scroll_column()
        layout.addWidget(left_scroll, 4)
        layout.addWidget(right_scroll, 6)

        left_column.addWidget(self._build_builder_card())
        left_column.addWidget(self._build_examples_card())
        right_column.addWidget(self._build_preview_card(), 4)

        self.result_widget = ResultDisplayWidget()
        right_column.addWidget(self.result_widget, 5)
        left_column.addStretch()
        right_column.addStretch()

    def _build_builder_card(self):
        card, layout = self._create_card(
            "Root equation builder",
            "Build equations around square roots and cube roots of a linear expression. This covers examples like y = sqrt(x) - 3 and y = cbrt(x + 2).",
        )

        form_layout = QFormLayout()
        form_layout.setSpacing(14)
        layout.addLayout(form_layout)

        validator = QDoubleValidator(-999999.0, 999999.0, 4, self)

        self.root_selector = QComboBox()
        self.root_selector.addItem("Square root", 2)
        self.root_selector.addItem("Cube root", 3)

        self.outer_coefficient_input = QLineEdit()
        self.outer_coefficient_input.setValidator(validator)
        self.outer_coefficient_input.setPlaceholderText("Default 1")

        self.inner_x_coefficient_input = QLineEdit()
        self.inner_x_coefficient_input.setValidator(validator)
        self.inner_x_coefficient_input.setPlaceholderText("Default 1")

        self.inner_constant_input = QLineEdit()
        self.inner_constant_input.setValidator(validator)
        self.inner_constant_input.setPlaceholderText("Default 0")

        self.outer_constant_input = QLineEdit()
        self.outer_constant_input.setValidator(validator)
        self.outer_constant_input.setPlaceholderText("Default 0")

        form_layout.addRow("Root type", self.root_selector)
        form_layout.addRow("Outside coefficient", self.outer_coefficient_input)
        form_layout.addRow("Inside x coefficient", self.inner_x_coefficient_input)
        form_layout.addRow("Inside constant", self.inner_constant_input)
        form_layout.addRow("Outside constant", self.outer_constant_input)

        button_row = QHBoxLayout()
        button_row.setSpacing(12)

        self.calculate_btn = QPushButton("Differentiate Root Equation")
        self.calculate_btn.setObjectName("PrimaryButton")
        self.calculate_btn.clicked.connect(self.calculate_derivative)

        self.reset_btn = QPushButton("Reset Fields")
        self.reset_btn.setObjectName("SecondaryButton")
        self.reset_btn.clicked.connect(self.reset_inputs)

        button_row.addWidget(self.calculate_btn)
        button_row.addWidget(self.reset_btn)
        layout.addLayout(button_row)

        helper_text = QLabel(
            "The inner expression is interpreted as mx + b. The derivative includes the slope m automatically."
        )
        helper_text.setObjectName("MutedText")
        helper_text.setWordWrap(True)
        layout.addWidget(helper_text)

        for widget in (
            self.root_selector,
            self.outer_coefficient_input,
            self.inner_x_coefficient_input,
            self.inner_constant_input,
            self.outer_constant_input,
        ):
            if isinstance(widget, QComboBox):
                widget.currentIndexChanged.connect(self._update_preview)
            else:
                widget.textChanged.connect(self._update_preview)
                widget.returnPressed.connect(self.calculate_derivative)

        return card

    def _build_examples_card(self):
        card, layout = self._create_card(
            "Guided examples",
            "These examples map directly to the kinds of root questions you described.",
        )

        example_row = QHBoxLayout()
        example_row.setSpacing(10)

        sample_one = QPushButton("Load y = √x − 3")
        sample_one.setObjectName("SecondaryButton")
        sample_one.clicked.connect(lambda: self._load_example(2, 1.0, 1.0, 0.0, -3.0))

        sample_two = QPushButton("Load y = ∛(x + 2)")
        sample_two.setObjectName("SecondaryButton")
        sample_two.clicked.connect(lambda: self._load_example(3, 1.0, 1.0, 2.0, 0.0))

        example_row.addWidget(sample_one)
        example_row.addWidget(sample_two)
        layout.addLayout(example_row)

        note = QLabel(
            "Root mode is intentionally guided so students can enter radical expressions and still see proper symbols like √ and ∛."
        )
        note.setObjectName("MutedText")
        note.setWordWrap(True)
        layout.addWidget(note)
        return card

    def _build_preview_card(self):
        card, layout = self._create_card(
            "Live preview",
            "Every change updates the interpreted equation and its equivalent fractional-power form.",
        )

        self.equation_preview = ScrollableValueBox("PreviewValue")
        self.equation_preview.setMaximumHeight(110)

        self.power_preview = ScrollableValueBox("PreviewValue")
        self.power_preview.setMaximumHeight(110)

        self.preview_note = QLabel()
        self.preview_note.setObjectName("MutedText")
        self.preview_note.setWordWrap(True)

        layout.addWidget(QLabel("Equation entered"))
        layout.addWidget(self.equation_preview)
        layout.addWidget(QLabel("Fractional-power interpretation"))
        layout.addWidget(self.power_preview)
        layout.addWidget(self.preview_note)
        layout.addStretch()
        return card

    def _create_card(self, title_text: str, subtitle_text: str):
        card = QFrame()
        card.setObjectName("Card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(16)

        title = QLabel(title_text)
        title.setObjectName("CardTitle")
        subtitle = QLabel(subtitle_text)
        subtitle.setObjectName("MutedText")
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        return card, layout

    def _set_default_inputs(self):
        self.root_selector.setCurrentIndex(0)
        self.outer_coefficient_input.setText("1")
        self.inner_x_coefficient_input.setText("1")
        self.inner_constant_input.setText("0")
        self.outer_constant_input.setText("0")

    def reset_inputs(self):
        self._set_default_inputs()
        self.result_widget.clear_result()
        self.status_message.emit("Root equation form reset.", 3000)

    def _load_example(
        self,
        root_degree: int,
        outer_coefficient: float,
        inner_x_coefficient: float,
        inner_constant: float,
        outer_constant: float,
    ):
        self.root_selector.setCurrentIndex(0 if root_degree == 2 else 1)
        self.outer_coefficient_input.setText(format_number(outer_coefficient))
        self.inner_x_coefficient_input.setText(format_number(inner_x_coefficient))
        self.inner_constant_input.setText(format_number(inner_constant))
        self.outer_constant_input.setText(format_number(outer_constant))
        self.calculate_derivative()
        self.status_message.emit("Root example loaded.", 4000)

    def _read_inputs(self):
        root_degree = self.root_selector.currentData()
        outer_coefficient = self._parse_or_default(self.outer_coefficient_input.text(), 1.0)
        inner_x_coefficient = self._parse_or_default(self.inner_x_coefficient_input.text(), 1.0)
        inner_constant = self._parse_or_default(self.inner_constant_input.text(), 0.0)
        outer_constant = self._parse_or_default(self.outer_constant_input.text(), 0.0)

        return {
            "root_degree": root_degree,
            "outer_coefficient": outer_coefficient,
            "inner_x_coefficient": inner_x_coefficient,
            "inner_constant": inner_constant,
            "outer_constant": outer_constant,
        }

    def _parse_or_default(self, text: str, default: float) -> float:
        stripped = text.strip()
        if not stripped:
            return default
        return float(stripped)

    def _expression_details(self, inputs):
        root_degree = inputs["root_degree"]
        outer_coefficient = inputs["outer_coefficient"]
        inner_x_coefficient = inputs["inner_x_coefficient"]
        inner_constant = inputs["inner_constant"]
        outer_constant = inputs["outer_constant"]

        inner_expression = _format_linear_expression(inner_x_coefficient, inner_constant)
        radical_body = f"{_radical_name(root_degree)}({inner_expression})"
        head_expression = _join_coefficient_and_body(outer_coefficient, radical_body)
        equation_text = _combine_with_constant(head_expression, outer_constant)

        power_body = _power_body(inner_expression, 1 / root_degree)
        power_expression = _join_coefficient_and_body(outer_coefficient, power_body)
        power_form_text = _combine_with_constant(power_expression, outer_constant)
        power_expression_unicode = _join_coefficient_and_body(
            outer_coefficient,
            _power_body_unicode(inner_expression, 1 / root_degree),
        )
        power_form_unicode = _combine_with_constant(power_expression_unicode, outer_constant)

        if _is_zero(outer_coefficient) or _is_zero(inner_x_coefficient):
            derivative_text = "0"
            derivative_unicode = "0"
        else:
            derivative_coefficient = outer_coefficient * inner_x_coefficient / root_degree
            derivative_exponent = 1 / root_degree - 1
            derivative_body = _power_body(inner_expression, derivative_exponent)
            derivative_text = _join_coefficient_and_body(
                derivative_coefficient,
                derivative_body,
                formatter=format_exponent,
            )
            derivative_unicode = _join_coefficient_and_body(
                derivative_coefficient,
                _power_body_unicode(inner_expression, derivative_exponent),
                formatter=format_exponent,
            )

        return equation_text, power_form_text, derivative_text, power_form_unicode, derivative_unicode

    def _update_preview(self):
        try:
            equation_text, power_form_text, derivative_text, power_form_unicode, derivative_unicode = self._expression_details(
                self._read_inputs()
            )
        except ValueError:
            self.equation_preview.set_value("Finish the numeric inputs to preview the equation.")
            self.power_preview.set_value("The fractional-power form will appear here.")
            self.preview_note.setText("Use whole numbers or decimals in every numeric field.")
            return

        equation_expression, _ = _radical_sympy_expression(self._read_inputs())
        self.equation_preview.set_value(_pretty_math_text(equation_expression, "y"))
        self.power_preview.set_value(f"y = {power_form_unicode}")
        self.preview_note.setText(f"Expected derivative: y′ = {derivative_unicode}")

    def calculate_derivative(self):
        try:
            (
                equation_text,
                power_form_text,
                derivative_text,
                power_form_unicode,
                derivative_unicode,
            ) = self._expression_details(self._read_inputs())
        except ValueError:
            QMessageBox.warning(self, "Invalid values", "Use valid numbers in the root equation fields.")
            return

        equation_expression, _ = _radical_sympy_expression(self._read_inputs())
        self.result_widget.set_result(
            _pretty_math_text(equation_expression, "y"),
            f"y = {power_form_unicode}",
            f"y′ = {derivative_unicode}",
            True,
            "Root mode now shows radicals and powers with clearer mathematical symbols while still applying the power rule and inner slope.",
        )
        self.status_message.emit("Root derivative updated.", 4000)

    def solve_workspace(self):
        self.calculate_derivative()

    def reset_workspace(self):
        self.reset_inputs()
