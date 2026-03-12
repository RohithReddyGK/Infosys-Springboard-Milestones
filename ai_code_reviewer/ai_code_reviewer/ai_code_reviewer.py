import reflex as rx

from ai_code_reviewer.code_parser import parse_code
from ai_code_reviewer.error_detector_visitor import detect_errors
from ai_code_reviewer.ai_suggestor import get_ai_suggestions


# ---------------------------
# STATE
# ---------------------------

class CodeState(rx.State):

    code_input: str = ""
    result: str = ""

    def set_code_input(self, value: str):
        self.code_input = value

    def analyze_code(self):

        if self.code_input.strip() == "":
            self.result = "⚠ Please paste Python code."
            return

        # AST Parsing
        parse_result = parse_code(self.code_input)

        if not parse_result["success"]:
            self.result = parse_result["error"]
            return

        ast_feedback = "\n".join(parse_result["feedback"])

        # Error Detection
        errors = detect_errors(self.code_input)
        error_feedback = "\n".join(errors)

        # AI Suggestions
        ai_feedback = get_ai_suggestions(self.code_input)

        # Combine results
        self.result = f"""
================ AST ANALYSIS ================

{ast_feedback}

================ ERROR DETECTOR ================

{error_feedback}

================ AI SUGGESTIONS ================

{ai_feedback}
"""


# ---------------------------
# NAVBAR
# ---------------------------

def navbar():

    return rx.hstack(

        rx.hstack(
            rx.icon("cpu"),
            rx.text(
                "AI Code Reviewer",
                font_weight="bold",
                font_size="20px"
            ),
            spacing="2",
        ),

        rx.spacer(),

        rx.hstack(
            rx.link("Home", href="/"),
            rx.link("Analyze Code", href="/analyze"),
            rx.link("About", href="/about"),
            spacing="6",
        ),

        padding="20px",
        width="100%",
        border_bottom="1px solid #ddd"
    )


# ---------------------------
# ANALYZER PAGE
# ---------------------------

def analyzer_page():

    return rx.vstack(

        navbar(),

        rx.heading(
            "AI Code Analyzer",
            size="8"
        ),

        rx.text(
            "Paste Python code below and click analyze."
        ),

        rx.text_area(
            placeholder="Paste your Python code here...",
            value=CodeState.code_input,
            on_change=CodeState.set_code_input,
            width="80%",
            height="300px",
        ),

        rx.button(
            "Analyze Code",
            on_click=CodeState.analyze_code,
            color_scheme="blue",
            margin_top="20px"
        ),

        rx.divider(),

        rx.heading("Analysis Result", size="6"),

        rx.box(
            rx.text(
                CodeState.result,
                white_space="pre-wrap"
            ),
            padding="20px",
            border="1px solid #ccc",
            border_radius="10px",
            width="80%"
        ),

        align="center",
        spacing="5",
        padding="40px"
    )


# ---------------------------
# HOME PAGE
# ---------------------------

def home():

    return rx.center(

        rx.vstack(

            navbar(),

            rx.heading(
                "AI Driven Code Reviewer",
                size="9"
            ),

            rx.text(
                "Analyze Python code using AST parsing, error detection, and AI suggestions."
            ),

            rx.button(
                "Start Code Analysis",
                on_click=rx.redirect("/analyze"),
                color_scheme="blue",
                size="3"
            ),

            spacing="6",
            align="center",
        ),

        height="80vh"
    )


# ---------------------------
# ABOUT PAGE
# ---------------------------

def about():

    return rx.center(

        rx.vstack(

            navbar(),

            rx.heading("About This Project"),

            rx.text(
                "This system analyzes Python code using AST parsing, "
                "detects possible issues, and provides AI suggestions."
            ),

            spacing="5",
            align="center"
        ),

        height="80vh"
    )


# ---------------------------
# APP
# ---------------------------

app = rx.App()

app.add_page(home, route="/")
app.add_page(analyzer_page, route="/analyze")
app.add_page(about, route="/about")
