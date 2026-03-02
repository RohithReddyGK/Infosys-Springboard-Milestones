import reflex as rx
import ast
from .error_detector_visitor import ErrorDetector  # Make sure class name matches yours


class State(rx.State):
    code_input: str = ""
    output: str = ""

    def analyze_code(self):
        if not self.code_input.strip():
            self.output = "⚠️ Please enter some Python code."
            return

        try:
            tree = ast.parse(self.code_input)
            detector = ErrorDetector()
            detector.visit(tree)

            results = []

            # Example checks (adjust according to your visitor class)
            if detector.imports - detector.used_imports:
                results.append("❌ Unused Imports Detected.")

            if detector.defined_vars - detector.used_vars:
                results.append("⚠️ Defined but Unused Variables Detected.")

            if not results:
                results.append("✅ No major issues detected.")

            self.output = "\n".join(results)

        except SyntaxError as e:
            self.output = f"❌ Syntax Error: {e}"
        except Exception as e:
            self.output = f"⚠️ Unexpected Error: {e}"


def index():
    return rx.container(
        rx.vstack(
            rx.heading("AI-Driven Code Reviewer", size="6"),

            rx.text_area(
                placeholder="Paste your Python code here...",
                value=State.code_input,
                on_change=State.set_code_input,
                height="300px",
                width="100%",
            ),

            rx.button(
                "Analyze Code",
                on_click=State.analyze_code,
                width="100%",
            ),

            rx.box(
                rx.text(State.output),
                padding="1em",
                border="1px solid #ccc",
                width="100%",
                min_height="150px",
                white_space="pre-wrap",
            ),

            spacing="4",
            width="60%",
        ),
        display="flex",
        justify_content="center",
        padding="2em",
    )


app = rx.App()
app.add_page(index)
