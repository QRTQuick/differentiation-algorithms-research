# Copyright 2026 QuickRed Tech
# Licensed under the Apache License, Version 2.0

# This code is part of the QuickRed Tech project and is licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0

#imports of libraries

print("Welcome to the Power Rule Differentiation Method!")
print("example of equations that can be differentiated using this method: 2X^3-3X^3+2")
print("the answer to this question is: 6X^2-9X^2")
# Function to differentiate using the power rule
equation = input("write the full equation you want to differentiate: ")
signBetweenTerms = input("enter the sign between the terms in th other they appear (either + or -): ")
coefficient1 = int(input("enter the coefficient of the first term: "))
power1 = int(input("enter the power of the first term: "))
coefficient2 = int(input("enter the coefficient of the second term: "))
power2 = int(input("enter the power of the second term: "))
# Applying the power rule: d/dx [ax^n] = n*ax^(n-1)
derivative1 = power1 * coefficient1
derivative2 = power2 * coefficient2
new_power1 = power1 - 1
new_power2 = power2 - 1

print(f"The derivative of the first term is: {derivative1}X^{new_power1}")
print(f"The derivative of the second term is: {derivative2}X^{new_power2}")
print(f"The derivative of the equation is: {derivative1}X^{new_power1} {signBetweenTerms[0]} {derivative2}X^{new_power2}")

