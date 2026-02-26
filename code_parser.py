import ast
from typing import Dict, Any

class CodeAnalyzer(ast.NodeVisitor):
    """
    Custom AST Analyzer that visits nodes
    and collects feedback about the code.
    """

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
    """
    Parses user Python code and returns:
    - AST tree
    - Formatted code
    - AST structure
    - Basic feedback
    """

    result = {
        "success": False,
        "formatted_code": None,
        "ast_dump": None,
        "feedback": None,
        "error": None
    }

    try:
        # Step 1: Parse code into AST
        tree = ast.parse(code)

        # Step 2: Format code 
        formatted_code = ast.unparse(tree)

        # Step 3: Dump AST structure
        ast_structure = ast.dump(tree, indent=4)

        # Step 4: Analyze using NodeVisitor
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


# Example Usage 
if __name__ == "__main__":

    sample_code = """import math
def calculate_area(radius):
    for i in range(3):
        print(i)
    return math.pi * radius * radius
"""

    output = parse_code(sample_code)

    if output["success"]:
        print("Code Parsed Successfully.\n")

        print("---- Formatted Code ----")
        print(output["formatted_code"])

        print("\n---- AST Structure ----")
        print(output["ast_dump"])

        print("\n---- Feedback ----")
        for item in output["feedback"]:
            print("-", item)

    else:
        print("Error:", output["error"])
