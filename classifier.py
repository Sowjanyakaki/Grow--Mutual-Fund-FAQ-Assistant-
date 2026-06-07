import re
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Load environment variables (e.g., GROQ_API_KEY)
load_dotenv()

# Fallback response for non-factual queries
REFUSAL_MESSAGE = (
    "I am a facts-only assistant and cannot provide investment advice or recommendations. "
    "Please consult a registered financial advisor or visit "
    "[AMFI Investor Corner](https://www.amfiindia.com/investor-corner) for educational resources."
)

class IntentClassifier:
    def __init__(self, use_llm=True):
        self.use_llm = use_llm
        
        # Rule-based trigger words indicating subjective/advisory intent
        self.trigger_patterns = [
            r"\bshould i\b",
            r"\brecommend\b",
            r"\bbest fund\b",
            r"\bcompare\b",
            r"\bbetter\b",
            r"\bgood investment\b",
            r"\badapt\b",
            r"\bsuggest\b",
            r"\bpredict\b",
            r"\bfuture\b"
        ]
        
        # Initialize Groq LLM for fast classification if enabled
        if self.use_llm:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key or api_key == "your_groq_api_key_here":
                print("Warning: GROQ_API_KEY is missing or invalid in .env. Falling back to rule-based classification.")
                self.use_llm = False
            else:
                try:
                    self.llm = ChatGroq(
                        temperature=0, 
                        model_name="llama-3.1-8b-instant", 
                        api_key=api_key
                    )
                    self.classification_prompt = PromptTemplate(
                        input_variables=["query"],
                        template="""
You are an intent classifier for a strictly factual Mutual Fund assistant.
Categorize the user query as either "FACTUAL" or "ADVICE".

Rules:
1. "FACTUAL": The query asks for objective, verifiable data (e.g., "What is the exit load?", "What is the expense ratio?").
2. "ADVICE": The query asks for opinions, recommendations, comparisons, or predictions (e.g., "Should I invest?", "Is this a good fund?", "Compare these funds").

User Query: "{query}"

Output only a single word: FACTUAL or ADVICE.
"""
                    )
                    self.chain = self.classification_prompt | self.llm
                except Exception as e:
                    print(f"Warning: Failed to initialize Groq LLM for classification. Using rule-based only. Error: {e}")
                    self.use_llm = False

    def check_rules(self, query: str) -> bool:
        """Returns True if the query appears factual based on rules, False if it looks like advice."""
        query_lower = query.lower()
        for pattern in self.trigger_patterns:
            if re.search(pattern, query_lower):
                return False # Triggered an advice rule
        return True

    def check_llm(self, query: str) -> bool:
        """Returns True if LLM classifies as FACTUAL, False if ADVICE."""
        try:
            response = self.chain.invoke({"query": query})
            result = response.content.strip().upper()
            return "FACTUAL" in result
        except Exception as e:
            print(f"LLM Classification failed, falling back to True: {e}")
            return True

    def is_factual(self, query: str) -> tuple[bool, str]:
        """
        Main entry point. Evaluates the query.
        Returns:
            (is_valid: bool, response: str)
            If is_valid is False, response contains the refusal message.
            If is_valid is True, response is empty.
        """
        # 1. Fast Rule-Based Check
        if not self.check_rules(query):
            return False, REFUSAL_MESSAGE
            
        # 2. LLM-Based Check (Secondary Guardrail)
        if self.use_llm:
            if not self.check_llm(query):
                return False, REFUSAL_MESSAGE
                
        return True, ""

# Example Usage
if __name__ == "__main__":
    classifier = IntentClassifier(use_llm=True)
    
    test_queries = [
        "What is the exit load for Tata Gold ETF?",
        "Should I invest my money in Tata Small Cap Fund?",
        "What is the expense ratio?",
        "Which fund is better for long term?"
    ]
    
    for q in test_queries:
        valid, msg = classifier.is_factual(q)
        print(f"\nQuery: '{q}'")
        if valid:
            print("-> Result: PASS (Proceed to Retrieval)")
        else:
            print(f"-> Result: REFUSED\nReason/Message: {msg}")
