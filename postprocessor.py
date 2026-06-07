class PostProcessor:
    def format_response(self, raw_answer: str, retrieved_docs: list) -> str:
        """
        Appends the mandatory citation footer to the generated answer.
        Reads the metadata from the top retrieved chunk.
        
        Args:
            raw_answer: The string output from the LLM.
            retrieved_docs: The list of LangChain documents retrieved.
        Returns:
            The final formatted string with the citation footer.
        """
        # If no documents were retrieved or the LLM indicated it couldn't find the answer
        if not retrieved_docs or "I do not have the verified information" in raw_answer:
            return raw_answer
            
        # Extract metadata from the primary (most relevant) document
        primary_doc = retrieved_docs[0]
        source_url = primary_doc.metadata.get("source_url", "Unknown Source")
        last_updated = primary_doc.metadata.get("last_updated", "Unknown Date")
        
        # Append the mandatory footer
        footer = f"\n\nLast updated from sources: {last_updated} - {source_url}"
        final_response = raw_answer.strip() + footer
        
        return final_response

# Example Usage
if __name__ == "__main__":
    from retriever import Retriever
    from generator import Generator
    
    try:
        # 1. Initialize pipeline components
        retriever = Retriever(k=3)
        generator = Generator()
        postprocessor = PostProcessor()
        
        # 2. Define Query
        test_query = "What is the exit load for Tata Gold ETF?"
        print(f"Testing Post-Processing with query: '{test_query}'\n")
        
        # 3. Retrieve & Generate
        docs = retriever.retrieve(test_query)
        raw_answer = generator.generate(test_query, docs)
        
        # 4. Post-Process
        final_answer = postprocessor.format_response(raw_answer, docs)
        
        print("--- Final Formatted Response ---")
        print(final_answer)
        print("--------------------------------")
        
    except Exception as e:
        print(f"Error during testing: {e}")
