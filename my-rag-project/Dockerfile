FROM python:3.10-slim

WORKDIR /app

# Install dependencies including streamlit
RUN pip install --no-cache-dir \
    langchain \
    langchain-community \
    langchain-ollama \
    langchain-core \
    chromadb \
    pypdf \
    streamlit

COPY . .

# Expose the port Streamlit uses
EXPOSE 8501

# Command to run Streamlit instead of raw python
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]