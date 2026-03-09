# Copyright 2026 QuickRed Tech
# Licensed under the Apache License, Version 2.0
# This code is part of the QuickRed Tech project and is licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0

print("Welcome to the Power Rule Differentiation Method!")
print("Example: 2X^3 - 3X^2 + 4")

# Ask how many terms the equation has
num_terms = int(input("Enter the number of terms in your equation: "))

# Lists to store coefficients, powers, and derivatives
coefficients = []
powers = []
derivatives = []
new_powers = []

# Loop to get term details
for i in range(num_terms):
    print(f"\nTerm {i+1}:")
    coefficient = int(input("Enter the coefficient: "))
    power = int(input("Enter the power: "))
    
    coefficients.append(coefficient)
    powers.append(power)
    
    # Apply the power rule
    derivatives.append(coefficient * power)
    new_powers.append(power - 1)

# Ask for the signs between terms
signs = input(f"Enter {num_terms-1} signs (+ or -) between the terms in order: ").strip()

# Display results
print("\nDerivatives of each term:")
for i in range(num_terms):
    print(f"Term {i+1}: {derivatives[i]}X^{new_powers[i]}")

# Build the full derivative equation
full_derivative = ""
for i in range(num_terms):
    full_derivative += f"{derivatives[i]}X^{new_powers[i]}"
    if i < num_terms - 1:
        full_derivative += f" {signs[i]} "

print(f"\nThe derivative of the full equation is: {full_derivative}")