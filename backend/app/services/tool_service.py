from datetime import datetime, timezone
import ast
import operator as op


_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def _safe_eval(node):
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.UnaryOp):
        return _ALLOWED_OPERATORS[type(node.op)](_safe_eval(node.operand))
    if isinstance(node, ast.BinOp):
        return _ALLOWED_OPERATORS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    raise ValueError("Biểu thức không hợp lệ")


def calculator(expression: str) -> str:
    tree = ast.parse(expression, mode="eval")
    return str(_safe_eval(tree.body))


def current_time_tool() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


TOOLS = {
    "calculator": {
        "description": "Tính toán biểu thức toán học cơ bản",
        "handler": calculator,
    },
    "current_time": {
        "description": "Lấy thời gian hiện tại theo UTC",
        "handler": lambda _=None: current_time_tool(),
    },
}
