import ast
from typing import Dict, Any

class CodeAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.feedback = []
        self.function_count = 0
        self.loop_count = 0
        self.import_count = 0

    def visit_FunctionDef(self, node):
        self.function_count += 1
        self.feedback.append(f"Function detected: '{node.name}'")
        self.generic_visit(node)

    def visit_For(self, node):
        self.loop_count += 1
        self.feedback.append("For loop detected.")
        self.generic_visit(node)

    def visit_While(self, node):
        self.loop_count += 1
        self.feedback.append("While loop detected.")
        self.generic_visit(node)

    def visit_Import(self, node):
        self.import_count += 1
        self.feedback.append("Import statement detected.")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.import_count += 1
        self.feedback.append("Import-from statement detected.")
        self.generic_visit(node)


def parse_code(code: str) -> Dict[str, Any]:

    result = {
        "success": False,
        "formatted_code": None,
        "ast_dump": None,
        "feedback": None,
        "error": None
    }

    try:
        tree = ast.parse(code)

        formatted_code = ast.unparse(tree)

        ast_structure = ast.dump(tree, indent=4)

        analyzer = CodeAnalyzer()
        analyzer.visit(tree)

        result["success"] = True
        result["formatted_code"] = formatted_code
        result["ast_dump"] = ast_structure
        result["feedback"] = analyzer.feedback

    except SyntaxError as e:
        result["error"] = f"Syntax Error: {e}"

    except Exception as e:
        result["error"] = f"Unexpected Error: {e}"

    return result
