# main.py
# Copyright 2026 QuickRed Tech
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

from polynomial import Polynomial
from term import Term

def main():
    print("Welcome to the Power Rule Differentiation Method!")
    print("Example: 2X^3 - 3X^2 + 4")
    
    num_terms = int(input("Enter the number of terms in your equation: "))
    
    polynomial = Polynomial()
    
    for i in range(num_terms):
        print(f"\nTerm {i+1}:")
        coefficient = int(input("Enter the coefficient: "))
        power = int(input("Enter the power: "))
        polynomial.add_term(Term(coefficient, power))
    
    if num_terms > 1:
        signs = input(f"Enter {num_terms-1} signs (+ or -) between the terms in order: ").strip()
        polynomial.set_signs(signs)
    
    derivative = polynomial.differentiate()
    print("\nDerivative of each term:")
    for i, term in enumerate(polynomial.terms):
        print(f"Term {i+1}: {term.derivative_str()}")
    
    print(f"\nThe derivative of the full equation is: {derivative}")

if __name__ == "__main__":
    main()