# Implementation Guide: Mutual Fund FAQ Assistant

## Overview
This document outlines the concrete implementation steps and technology stack for building the Mutual Fund FAQ Assistant based on the `architecture.md`.

## Technology Stack (Proposed)
*   **Language:** Python 3.10+
*   **Backend Framework:** FastAPI (for a lightweight API)
*   **Frontend UI:** Streamlit or basic HTML/JS (for the minimal UI)
*   **LLM Orchestration:** LangChain or LlamaIndex
*   **Vector Database:** ChromaDB or FAISS (local, lightweight options)
*   **Embedding Model:** `BAAI/bge-small-en-v1.5` (free, high-performance, local via HuggingFace) or Google `models/embedding-001` (free tier via Gemini API)
*   **Generative LLM:** `llama3-8b-8192` or `mixtral-8x7b-32768` accessed via Groq API (free, ultra-fast inference, running at `temperature=0.0` for determinism)

## Implementation Steps

### Phase 1: Data Ingestion & Offline Processing (The Corpus)
1.  **Web Scraping & Loading:**
    *   Use `BeautifulSoup` or `LangChain WebBaseLoader` to scrape the text from the 5 specified Tata Mutual Fund URLs.
    *   Extract the main content, explicitly ignoring navigation menus, generic footers, and ads.
2.  **Chunking Strategy:**
    *   Use **Semantic Chunking** (`SemanticChunker` from LangChain).
    *   This splits the document based on semantic similarity of sentences, ensuring that logically related facts (e.g., expense ratios, exit loads) stay within the same chunk regardless of length constraints.
3.  **Embedding & Indexing:**
    *   Generate embeddings for each chunk.
    *   Store chunks in the Vector DB with strict metadata: `{"source_url": "...", "last_updated": "YYYY-MM-DD", "scheme_name": "..."}`.
4.  **Daily Data Refresh:**
    *   Set up a scheduled task (e.g., cron job or Windows Task Scheduler) to automatically run the data ingestion script (`ingest.py`) daily at 10:00 AM IST to ensure the knowledge base stays updated.

### Phase 2: Intent Classification & Refusal Handling (The Guardrail)
1.  **Build the Classifier:**
    *   Create a pre-retrieval validation step.
    *   *Approach 1 (Rules):* Regex/keyword matching for trigger words like "should I", "recommend", "best fund", "compare", "better".
    *   *Approach 2 (LLM Route):* A fast classification prompt: *"Categorize this query as FACTUAL or ADVICE."*
2.  **Implement Refusal Logic:**
    *   If the query is classified as `ADVICE` or `NON-FACTUAL`, instantly return the fallback template: 
    *"I am a facts-only assistant and cannot provide investment advice or recommendations. Please consult a registered financial advisor or visit [AMFI Investor Corner](https://www.amfiindia.com/investor-corner) for educational resources."*

### Phase 3: Retrieval Engine
1.  **Query Embedding:** Convert the valid user input into a vector using the chosen embedding model.
2.  **Top-K Retrieval:** Query the Vector DB to fetch the top 3-5 most semantically similar chunks.

### Phase 4: LLM Generation
1.  **Strict Prompt Construction:** Implement the following system prompt:
    ```text
    You are a strictly facts-only Mutual Fund assistant. 
    Using ONLY the context provided below, answer the user's question in a maximum of 3 sentences.
    Do NOT provide any investment advice, opinions, or performance comparisons.
    If the answer is not contained within the context, state "I do not have the verified information to answer this query."
    
    Context: {retrieved_chunks}
    
    User Query: {user_query}
    ```
2.  **LLM Execution:** Execute the model call.

### Phase 5: Post-Processing & Citation
1.  **Citation Extraction:** Read the metadata of the retrieved chunk(s) used by the LLM.
2.  **Response Formatting:** Append the mandatory footer to the LLM's raw response.
    *   Format: `\n\nLast updated from sources: <date> - <Source URL>`

### Phase 6: Minimal UI Integration
1.  **Streamlit App Setup:** Create a simple `app.py`.
2.  **UI Elements:**
    *   Header: "Mutual Fund FAQ Assistant"
    *   Disclaimer banner (highly visible): **"Facts-only. No investment advice."**
    *   3 Example Prompt Buttons (e.g., "What is the exit load for Tata Gold ETF?").
    *   Chat input box and conversation history display.
