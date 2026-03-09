from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QComboBox, QFormLayout, QFrame, QLabel, QLineEdit, QVBoxLayout, QWidget

from core.term import Term


class TermInputWidget(QWidget):
    """Styled form for building a single term."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self._connect_signals()
        self.set_first_term_mode(True)
        self.clear_inputs()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        self.mode_label = QLabel("First term starts the equation.")
        self.mode_label.setObjectName("MutedText")
        layout.addWidget(self.mode_label)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(self.mode_label.alignment())
        form_layout.setFormAlignment(self.mode_label.alignment())
        form_layout.setSpacing(14)
        layout.addLayout(form_layout)

        numeric_validator = QDoubleValidator(-999999.0, 999999.0, 4, self)

        self.sign_input = QComboBox()
        self.sign_input.addItem("Add to equation", "+")
        self.sign_input.addItem("Subtract from equation", "-")

        self.coeff_input = QLineEdit()
        self.coeff_input.setPlaceholderText("Example: 3 or -2.5")
        self.coeff_input.setValidator(numeric_validator)

        self.power_input = QLineEdit()
        self.power_input.setPlaceholderText("Default is 1")
        self.power_input.setValidator(numeric_validator)

        self.root_input = QComboBox()
        self.root_input.addItem("Standard power xⁿ", None)
        self.root_input.addItem("Square root √x", 2.0)
        self.root_input.addItem("Cube root ∛x", 3.0)

        form_layout.addRow("Join sign", self.sign_input)
        form_layout.addRow("Coefficient", self.coeff_input)
        form_layout.addRow("Power", self.power_input)
        form_layout.addRow("Structure", self.root_input)

        preview_card = QFrame()
        preview_card.setObjectName("PreviewCard")
        preview_layout = QVBoxLayout(preview_card)
        preview_layout.setContentsMargins(18, 16, 18, 16)
        preview_layout.setSpacing(8)

        preview_title = QLabel("Live term preview")
        preview_title.setObjectName("SectionLabel")
        self.preview_value = QLabel("Enter a coefficient to preview the term.")
        self.preview_value.setObjectName("PreviewValue")
        self.preview_value.setWordWrap(True)

        self.preview_note = QLabel("Power-rule form appears here after you complete the inputs.")
        self.preview_note.setObjectName("MutedText")
        self.preview_note.setWordWrap(True)

        preview_layout.addWidget(preview_title)
        preview_layout.addWidget(self.preview_value)
        preview_layout.addWidget(self.preview_note)
        layout.addWidget(preview_card)

    def _connect_signals(self):
        self.coeff_input.textChanged.connect(self._update_preview)
        self.power_input.textChanged.connect(self._update_preview)
        self.root_input.currentIndexChanged.connect(self._update_preview)
        self.sign_input.currentIndexChanged.connect(self._update_preview)

    def set_first_term_mode(self, is_first_term: bool):
        self.sign_input.setDisabled(is_first_term)
        if is_first_term:
            self.mode_label.setText("First term starts the equation. Its sign comes from the coefficient itself.")
        else:
            self.mode_label.setText("The join sign is placed before this new term.")

    def clear_inputs(self):
        self.sign_input.setCurrentIndex(0)
        self.coeff_input.clear()
        self.power_input.setText("1")
        self.root_input.setCurrentIndex(0)
        self._update_preview()

    def focus_coefficient(self):
        self.coeff_input.setFocus()
        self.coeff_input.selectAll()

    def get_term_data(self):
        coefficient_text = self.coeff_input.text().strip()
        power_text = self.power_input.text().strip()

        if not coefficient_text:
            raise ValueError("Enter a coefficient for the term.")

        coefficient = float(coefficient_text)
        if abs(coefficient) < 1e-9:
            raise ValueError("Coefficient cannot be zero.")

        power = float(power_text) if power_text else 1.0
        root = self.root_input.currentData()
        sign = self.sign_input.currentData()

        return sign, coefficient, power, root

    def _update_preview(self):
        coefficient_text = self.coeff_input.text().strip()
        power_text = self.power_input.text().strip()
        root = self.root_input.currentData()

        if not coefficient_text:
            self.preview_value.setText("Enter a coefficient to preview the term.")
            self.preview_note.setText("Power-rule form appears here after you complete the inputs.")
            return

        try:
            coefficient = float(coefficient_text)
            power = float(power_text) if power_text else 1.0
        except ValueError:
            self.preview_value.setText("Finish the numeric inputs to generate a clean preview.")
            self.preview_note.setText("Use whole numbers or decimals for the coefficient and power.")
            return

        term = Term(coefficient, power, root)
        self.preview_value.setText(term.display_expression_unicode())
        self.preview_note.setText(f"Power-rule form: {term.standard_expression_unicode()}")
