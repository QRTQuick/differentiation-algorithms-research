# term.py
# Copyright 2026 QuickRed Tech
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

class Term:
    """Represents a single term in a polynomial."""
    def __init__(self, coefficient: int, power: int):
        self.coefficient = coefficient
        self.power = power
        self.derivative_coefficient = None
        self.derivative_power = None
    
    def differentiate(self):
        self.derivative_coefficient = self.coefficient * self.power
        self.derivative_power = self.power - 1
        return self.derivative_coefficient, self.derivative_power
    
    def derivative_str(self):
        return f"{self.derivative_coefficient}X^{self.derivative_power}"