from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QTextEdit, QVBoxLayout


class ScrollableValueBox(QTextEdit):
    """Read-only text box with its own scrollbars for long expressions."""

    def __init__(self, object_name: str, parent=None):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setReadOnly(True)
        self.setAcceptRichText(False)
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setMinimumHeight(84)
        self.setMaximumHeight(140)

    def set_value(self, text: str):
        self.setPlainText(text)


class ResultDisplayWidget(QFrame):
    """Displays equation and derivative output in a styled card."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(12)

        title = QLabel("Derivative workspace")
        title.setObjectName("CardTitle")
        subtitle = QLabel("Review the equation, the equivalent power-rule form, and the simplified derivative.")
        subtitle.setObjectName("MutedText")
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.equation_title_label = QLabel()
        self.power_rule_title_label = QLabel()
        self.derivative_title_label = QLabel()

        self.equation_label = ScrollableValueBox("ResultValue")

        self.power_rule_label = ScrollableValueBox("ResultValue")

        self.derivative_label = ScrollableValueBox("ResultValue")

        self.note_label = QLabel()
        self.note_label.setObjectName("MutedText")
        self.note_label.setWordWrap(True)

        layout.addWidget(self.equation_title_label)
        layout.addWidget(self.equation_label)
        layout.addWidget(self.power_rule_title_label)
        layout.addWidget(self.power_rule_label)
        layout.addWidget(self.derivative_title_label)
        layout.addWidget(self.derivative_label)
        layout.addWidget(self.note_label)

        self.set_section_titles()
        self.clear_result()

    def set_section_titles(
        self,
        equation_title: str = "Equation entered",
        power_title: str = "Power-rule interpretation",
        derivative_title: str = "Derivative",
    ):
        self.equation_title_label.setText(equation_title)
        self.power_rule_title_label.setText(power_title)
        self.derivative_title_label.setText(derivative_title)

    def clear_result(self):
        self.equation_label.set_value("Build an equation to see the formatted result.")
        self.power_rule_label.set_value("Root terms are converted into fractional powers automatically.")
        self.derivative_label.set_value("Press Differentiate Equation when you are ready.")
        self.note_label.setText("Version 1 focuses on clean power-rule differentiation for polynomial and root terms.")

    def set_result(
        self,
        equation_text: str,
        power_rule_text: str,
        derivative_text: str,
        contains_roots: bool,
        note_text: str | None = None,
    ):
        self.equation_label.set_value(equation_text)
        self.power_rule_label.set_value(power_rule_text)
        self.derivative_label.set_value(derivative_text)

        if note_text:
            self.note_label.setText(note_text)
        elif contains_roots:
            self.note_label.setText(
                "Root expressions are differentiated by converting them to fractional powers before applying the power rule."
            )
        else:
            self.note_label.setText("Polynomial terms are differentiated term-by-term using the standard power rule.")


# Preserve the older name in case other modules still import it directly.
ResultWidget = ResultDisplayWidget
