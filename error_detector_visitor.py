import ast

# Example user code 
code = """
import os
import sys
from datetime import datetime, timedelta

score = 100

while True:
    print("Running...")

print(score)
"""

class ErrorDetector(ast.NodeVisitor):
    def __init__(self):
        self.defined_vars = set()
        self.used_vars = set()
        self.imports = set()
        self.used_imports = set()
        self.infinite_loops = []

    # Detect imports
    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports.add(name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports.add(name)
        self.generic_visit(node)

    # Detect variable usage
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.defined_vars.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.used_vars.add(node.id)

        self.generic_visit(node)

    # Detect infinite loops
    def visit_While(self, node):
        # Case 1: while True
        if isinstance(node.test, ast.Constant) and node.test.value is True:
            has_break = any(isinstance(n, ast.Break) for n in ast.walk(node))

            if not has_break:
                self.infinite_loops.append(node.lineno)

        self.generic_visit(node)

    # Final Report
    def report(self):
        unused_vars = self.defined_vars - self.used_vars
        unused_imports = self.imports - self.used_vars

        print("\n================ ERROR DETECTOR REPORT ================\n")

        # Unused Variables
        if unused_vars:
            print("⚠️ UNUSED VARIABLE(S) DETECTED:\n")
            for var in unused_vars:
                print(f"• Variable '{var}' is defined but never used.")
                print("  Explanation: The variable is assigned a value but not referenced later in the program.")
                print("  Suggestion: Remove the variable or use it in your logic.\n")

        # Unused Imports 
        if unused_imports:
            print("⚠️ UNUSED IMPORT(S) DETECTED:\n")
            for imp in unused_imports:
                print(f"• Import '{imp}' is not used anywhere in the code.")
                print("  Explanation: The module is imported but no function or object from it is used.")
                print("  Suggestion: Remove the unused import to improve code cleanliness and performance.\n")

        # Infinite Loops 
        if self.infinite_loops:
            print("🚨 INFINITE LOOP DETECTED:\n")
            for line in self.infinite_loops:
                print(f"• Infinite loop found at line {line}.")
                print("  Explanation: The loop condition is always True and there is no 'break' statement.")
                print("  This means the loop will never terminate on its own.")
                print("  Suggestion:")
                print("     - Add a 'break' statement inside the loop, OR")
                print("     - Change the loop condition to a proper terminating condition.\n")

        if not (unused_vars or unused_imports or self.infinite_loops):
            print("No issues detected!\n")

# Execution
try:
    tree = ast.parse(code)
    detector = ErrorDetector()
    detector.visit(tree)
    detector.report()
except SyntaxError as e:
    print("🚨 SYNTAX ERROR DETECTED")
    print(f"Line {e.lineno}: {e.msg}")
    print("Explanation: There is a syntax mistake in your code.")
    print("Suggestion: Check the indicated line and correct the syntax.")
