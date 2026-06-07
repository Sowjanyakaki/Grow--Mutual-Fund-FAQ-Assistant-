import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()

class Generator:
    def __init__(self, model_name="llama-3.1-8b-instant"):
        """
        Initializes the LLM Generation Engine.
        Args:
            model_name: The name of the Groq model to use.
        """
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            print("Warning: GROQ_API_KEY is missing or invalid in .env. Generation will fail if invoked.")
            api_key = "dummy_key_to_allow_init"

        self.llm = ChatGroq(
            temperature=0,  # Zero temperature for deterministic, factual responses
            model_name=model_name,
            api_key=api_key
        )

        # Strict Prompt Construction from implementation.md
        template = """
You are a strictly facts-only Mutual Fund assistant. 
Using ONLY the context provided below, answer the user's question in a maximum of 3 sentences.
Do NOT provide any investment advice, opinions, or performance comparisons.
If the answer is not contained within the context, state "I do not have the verified information to answer this query."

Context: {retrieved_chunks}

User Query: {user_query}
"""
        self.prompt = PromptTemplate(
            input_variables=["retrieved_chunks", "user_query"],
            template=template
        )
        
        self.chain = self.prompt | self.llm

    def generate(self, user_query: str, retrieved_docs: list) -> str:
        """
        Generates an answer based on the retrieved documents.
        Args:
            user_query: The user's original question.
            retrieved_docs: A list of LangChain Document objects from the retriever.
        Returns:
            The generated string answer.
        """
        # Combine the content of all retrieved chunks into a single string
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        
        # Truncate context to ~6000 characters (approx 1500 tokens) to stay well below 
        # Groq's 6000 TPM free tier limit, leaving room for the query and response.
        if len(context) > 6000:
            context = context[:6000] + "\n...[truncated]"
        
        # Execute the model call
        response = self.chain.invoke({
            "retrieved_chunks": context,
            "user_query": user_query
        })
        
        return response.content.strip()

# Example Usage (assuming you have retriever.py available)
if __name__ == "__main__":
    from retriever import Retriever
    
    # 1. Initialize dependencies
    try:
        generator = Generator()
        retriever = Retriever(k=3)
        
        # 2. Test query
        test_query = "What is the exit load for Tata Gold ETF?"
        print(f"Testing Generator with query: '{test_query}'")
        print("Retrieving context...\n")
        
        # 3. Retrieve context
        docs = retriever.retrieve(test_query)
        
        # 4. Generate answer
        print("Generating answer...\n")
        answer = generator.generate(test_query, docs)
        
        print("--- Generated Answer ---")
        print(answer)
        print("------------------------")
        
    except Exception as e:
        print(f"Error during testing: {e}")
