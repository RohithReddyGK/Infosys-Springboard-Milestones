from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

model = ChatGroq(
    model="llama-3.1-8b-instant"
)

prompt = PromptTemplate.from_template(
"""
You are an experienced AI teacher.

Analyze the following Python code and give suggestions.

Explain:
1. Code improvements
2. Possible errors
3. Time complexity
4. Space complexity
5. Best practices

Code:
{code}
"""
)


def get_ai_suggestions(code: str):

    try:

        formatted_prompt = prompt.format(code=code)

        result = model.invoke(formatted_prompt)

        return result.content

    except Exception as e:

        return f"AI Suggestion Error: {str(e)}"
    