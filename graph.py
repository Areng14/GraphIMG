import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, sympify
from typing import Tuple

plt.figure(figsize=(10, 10))

# Preprocess functions
def preprocess_expression(expression: str) -> str:
    """Adds explicit multiplication symbols to the expression."""
    import re
    return re.sub(r'(?<=[0-9])(?=[a-zA-Z])', '*', expression)

def preprocess_for_axis(axis: str, expression: str) -> str:
    """Adjusts the expression to ensure it uses the correct variable for the given axis."""
    if axis == 'y':
        return expression.replace('y', 'x')
    elif axis == 'x':
        return expression.replace('x', 'y')
    return expression

# LINE function
def line(axis: str, expression: str, range_: str, color: Tuple[int, int, int]) -> None:
    x, y = symbols('x y')
    expression = preprocess_for_axis(axis, preprocess_expression(expression))
    sympy_expr = sympify(expression)

    # Parse the range
    range_var, range_values = range_.split("=")
    range_min, range_max = map(float, range_values.split(","))

    var_vals = np.linspace(range_min, range_max, 1000)  # Smooth plotting
    x_vals, y_vals = [], []

    if axis == 'y':  # y depends on x
        for val in var_vals:
            try:
                x_val = val
                y_val = float(sympy_expr.subs(x, val).evalf())
                x_vals.append(x_val)
                y_vals.append(y_val)
            except (TypeError, ValueError):
                continue
    elif axis == 'x':  # x depends on y
        for val in var_vals:
            try:
                y_val = val
                x_val = float(sympy_expr.subs(y, val).evalf())
                x_vals.append(x_val)
                y_vals.append(y_val)
            except (TypeError, ValueError):
                continue
    else:
        raise ValueError(f"Invalid axis '{axis}'.")

    if len(x_vals) == 0 or len(y_vals) == 0:
        raise ValueError(f"No valid points to plot for expression '{expression}'.")

    matplotlib_color = tuple(c / 255 for c in color)
    plt.plot(x_vals, y_vals, color=matplotlib_color, label=f"{axis}({expression})")

# INEQUALITY function
def inequality(axis: str, expression: str, range_: str, color: Tuple[int, int, int], operator: str) -> None:
    """
    Handles inequalities by shading the region.

    Parameters:
    axis (str): The base axis ('x' or 'y') of the inequality.
    expression (str): The mathematical expression for the inequality.
    range_ (str): The range for the variable (e.g., 'x=-5,5').
    color (Tuple[int, int, int]): The RGB color of the shading region.
    operator (str): The inequality type ('less', 'lesse', 'great', 'greate').
    """
    x, y = symbols('x y')
    expression = preprocess_for_axis(axis, preprocess_expression(expression))
    sympy_expr = sympify(expression)

    # Parse the range
    range_var, range_values = range_.split("=")
    range_min, range_max = map(float, range_values.split(","))

    var_vals = np.linspace(range_min, range_max, 1000)
    x_vals, y_vals = [], []

    if axis == 'y':  # y depends on x
        for val in var_vals:
            try:
                x_vals.append(val)
                y_vals.append(float(sympy_expr.subs(x, val).evalf()))
            except (TypeError, ValueError):
                continue

        matplotlib_color = tuple(c / 255 for c in color)
        if operator in ["less", "lesse"]:  # Shade below
            plt.fill_between(x_vals, y_vals, range_min, color=matplotlib_color, alpha=1)
        elif operator in ["great", "greate"]:  # Shade above
            plt.fill_between(x_vals, y_vals, range_max, color=matplotlib_color, alpha=1)

    elif axis == 'x':  # x depends on y
        for val in var_vals:
            try:
                y_vals.append(val)
                x_vals.append(float(sympy_expr.subs(y, val).evalf()))
            except (TypeError, ValueError):
                continue

        matplotlib_color = tuple(c / 255 for c in color)
        if operator in ["less", "lesse"]:  # Shade left
            plt.fill_betweenx(y_vals, x_vals, range_min, color=matplotlib_color, alpha=1)
        elif operator in ["great", "greate"]:  # Shade right
            plt.fill_betweenx(y_vals, x_vals, range_max, color=matplotlib_color, alpha=1)

# Export function
def export(filepath: str = "graph.png") -> None:
    """Exports the current plot to a file."""
    plt.axis('off')  # Turn off axes for a clean image
    plt.savefig(filepath, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"Graph exported to {filepath}")
