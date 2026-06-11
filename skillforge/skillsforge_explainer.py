from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser 


llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash"
)

prompt = PromptTemplate.from_template(
    """
    Explain the {topic} to the {audience} in a very {tone} tone within the {limit} words.

    Requirements:
    - Use {tone} tone.
    - Give one real-life analogy to explain the concept.
    - Keep the response within {limit} words.
    """
)

parser = StrOutputParser()

chain = prompt | llm | parser

lesson_brief =[
    {
        "topic" : "SQL indexes",
        "audience" : "beginners",
        "tone": "simple",
        "limit":"120"
    },
    {
        "topic" : "FastAPI dependency injection",
        "audience" : "intermediate developers",
        "tone": "technical",
        "limit":"180"
    },
    {
        "topic" : "LangChain PromptTemplate",
        "audience" : "product managers",
        "tone": "friendly",
        "limit":"100"
    },
]


def validate_brief(brief):
    if "topic" not in brief:
        raise ValueError("No topic present")

    if "audience" not in brief:
        raise ValueError("No audience given")

    if "tone" not in brief:
        raise ValueError("No tone given")

    if "limit" not in brief:
        raise ValueError("No limit given")

    if not brief["limit"].isdigit():
        raise ValueError("Limit must be a digit string")
    
for brief in lesson_brief:
    print (f"====Lesson {brief['topic']} ====")
    validate_brief(brief)
    result = chain.invoke(brief)
    print (result)
    print (f"Length : {len(result)} characters")
