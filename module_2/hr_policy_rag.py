from google import genai
import chromadb
from typing import List, Dict, Any

EMBEDDING_MODEL = "gemini-embedding-001"
GENERATION_MODEL = "gemini-2.5-flash"

client = genai.Client()

HR_POLICY_DOCUMENTS = [
    {
        "id": "leave_policy",
        "text": (
            "Employees are entitled to 24 paid leave days per year. "
            "Sick leave can be taken up to 10 days annually without prior approval. "
            "Unused annual leave can be carried forward up to 5 days to the next year. "
            "All planned leaves must be approved by the reporting manager at least 3 days in advance."
        ),
        "metadata": {
            "category": "leave",
            "source": "hr_leave_policy"
        }
    },
    {
        "id": "wfh_policy",
        "text": (
            "Employees are allowed to work from home up to 2 days per week depending on role eligibility. "
            "New joiners are eligible for WFH only after completing 3 months of service. "
            "All WFH requests must be approved by the manager in advance. "
            "Critical team meetings may require mandatory office attendance."
        ),
        "metadata": {
            "category": "wfh",
            "source": "hr_wfh_policy"
        }
    },
    {
        "id": "appraisal_policy",
        "text": (
            "Performance appraisals are conducted once every year in December. "
            "Employees are rated on a scale from 1 to 5 based on performance and contribution. "
            "Salary increments are directly linked to performance ratings. "
            "Final appraisal decisions are reviewed by both manager and HR committee."
        ),
        "metadata": {
            "category": "appraisal",
            "source": "hr_appraisal_policy"
        }
    },
    {
        "id": "conduct_policy",
        "text": (
            "Employees must maintain professional behavior at all times in the workplace. "
            "Sharing confidential company data with unauthorized persons is strictly prohibited. "
            "Any conflict of interest must be disclosed to HR immediately. "
            "Violation of code of conduct may result in disciplinary action including termination."
        ),
        "metadata": {
            "category": "conduct",
            "source": "hr_conduct_policy"
        }
    }
]


def create_embeddings(texts: List[str]) -> List[List[float]]:
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts
    )
    return [item.values for item in response.embeddings]


def setup_vector_database():
    chroma_client = chromadb.PersistentClient("./hr_chroma_db")

    collection = chroma_client.get_or_create_collection(
        name="hr_policy_collection",
        metadata={"hnsw:space": "cosine"},
        embedding_function=None
    )

    return collection


def index_hr_documents(collection):
    ids = [doc["id"] for doc in HR_POLICY_DOCUMENTS]
    documents = [doc["text"] for doc in HR_POLICY_DOCUMENTS]
    metadatas = [doc["metadata"] for doc in HR_POLICY_DOCUMENTS]

    embeddings = create_embeddings(documents)

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print(f"Indexed {len(HR_POLICY_DOCUMENTS)} HR policy documents")


# RETRIEVAL

def retrieve_hr_content(collection, query: str, top_k: int = 3):
    query_embedding = create_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": doc,
            "metadata": meta,
            "distance": dist
        })

    return chunks

# PROMPT BUILDER

def build_grounded_prompt(query: str, chunks: List[Dict[str, Any]]) -> str:
    context = ""

    for i, chunk in enumerate(chunks, start=1):
        context += f"\nPolicy Chunk {i} | {chunk['metadata']['source']}\n{chunk['text']}\n"

    return f"""
You are an HR assistant for a company.

Answer ONLY using the policy context below.

Rules:
- Do NOT guess or use outside knowledge.
- If answer is missing, say: "I do not have enough information in the provided HR policies."
- Be clear and concise.

Policy Context:
{context}

Employee Question:
{query}

Final Answer:
"""



def generate_answer(query: str, chunks: List[Dict[str, Any]]) -> str:
    prompt = build_grounded_prompt(query, chunks)

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt,
        config={
            "system_instruction": "You are a strict HR policy assistant."
        }
    )

    return response.text


def generate_answer_without_retrieval(query: str) -> str:
    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=query
    )
    return response.text


def answer_with_rag(collection, query: str, top_k: int = 3):
    chunks = retrieve_hr_content(collection, query, top_k)

    print("\n================ RETRIEVED CHUNKS ================")
    for i, c in enumerate(chunks, 1):
        print(f"\nChunk {i}")
        print(c["metadata"])
        print(c["distance"])
        print(c["text"])

    answer = generate_answer(query, chunks)
    return answer


def main():
    collection = setup_vector_database()
    index_hr_documents(collection)

    queries = [
        "How many leave days do I get in a year?",
        "Do I need approval for working from home?",
        "When is performance appraisal conducted and how is increment decided?"
    ]

    for q in queries:
        print("\n\n==============================")
        print("QUERY:", q)

        print("\n--- RAG ANSWER ---")
        print(answer_with_rag(collection, q))

    
    test_query = "Do I need approval before working from home?"

    print("\n\n================ NO RAG =================")
    print(generate_answer_without_retrieval(test_query))

    print("\n\n================ WITH RAG ================")
    print(answer_with_rag(collection, test_query))

if __name__ == "__main__":
    main()