from fastmcp import FastMCP
from sympy import nroots, sympify
mcp = FastMCP(name="EquationSOlvingServer")

@mcp.tool
def get_roots_to_equation(eqn: str) -> list:
    """
    Compute the numerical roots of a univariate equation given as a string.

    This function uses SymPy to parse the input string into a symbolic 
    expression and then computes approximate numerical roots (real or 
    complex) using `nroots`. The results are returned as strings for 
    easier display or serialization.

    Parameters
    ----------
    eqn : str
        A string representing a univariate polynomial or algebraic 
        equation in terms of `x`. The expression should be written 
        in Python syntax (e.g., "x**2 - 2" instead of "x^2 - 2").

    Returns
    -------
    list of str
        A list of string representations of the numerical roots.

    Examples
    --------
    >>> get_roots_to_equation("x**2 - 2")
    ['-1.41421356237310', '1.41421356237310']

    >>> get_roots_to_equation("x**3 - 1")
    ['1.00000000000000', 
     '-0.500000000000000 - 0.866025403784439*I', 
     '-0.500000000000000 + 0.866025403784439*I']
    """
    eqn = sympify(eqn)
    roots = nroots(eqn)
    return [str(i) for i in roots]


if __name__ == "__main__":
    print("\n Starting Test Server...")
    mcp.run(
        transport="sse",
        host="127.0.0.1", 
        port=6969
    )
