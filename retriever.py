from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

class Retriever:
    def __init__(self, persist_directory="./chroma_db", k=4):
        """
        Initializes the Retrieval Engine.
        Args:
            persist_directory: Path to the ChromaDB directory.
            k: Number of documents to retrieve.
        """
        self.persist_directory = persist_directory
        self.k = k
        
        # Load the same embedding model used during ingestion
        self.embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        
        # Load the vector store from the local directory
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        
        # Configure the retriever
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": self.k})

    def retrieve(self, query: str):
        """
        Retrieves the top k most semantically similar chunks for the given query.
        Returns a list of LangChain Document objects.
        """
        # invoke is the recommended method in newer LangChain versions instead of get_relevant_documents
        try:
            docs = self.retriever.invoke(query)
        except AttributeError:
            # Fallback for older Langchain versions
            docs = self.retriever.get_relevant_documents(query)
        return docs

# Example Usage
if __name__ == "__main__":
    retriever = Retriever(k=3)
    
    test_query = "What is the exit load for Tata Gold ETF?"
    print(f"Testing Retrieval Engine with query: '{test_query}'\n")
    
    retrieved_docs = retriever.retrieve(test_query)
    
    if not retrieved_docs:
        print("No documents retrieved.")
    else:
        for i, doc in enumerate(retrieved_docs, 1):
            print(f"--- Document {i} ---")
            print(f"Source: {doc.metadata.get('source_url', 'N/A')}")
            print(f"Last Updated: {doc.metadata.get('last_updated', 'N/A')}")
            print(f"Content Snippet: {doc.page_content[:250]}...\n")
