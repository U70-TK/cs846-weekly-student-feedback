
from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

def safe_eval(expr):
    """
    Safely evaluate a simple arithmetic expression using ast.
    Allowed: +, -, *, /, //, %, **, (, ), numbers, whitespace.
    Disallows function calls, attribute access, and all non-arithmetic operations.
    Limits expression length to prevent DoS.
    """
    if not isinstance(expr, str) or len(expr) > 256:
        raise ValueError("Expression too long or not a string")
    allowed_nodes = (
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow,
        ast.USub, ast.UAdd, ast.Load
    )
    def _check_node(node):
        if isinstance(node, ast.Name):
            raise ValueError("Names are not allowed")
        elif isinstance(node, ast.Call):
            raise ValueError("Function calls are not allowed")
        elif isinstance(node, ast.Attribute):
            raise ValueError("Attribute access is not allowed")
        elif isinstance(node, ast.Subscript):
            raise ValueError("Subscript access is not allowed")
        elif isinstance(node, ast.ListComp):
            raise ValueError("List comprehensions are not allowed")
        elif isinstance(node, ast.Lambda):
            raise ValueError("Lambda expressions are not allowed")
        elif type(node) not in allowed_nodes:
            raise ValueError(f"Disallowed node: {type(node).__name__}")
        for child in ast.iter_child_nodes(node):
            _check_node(child)
    try:
        tree = ast.parse(expr, mode="eval")
        _check_node(tree)
        # Evaluate safely, catch division by zero
        try:
            result = eval(compile(tree, filename="<expr>", mode="eval"), {"__builtins__": {}})
        except ZeroDivisionError:
            raise ValueError("Division by zero")
        # Only allow int/float results
        if not isinstance(result, (int, float)):
            raise ValueError("Result type not allowed")
        return result
    except Exception:
        raise ValueError("Invalid expression")

@app.route('/calculator', methods=['POST'])
def calculate():
    if not request.is_json:
        return '', 400
    data = request.get_json()
    if not isinstance(data, dict) or 'expression' not in data:
        return '', 400
    expr = data['expression']
    if not isinstance(expr, str):
        return '', 400
    try:
        result = safe_eval(expr)
        return jsonify({"result": str(result)})
    except Exception:
        return '', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)