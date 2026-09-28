def poly_to_string(coeffs: list, var: str = 'x') -> str:
    """
    Convert a polynomial coefficient list to a readable string.
    
    Args:
        coeffs: List of coefficients in descending order (highest degree first)
        var: Variable name to use (default 'x')
    
    Returns:
        String representation of the polynomial
    
    Example:
        poly_to_string([1, 0, -1]) returns "x^2 - 1"
        poly_to_string([2, -3, 0, 5]) returns "2x^3 - 3x^2 + 5"
    """
    if not coeffs or all(c == 0 for c in coeffs):
        return "0"
    
    # Remove leading zeros
    while len(coeffs) > 1 and coeffs[0] == 0:
        coeffs = coeffs[1:]
    
    terms = []
    degree = len(coeffs) - 1
    
    for i, coef in enumerate(coeffs):
        power = degree - i
        
        # Skip zero coefficients
        if coef == 0:
            continue
        
        # Build the term
        term = ""
        
        # Handle coefficient
        abs_coef = abs(coef)
        if power == 0:
            # Constant term - always show the coefficient
            term = str(abs_coef)
        elif abs_coef == 1:
            # Coefficient is 1 or -1 (don't show the 1)
            term = ""
        else:
            # Show the coefficient
            if abs_coef == int(abs_coef):
                term = str(int(abs_coef))
            else:
                term = str(abs_coef)
        
        # Add variable and power
        if power > 1:
            term += f"{var}^{power}"
        elif power == 1:
            term += var
        
        # Add sign
        if coef < 0:
            if terms:  # Not the first term
                terms.append(f"- {term}")
            else:  # First term
                terms.append(f"-{term}")
        else:
            if terms:  # Not the first term
                terms.append(f"+ {term}")
            else:  # First term
                terms.append(term)
    
    return " ".join(terms) if terms else "0"


def divide_poly(numerator: list, divisor: list) -> tuple[list, list]:
    """
    Divide two polynomials using polynomial long division.
    
    Args:
        numerator: List of coefficients in descending order (highest degree first)
                   e.g., [1, 0, -1] represents x^2 - 1
        divisor: List of coefficients in descending order (highest degree first)
                 e.g., [1, -1] represents x - 1
    
    Returns:
        Tuple of (quotient, remainder) as lists of coefficients
    
    Example:
        divide_poly([1, 0, -1], [1, -1]) divides (x^2 - 1) by (x - 1)
        Returns ([1.0, 1.0], [0]) representing quotient (x + 1) and remainder 0
    """
    # Handle edge cases
    if not divisor or all(c == 0 for c in divisor):
        raise ValueError("Divisor cannot be zero polynomial")
    
    if not numerator or all(c == 0 for c in numerator):
        return [0], [0]
    
    # Helper function to remove leading zeros
    def remove_leading_zeros(poly):
        while len(poly) > 1 and poly[0] == 0:
            poly = poly[1:]
        return poly if poly else [0]
    
    # Make copies and remove leading zeros
    numerator = remove_leading_zeros(list(numerator))
    divisor = remove_leading_zeros(list(divisor))
    
    quotient = []
    remainder = list(numerator)
    
    # Polynomial long division algorithm
    while len(remainder) >= len(divisor):
        # Check if remainder is effectively zero
        if all(abs(c) < 1e-10 for c in remainder):
            break
            
        # Divide the leading term of remainder by leading term of divisor
        coef = remainder[0] / divisor[0]
        quotient.append(coef)
        
        # Multiply divisor by this coefficient and subtract from remainder
        for i in range(len(divisor)):
            remainder[i] -= coef * divisor[i]
        
        # Remove the leading term (which should now be ~zero)
        remainder = remainder[1:]
    
    # Clean up results
    if not quotient:
        quotient = [0]
    if not remainder:
        remainder = [0]
    
    # Remove any leading zeros from final results
    remainder = remove_leading_zeros(remainder)
    quotient = remove_leading_zeros(quotient)
    
    return quotient, remainder


# Test cases
if __name__ == "__main__":
    print("Polynomial Division Examples:")
    print("=" * 60)
    
    # Test 1: (x^2 - 1) / (x - 1) = x + 1, remainder 0
    print("\nTest 1:")
    num, div = [1, 0, -1], [1, -1]
    q, r = divide_poly(num, div)
    print(f"({poly_to_string(num)}) / ({poly_to_string(div)})")
    print(f"Quotient:  {poly_to_string(q)}")
    print(f"Remainder: {poly_to_string(r)}")
    
    # Test 2: (x^3 + 2x^2 + 3x + 4) / (x + 1)
    print("\nTest 2:")
    num, div = [1, 2, 3, 4], [1, 1]
    q, r = divide_poly(num, div)
    print(f"({poly_to_string(num)}) / ({poly_to_string(div)})")
    print(f"Quotient:  {poly_to_string(q)}")
    print(f"Remainder: {poly_to_string(r)}")
    
    # Test 3: (2x^2 + 3x + 1) / (x + 1)
    print("\nTest 3:")
    num, div = [2, 3, 1], [1, 1]
    q, r = divide_poly(num, div)
    print(f"({poly_to_string(num)}) / ({poly_to_string(div)})")
    print(f"Quotient:  {poly_to_string(q)}")
    print(f"Remainder: {poly_to_string(r)}")
    
    # Test 4: (x^2 + 1) / (x^2 + 1) = 1, remainder 0
    print("\nTest 4:")
    num, div = [1, 0, 1], [1, 0, 1]
    q, r = divide_poly(num, div)
    print(f"({poly_to_string(num)}) / ({poly_to_string(div)})")
    print(f"Quotient:  {poly_to_string(q)}")
    print(f"Remainder: {poly_to_string(r)}")
    
    # Test 5: (x^3 + 1) / (x^2 + x + 1)
    print("\nTest 5:")
    num, div = [1, 0, 0, 1], [1, 1, 1]
    q, r = divide_poly(num, div)
    print(f"({poly_to_string(num)}) / ({poly_to_string(div)})")
    print(f"Quotient:  {poly_to_string(q)}")
    print(f"Remainder: {poly_to_string(r)}")
    
    # Test 6: (5x^4 - 3x^2 + 7) / (x - 2)
    print("\nTest 6:")
    num, div = [5, 0, -3, 0, 7], [1, -2]
    q, r = divide_poly(num, div)
    print(f"({poly_to_string(num)}) / ({poly_to_string(div)})")
    print(f"Quotient:  {poly_to_string(q)}")
    print(f"Remainder: {poly_to_string(r)}")

