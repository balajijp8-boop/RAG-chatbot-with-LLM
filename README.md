# 🤖 Local-First RAG: Private Document Intelligence

A high-performance, **completely offline** Retrieval-Augmented Generation (RAG) system. This project enables users to upload PDF documents and have real-time, context-aware conversations with an LLM without their data ever leaving their local machine.

## 🌟 Key Features



https://github.com/user-attachments/assets/3ece8d00-2dc8-4408-b763-a65fab17a35c




* **100% Data Privacy:** Powered by **Ollama** and **Llama 3.2**, all processing happens locally on your hardware.
* **Dynamic Document Ingestion:** Uses **LangChain** and **ChromaDB** to instantly index uploaded PDFs and clear memory between different document sessions.
* **Modern UI:** A clean, reactive chat interface built with **Streamlit**.
* **Containerized Architecture:** Fully orchestrated with **Docker Compose** for easy deployment and environment isolation.

## 🏗️ Architecture

The system follows the standard RAG pattern but is optimized for local performance:

1. **Ingestion:** PDF text is extracted and split using `RecursiveCharacterTextSplitter`.
2. **Vectorization:** Text chunks are converted into mathematical embeddings via `llama3.2:3b`.
3. **Storage:** Vectors are stored in an in-memory **ChromaDB** instance.
4. **Retrieval:** The system performs a semantic search to find the top  relevant chunks for every user query.
5. **Generation:** The LLM synthesizes a final answer using only the retrieved context.

## 🛠️ Tech Stack

* **LLM:** Ollama (Llama 3.2:3b)
* **Orchestration:** LangChain (LCEL)
* **Frontend:** Streamlit
* **Vector Store:** ChromaDB
* **DevOps:** Docker, Docker Compose

## 🚀 Quick Start

### 1. Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
* [Ollama](https://ollama.com/) installed on your host machine.

### 2. Prepare Ollama

Since the app runs in Docker, you must allow Ollama to accept external connections. Open PowerShell as Admin and run:

```powershell
$env:OLLAMA_HOST="0.0.0.0"
ollama serve

```

### 3. Launch with Docker

```bash
docker compose up --build

```

### 4. Access the App

Open your browser to: **`http://localhost:8501`**

---

## 📈 Technical Challenges Overcome

* **Context Isolation:** Implemented a session-state tracking system to ensure that when a user swaps a PDF, the vector database is cleared and re-indexed, preventing "hallucinated" answers from previous documents.
* **Docker Networking:** Resolved the `host.docker.internal` bridge to allow the containerized application to communicate with the host-native GPU-accelerated Ollama service.
* **Asynchronous Processing:** Integrated Streamlit "Status" and "Spinner" components to handle the latency of local embedding generation, providing a smooth UX.
