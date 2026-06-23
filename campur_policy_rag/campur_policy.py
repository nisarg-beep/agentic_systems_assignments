import os
import re
import uuid
import chromadb

from pypdf import PdfReader
from google import genai



PDF_FOLDER = "policy_documents"
 


EMBEDDING_MODEL = "gemini-embedding-001"
LLM_MODEL = "gemini-2.5-flash"

CHUNK_SIZE = 150
OVERLAP = 20



client = genai.Client()


chroma_client = chromadb.PersistentClient("./campus_policy_db")


collection = chroma_client.get_or_create_collection(
    name="campus_policies",
    embedding_function=None
)


def infer_policy_type(filename):

    filename = filename.lower()

    if "hostel" in filename:
        return "hostel"

    elif "refund" in filename:
        return "refund"

    elif "library" in filename:
        return "library"

    elif "withdrawal" in filename:
        return "course_withdrawal"

    return "general"

def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()

def load_pdf_documents(folder_path):

    documents = []

    for file_name in os.listdir(folder_path):

        if not file_name.endswith(".pdf"):
            continue

        file_path = os.path.join(folder_path, file_name)

        reader = PdfReader(file_path)

        print(f"Loaded {len(reader.pages)} pages from: {file_name}")

        for page_number, page in enumerate(reader.pages):

            raw_text = page.extract_text()

            if not raw_text:
                continue

            cleaned_text = clean_text(raw_text)

            documents.append({
                "text": cleaned_text,
                "source": file_name,
                "page": page_number + 1,
                "policy_type": infer_policy_type(file_name)
            })

    return documents

def split_text_into_chunks(
    text,
    chunk_size=CHUNK_SIZE,
    overlap=OVERLAP
):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk_words = words[start:end]

        chunk_text = " ".join(chunk_words)

        chunks.append(chunk_text)

        start += chunk_size - overlap

    return chunks


def generate_embedding(text):

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    embedding = response.embeddings[0].values

    return embedding

def build_knowledge_base():

    documents = load_pdf_documents(PDF_FOLDER)

    all_ids = []
    all_documents = []
    all_embeddings = []
    all_metadatas = []

    total_chunks = 0

    for document in documents:

        chunks = split_text_into_chunks(document["text"])

        for chunk in chunks:

            embedding = generate_embedding(chunk)

            chunk_id = str(uuid.uuid4())

            metadata = {
                "source_file": document["source"],
                "page_number": document["page"],
                "policy_type": document["policy_type"]
            }

            all_ids.append(chunk_id)
            all_documents.append(chunk)
            all_embeddings.append(embedding)
            all_metadatas.append(metadata)

            total_chunks += 1

    print(f"Total chunks created: {total_chunks}")

    
    # Remove old chunks if collection already exists
    existing_count = collection.count()

    if existing_count > 0:
        existing_ids = collection.get(include=[])["ids"]
        collection.delete(ids=existing_ids)

    collection.add(
        ids=all_ids,
        documents=all_documents,
        embeddings=all_embeddings,
        metadatas=all_metadatas
)

    print(
        f"Successfully stored {total_chunks} chunks in vector database."
    )


def retrieve_relevant_chunks(query, top_k=3):

    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved_chunks = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        retrieved_chunks.append({
            "text": document,
            "metadata": metadata,
            "distance": distance
        })

    print(f"Retrieved {len(retrieved_chunks)} relevant chunks.")

    return retrieved_chunks


def build_prompt(user_question, retrieved_chunks):

    context = ""

    for chunk in retrieved_chunks:

        context += f"""
Policy Type: {chunk['metadata']['policy_type']}
Source File: {chunk['metadata']['source_file']}
Page Number: {chunk['metadata']['page_number']}

Policy Text:
{chunk['text']}

"""

    prompt = f"""
You are a campus policy assistant.

Answer ONLY using the retrieved policy context.

Rules:
1. Do not use outside knowledge.
2. If the answer is missing from the context, say:
"I don't have that information."
3. Keep the answer short and student-friendly.

Student Question:
{user_question}

Retrieved Policy Context:
{context}

Answer:
"""

    return prompt


def generate_answer(prompt):

    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt
    )

    return response.text



def answer_question(user_question):

    print("\n" + "=" * 60)

    print(f"User Query: {user_question}")

    retrieved_chunks = retrieve_relevant_chunks(user_question)

    prompt = build_prompt(
        user_question,
        retrieved_chunks
    )

    answer = generate_answer(prompt)

    print(f"\nAnswer: {answer}")




if __name__ == "__main__":

    build_knowledge_base()

    test_questions = [

        "Can I get a refund after dropping a course?",

        "What is the deadline for returning a library book?",

        "Are hostel visitors allowed on weekends?",

        "Can students cook inside hostel rooms?",

        "What happens if I lose a library book?"
    ]

    for question in test_questions:

        answer_question(question)