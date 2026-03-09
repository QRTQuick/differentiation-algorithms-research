# polynomial.py
# Copyright 2026 QuickRed Tech
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

from term import Term

class Polynomial:
    """Represents a full polynomial with multiple terms."""
    def __init__(self):
        self.terms = []
        self.signs = []
    
    def add_term(self, term: Term):
        self.terms.append(term)
    
    def set_signs(self, signs: str):
        if len(signs) != len(self.terms) - 1:
            raise ValueError("Number of signs must be one less than number of terms.")
        self.signs = list(signs)
    
    def differentiate(self):
        derivatives = []
        for term in self.terms:
            term.differentiate()
            derivatives.append(term.derivative_str())
        
        full_derivative = ""
        for i, deriv in enumerate(derivatives):
            full_derivative += deriv
            if i < len(self.signs):
                full_derivative += f" {self.signs[i]} "
        return full_derivative