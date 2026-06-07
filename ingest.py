import os
import datetime
from langchain_community.document_loaders import WebBaseLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# List of URLs to ingest (from ProblemStatement.md)
urls = [
    "https://groww.in/mutual-funds/tata-gold-etf-fof-direct-growth",
    "https://groww.in/mutual-funds/tata-silver-etf-fof-direct-growth",
    "https://groww.in/mutual-funds/tata-small-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/tata-multicap-fund-direct-growth",
    "https://groww.in/mutual-funds/tata-mid-cap-direct-plan-growth"
]

def clean_scheme_name(url):
    # Extract scheme name from URL
    parts = url.split('/')
    name = parts[-1].replace('-', ' ').title()
    return name

def main():
    print("Starting Phase 1: Data Ingestion...")
    
    # 1. Web Scraping & Loading
    docs = []
    for url in urls:
        print(f"Loading URL: {url}")
        loader = WebBaseLoader(url)
        loaded_docs = loader.load()
        
        # Add strict metadata
        scheme_name = clean_scheme_name(url)
        today = datetime.date.today().strftime("%Y-%m-%d")
        
        for doc in loaded_docs:
            doc.metadata["source_url"] = url
            doc.metadata["last_updated"] = today
            doc.metadata["scheme_name"] = scheme_name
            # Remove complex source structure if loaded
            if "source" in doc.metadata:
                del doc.metadata["source"]
        
        docs.extend(loaded_docs)
    
    print(f"Loaded {len(docs)} initial documents.")
    
    # 2. Initialize Embeddings (needed for Semantic Chunking)
    print("Initializing embedding model (BAAI/bge-small-en-v1.5)...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

    # 3. Chunking Strategy
    print("Chunking documents using Semantic Chunking...")
    text_splitter = SemanticChunker(embeddings)
    splits = text_splitter.split_documents(docs)
    print(f"Created {len(splits)} chunks.")

    # 4. Indexing
    
    persist_directory = "./chroma_db"
    print(f"Storing embeddings in ChromaDB at {persist_directory}...")
    
    # Chroma DB initialization
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    # vectorstore.persist() is deprecated in newer chromadb versions, 
    # it persists automatically if persist_directory is provided.
    
    print("Ingestion complete. Vector DB saved successfully.")

if __name__ == "__main__":
    main()
