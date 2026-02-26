from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant")

code_string = """
def calculate_sum(a,b):
    result = a + b
    if result > 10:
        print("Greater than 10")
    else:
        print("Less than or equal to 10")
    return result
"""
prompt = PromptTemplate.from_template("""You are an experienced AI teacher, so generate the suggestions based on the given code for the student. Also, not just only giving suggestions but also give information about why are you suggesting this, for e.g., if you are suggesting to remove, then explain the reason for removal. In the suggestion, even explain the error along with time complexity, space comlexity and etc."
                        Code: {code_string}""")

def get_ai_suggestions(code_string):
    formatted_promt = prompt.format(code_string=code_string)
    result = model.invoke(formatted_promt)
    print(result.content)

get_ai_suggestions(code_string)
