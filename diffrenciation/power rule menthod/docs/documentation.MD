# Power Rule Differentiation Method - Documentation

## Overview

The Power Rule Differentiation Method is an implementation of one of the fundamental calculus rules for finding derivatives of polynomial functions. This program specifically handles polynomial equations with two terms and calculates their derivatives using the mathematical power rule.

---

## Mathematical Background

### The Power Rule Formula

The power rule states that for any term of the form $ax^n$, the derivative is:

$$\frac{d}{dx}[ax^n] = n \cdot a \cdot x^{n-1}$$

Where:
- **a** = coefficient of the term
- **n** = power/exponent of the variable
- **x** = the variable

### Example

For the equation: $2x^3 - 3x^2 + 2$

Applying the power rule:
- First term: $2x^3$ → derivative is $3 \cdot 2 \cdot x^{3-1} = 6x^2$
- Second term: $-3x^2$ → derivative is $2 \cdot (-3) \cdot x^{2-1} = -6x$
- Constant: $2$ → derivative is $0$

Result: $6x^2 - 6x$

---

## Code Structure

### Purpose
This program automates the process of calculating derivatives of two-term polynomial equations using the power rule, eliminating manual calculation errors.

### Input Requirements

The program requires the following user inputs:

| Input | Type | Description |
|-------|------|-------------|
| `equation` | String | The complete equation to differentiate (informational) |
| `signBetweenTerms` | String | The sign between the two terms (+ or -) |
| `coefficient1` | Integer | The coefficient of the first term |
| `power1` | Integer | The exponent of the first term |
| `coefficient2` | Integer | The coefficient of the second term |
| `power2` | Integer | The exponent of the second term |

### Processing Steps

1. **Accept User Input**: Gather equation, coefficients, and powers
2. **Apply Power Rule to First Term**:
   - Multiply coefficient by power: `derivative1 = power1 * coefficient1`
   - Reduce power by 1: `new_power1 = power1 - 1`
3. **Apply Power Rule to Second Term**:
   - Multiply coefficient by power: `derivative2 = power2 * coefficient2`
   - Reduce power by 1: `new_power2 = power2 - 1`
4. **Display Results**: Print the derivative terms and final derivative expression

### Output

The program outputs:
1. **First derivative term**: `derivative1 X^new_power1`
2. **Second derivative term**: `derivative2 X^new_power2`
3. **Complete derivative**: Combines both terms with the original sign between them

---

## Code Variables

| Variable | Type | Purpose |
|----------|------|---------|
| `equation` | str | Stores the original equation (user-provided) |
| `signBetweenTerms` | str | Stores the operator (+ or -) between terms |
| `coefficient1` | int | First term's coefficient |
| `power1` | int | First term's exponent |
| `coefficient2` | int | Second term's coefficient |
| `power2` | int | Second term's exponent |
| `derivative1` | int | Calculated derivative coefficient of first term |
| `derivative2` | int | Calculated derivative coefficient of second term |
| `new_power1` | int | Reduced power of first derivative term |
| `new_power2` | int | Reduced power of second derivative term |

---

## Usage Example

### Example 1: Simple Polynomial
**Input:**
```
Write the full equation: 2X^3 - 3X^2
Enter the sign between terms: -
Enter coefficient of first term: 2
Enter power of first term: 3
Enter coefficient of second term: 3
Enter power of second term: 2
```

**Output:**
```
The derivative of the first term is: 6X^2
The derivative of the second term is: -6X^1
The derivative of the equation is: 6X^2 - 6X^1
```

### Example 2: With Positive Sign
**Input:**
```
Write the full equation: 5X^4 + 2X^2
Enter the sign between terms: +
Enter coefficient of first term: 5
Enter power of first term: 4
Enter coefficient of second term: 2
Enter power of second term: 2
```

**Output:**
```
The derivative of the first term is: 20X^3
The derivative of the second term is: 4X^1
The derivative of the equation is: 20X^3 + 4X^1
```

---

## Algorithm Flow

```
START
  ↓
Display Welcome Message
  ↓
Get equation from user (informational)
  ↓
Get operation sign (+ or -)
  ↓
Get coefficient and power for Term 1
  ↓
Get coefficient and power for Term 2
  ↓
Calculate: derivative1 = power1 × coefficient1
  ↓
Calculate: new_power1 = power1 - 1
  ↓
Calculate: derivative2 = power2 × coefficient2
  ↓
Calculate: new_power2 = power2 - 1
  ↓
Display individual derivatives
  ↓
Display complete derivative expression
  ↓
END
```

---

## Limitations

⚠️ **Current Limitations:**

1. **Two Terms Only**: Can only handle equations with exactly two terms
2. **No Constants**: Cannot properly handle constant terms (derivative = 0)
3. **Integer Values Only**: Coefficients and powers must be integers
4. **No Simplification**: Results like $6X^1$ are not simplified to $6X$
5. **Manual Input**: Requires manual entry of coefficients and powers
6. **No Error Handling**: Does not validate user inputs or handle invalid entries

---

## Future Enhancements

Potential improvements could include:

- [ ] Support for equations with 3+ terms
- [ ] Automatic parsing of equation strings
- [ ] Constant term handling
- [ ] Rational number support (fractions, decimals)
- [ ] Result simplification (removing exponent 1, etc.)
- [ ] Input validation and error handling
- [ ] Support for multiple variables
- [ ] Handling of special functions (trig, exponential, logarithmic)
- [ ] Display in LaTeX/mathematical notation

---

## License

Copyright 2026 QuickRed Tech - Licensed under Apache License, Version 2.0

---

## Related Concepts

- **Calculus**: Branch of mathematics dealing with rates of change
- **Derivative**: Measure of how a function changes at a point
- **Polynomial**: Expression with multiple terms and powers
- **Coefficient**: Numerical factor in front of a variable term
- **Exponent**: Power to which a variable is raised
