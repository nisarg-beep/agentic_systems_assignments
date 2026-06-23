from pathlib import Path
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI , GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough


DATA_DIR=Path("/Users/khushijain/Desktop/iitr /agentic_systems_assignments/langchain-rag/documents")
CHROMA_DIR=Path("/Users/khushijain/Desktop/iitr /agentic_systems_assignments/langchain-rag/chroma-db")
COLLECTION_NAME="hostel_policy_docs"
EMBEDDING_MODEL="gemini-embedding-001"
MODEL_NAME="gemini-2.5-flash"


embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

vector_store= Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR)
)

llm= ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0
)

retriever= vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k" : 3}
)

prompt = ChatPromptTemplate.from_template(
     """
    You are a helpful customer-support assistant for an e-commerce company.

    Use ONLY the retrieved context to answer the user's question.

    Rules:
    1. If the answer is present in the context, answer clearly.
    2. If the answer is not present in the context, say: "I don't know based on the provided documents."
    3. Do not use outside knowledge.
    4. Mention the source file name wherever possible.
    5. Keep the answer concise and practical.

    <context>
    {context}
    </context>

    Question:
    {query}

    Answer:
    """
)

rag_chain=(
    {
        "context": retriever,
        "query" : RunnablePassthrough(),
    }
    | prompt
    | llm 
    | StrOutputParser()
)


def main():
    queries= [
        "What are the quiet hours on weekdays?",
        "What is the scholarship amount for hostel residents?"
    ]

    for item , query in enumerate(queries , start=1):
        response = rag_chain.invoke(query)

        print(f"Q{item}: {query}")
        print(f"A{item}: {response}")
        print("===========")

if __name__ == "__main__":
    main()