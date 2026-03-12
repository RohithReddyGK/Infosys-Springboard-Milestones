import ast

class ErrorDetector(ast.NodeVisitor):

    def __init__(self):
        self.defined_vars = set()
        self.used_vars = set()
        self.imports = set()
        self.infinite_loops = []
        self.long_functions = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.defined_vars.add(node.id)

        elif isinstance(node.ctx, ast.Load):
            self.used_vars.add(node.id)

        self.generic_visit(node)

    def visit_While(self, node):

        if isinstance(node.test, ast.Constant) and node.test.value is True:

            has_break = any(isinstance(n, ast.Break) for n in ast.walk(node))

            if not has_break:
                self.infinite_loops.append(node.lineno)

        self.generic_visit(node)

    def visit_FunctionDef(self, node):

        start = node.lineno
        end = getattr(node, "end_lineno", start)
        length = end - start + 1

        if length > 20:
            self.long_functions.append(node.name)

        self.generic_visit(node)


def detect_errors(code: str):

    try:

        tree = ast.parse(code)

        detector = ErrorDetector()
        detector.visit(tree)

        report = []

        unused_vars = detector.defined_vars - detector.used_vars
        unused_imports = detector.imports - detector.used_vars

        if unused_vars:
            report.append(f"Unused variables: {', '.join(unused_vars)}")

        if unused_imports:
            report.append(f"Unused imports: {', '.join(unused_imports)}")

        if detector.infinite_loops:
            report.append("Infinite loop detected")

        if detector.long_functions:
            report.append("Very long functions detected")

        if not report:
            report.append("No major errors detected.")

        return report

    except Exception as e:

        return [f"Error while analyzing: {str(e)}"]
    