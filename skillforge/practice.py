# this is practice file for langchain introduction concepts. in this we have covered how to use prompt templates , chains and the other conecpts of langchain. 

# from langchain_core.prompts import PromptTemplate
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.output_parsers import StrOutputParser

# llm = ChatGoogleGenerativeAI(
#     model = "gemini-2.5-flash"
# )

# prompt = PromptTemplate.from_template (
#     """
#     Explain {topic} to the {audience} in a {tone} tone
#     Requirements:
#     -Use {tone} tone
#     -Use one Real-life analogy 
#     -Keep the respone in {limit} words
#     """
# )

# # replacing variables with actual values
# values = prompt.format(
#     topic = "Langchain components",
#     tone = "simple",
#     audience ="professionals",
#     limit=100
# )

# result = llm.invoke(values)
# print (result)

# we have succesfully over viewed the implementation of langchain components and the methods of how to use them now there is a slight difference between two methods .  In this method we are just give me the values to the llm directly and it prints the result with all the metadata instead we can print the output in the string format so lets go through that method as well. 

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash"
)

prompt = PromptTemplate.from_template (
    """
    Explain {topic} to the {audience} in a {tone} tone
    Requirements:
    -Use {tone} tone
    -Use one Real-life analogy 
    -Keep the respone in {limit} words
    """
)

output = StrOutputParser()
chain = prompt | llm | output 


result = chain.invoke ({
    "topic" : "Langchain components",
    "tone": "simple",
    "audience" : "professionals",
    "limit":100
})
print (result)
