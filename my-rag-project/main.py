import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="Dynamic RAG", layout="wide")
st.title("📁 Instant PDF RAG")

MODEL_NAME = "llama3.2:3b"
OLLAMA_URL = "http://host.docker.internal:11434"

# 1. Sidebar for File Upload
with st.sidebar:
    st.header("Upload Documents")
    uploaded_file = st.file_uploader("Upload a PDF to start chatting", type="pdf")

    # NEW: Clear button to manually reset
    if st.button("Clear All Data"):
        st.session_state.clear()
        st.rerun()


# 2. RAG Processing Logic
def process_document(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file.getvalue())
        tmp_path = tmp_file.name

    try:
        loader = PyPDFLoader(tmp_path)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(docs)

        embeddings = OllamaEmbeddings(model=MODEL_NAME, base_url=OLLAMA_URL)
        # Using a fresh Chroma instance every time
        vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings)

        template = """Answer based ONLY on context: {context}\nQuestion: {question}"""
        prompt = ChatPromptTemplate.from_template(template)
        llm = ChatOllama(model=MODEL_NAME, base_url=OLLAMA_URL, temperature=0)

        return ({"context": vector_db.as_retriever(), "question": RunnablePassthrough()}
                | prompt | llm | StrOutputParser())
    finally:
        os.remove(tmp_path)


# 3. Main Logic with "File Change Detection"
if uploaded_file:
    # IF the file name changes, clear the old chain and history
    if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:
        with st.spinner(f"Processing new file: {uploaded_file.name}..."):
            st.session_state.rag_chain = process_document(uploaded_file)
            st.session_state.current_file = uploaded_file.name
            st.session_state.messages = []  # Reset chat for the new document
            st.success("New document indexed!")

    # Display Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_query := st.chat_input("Ask about this specific document..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            response = st.session_state.rag_chain.invoke(user_query)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("👈 Please upload a PDF in the sidebar to begin.")   