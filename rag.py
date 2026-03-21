# ==============================
# 📦 IMPORTS
# ==============================

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from HF_KEY import query_hf


# ==============================
# 🤖 LOAD MODEL (ONCE)
# ==============================

model = SentenceTransformer('all-MiniLM-L6-v2')


# ==============================
# 🔹 1. CHUNKING
# ==============================

def create_chunks(transcript, chunk_size=300, overlap=100):
    chunks = []
    current_chunk = ""
    start_time = None

    for entry in transcript:
        text = entry["text"]

        # set start time for chunk
        if start_time is None:
            start_time = entry["start"]

        # add text
        current_chunk += " " + text

        # if chunk is large enough → save it
        if len(current_chunk.split()) >= chunk_size:
            chunks.append({
                "text": current_chunk.strip(),
                "start": start_time
            })
            current_chunk = ""
            start_time = None

    # add remaining chunk
    if current_chunk:
        chunks.append({
            "text": current_chunk.strip(),
            "start": start_time
        })

    return chunks


# ==============================
# 🔹 2. EMBEDDINGS
# ==============================

def create_embeddings(chunks):
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts)
    return np.array(embeddings)


# ==============================
# 🔹 3. FAISS INDEX
# ==============================

def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]  # usually 384

    index = faiss.IndexFlatL2(dimension)  # L2 distance
    index.add(embeddings)

    return index


# ==============================
# 🔹 4. RETRIEVAL
# ==============================

def retrieve_chunks(query, index, chunks, k=5):
    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), k)

    results = []
    for idx in indices[0]:
        results.append(chunks[idx])

    return results


# ==============================
# 🔹 5. PROMPT BUILDING
# ==============================

def build_prompt(chunks, query):
    chunks = chunks[:3]  # 🔥 MUST LIMIT

    context = "\n\n".join([c["text"] for c in chunks])

    return f"""
You are an AI assistant.

Answer ONLY from the context below.
If the answer is not present, say "Not in video".

Context:
{context}

Question:
{query}
"""

    return prompt


# ==============================
# 🔹 6. FINAL ANSWER GENERATION
# ==============================

def generate_answer(query, index, chunks):
    retrieved = retrieve_chunks(query, index, chunks)

    prompt = build_prompt(retrieved, query)

    answer = query_hf(prompt)

    return answer, retrieved