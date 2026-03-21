# 🎥 YouTube AI Assistant (RAG-based)

An AI-powered assistant that allows users to ask questions about any YouTube video.  
Built using Retrieval-Augmented Generation (RAG), it extracts video transcripts, processes them, and generates accurate answers using LLMs.

---

## 🚀 Features

- 🔗 Input any YouTube video URL  
- 🧠 Ask questions about the video  
- ⚡ Fast semantic search using FAISS  
- 🤖 LLM-powered answers (Hugging Face)  
- 💬 Chat-based interface (Streamlit)  
- 🔄 Maintains conversation history  

---

## 🧠 How It Works (RAG Pipeline)
User Query
↓
Transcript Extraction
↓
Chunking
↓
Embeddings (Sentence Transformers)
↓
FAISS Vector Search
↓
Relevant Context Retrieval
↓
LLM (Hugging Face)
↓
Final Answer
## 🛠️ Tech Stack

- Python  
- Streamlit  
- FAISS  
- Sentence Transformers  
- Hugging Face Inference API  
- YouTube Transcript API
demo url = https://youtube-ai-study-assistant-q6ypzvrztedlsyubgljhhs.streamlit.app/
