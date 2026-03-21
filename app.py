import streamlit as st
from transcript_youtube import get_transcript
from rag import (
    create_chunks,
    create_embeddings,
    create_faiss_index,
    generate_answer
)

# ==============================
# 🎨 PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="YouTube AI Assistant",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 YouTube AI Assistant")
st.markdown("Ask questions about any YouTube video")

# ==============================
# 📦 SESSION STATE
# ==============================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "index" not in st.session_state:
    st.session_state.index = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None


# ==============================
# 🔗 INPUT URL
# ==============================

url = st.text_input("Enter YouTube Video URL")

if st.button("Process Video"):

    with st.spinner("Fetching transcript..."):
        data = get_transcript(url)

    if isinstance(data, dict):
        st.error(data["error"])
    else:
        with st.spinner("Processing video..."):
            chunks = create_chunks(data)
            embeddings = create_embeddings(chunks)
            index = create_faiss_index(embeddings)

        # store in session
        st.session_state.index = index
        st.session_state.chunks = chunks
        st.session_state.chat_history = []  # reset chat

        st.success("✅ Video processed successfully!")


# ==============================
# 📜 DISPLAY CHAT HISTORY
# ==============================

for role, message in st.session_state.chat_history:
    st.chat_message(role).write(message)


# ==============================
# 💬 CHAT INTERFACE
# ==============================

if st.session_state.index is not None:

    query = st.chat_input("Ask a question about the video...")

    if query:
        # Save user message
        st.session_state.chat_history.append(("user", query))

        with st.spinner("Thinking..."):
            answer, _ = generate_answer(
                query,
                st.session_state.index,
                st.session_state.chunks
            )

        # Save assistant response
        st.session_state.chat_history.append(("assistant", answer))

        # Rerun to refresh UI immediately
        st.rerun()