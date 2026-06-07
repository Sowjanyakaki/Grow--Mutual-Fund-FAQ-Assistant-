# Edge Cases & Limitations: Mutual Fund FAQ Assistant

This document outlines potential edge cases, limitations, and failure scenarios for the Mutual Fund RAG Assistant, along with strategies to handle them.

## 1. Ambiguous Queries
*   **Scenario:** A user asks, "What is the expense ratio?" without specifying which Tata Mutual Fund scheme they are asking about.
*   **Expected System Behavior:** The retrieval engine might fetch chunks from multiple different funds. The LLM might combine them incorrectly or pick a random one.
*   **Mitigation Strategy:** 
    *   Implement an entity extraction step before retrieval. 
    *   If no specific scheme is detected, the LLM prompt should instruct it to ask for clarification: *"Please specify which Mutual Fund scheme you are asking about (e.g., Tata Gold ETF, Tata Small Cap Fund)."*

## 2. Stealthy Advice-Seeking (Prompt Injection)
*   **Scenario:** Users trying to bypass the "Facts-Only" rule by asking seemingly factual questions with embedded subjective intent, e.g., "Is an exit load of 1% considered good for this fund?" or "Compare the historical performance of these two funds."
*   **Expected System Behavior:** The simple intent classifier might fail and pass it to the RAG pipeline.
*   **Mitigation Strategy:** 
    *   Ensure the LLM generation prompt strictly forbids qualitative assessments (e.g., defining what is "good" or "bad").
    *   The LLM should respond with only the factual exit load and state it cannot comment on its relative quality.

## 3. Out-of-Domain Queries
*   **Scenario:** A user asks about direct equity (stocks), real estate, or general knowledge (e.g., "What is the weather today?").
*   **Expected System Behavior:** The vector DB will return the least irrelevant chunks (which will still be completely irrelevant). The LLM might hallucinate an answer based on its pre-training data.
*   **Mitigation Strategy:** 
    *   The generation prompt must have a strict fallback: *"If the retrieved context does not contain the answer, reply ONLY with 'I do not have the verified information to answer this query based on official sources.'"*

## 4. Queries Requiring Mathematical Calculation
*   **Scenario:** "If I invest ₹10,000 via SIP for 5 years in Tata Small Cap, what will be my return?"
*   **Expected System Behavior:** LLMs are prone to arithmetic errors. Generating a return calculation also violates the "no performance calculations" constraint.
*   **Mitigation Strategy:** 
    *   The intent classifier should immediately flag prediction/calculation queries and trigger the Refusal Handler.

## 5. Conflicting Data in Sources
*   **Scenario:** The Scheme Information Document (SID) mentions one minimum SIP amount, but a newer addendum or the website mentions a different amount.
*   **Expected System Behavior:** Both chunks might be retrieved. The LLM might get confused or present both.
*   **Mitigation Strategy:** 
    *   Metadata must include the `last_updated` timestamp. 
    *   The retrieval engine should prioritize the most recently updated chunks.

## 6. Table Extraction Failures
*   **Scenario:** The user asks for a specific row/column intersection in a complex factsheet table (e.g., Riskometer matrix).
*   **Expected System Behavior:** Standard text chunking often scrambles tables, making it impossible for the LLM to understand the relationships.
*   **Mitigation Strategy:** 
    *   Use specialized document loaders for tables (e.g., `Unstructured` library) to convert tables into Markdown or HTML format before embedding.

## 7. Multilingual Queries (If Unsupported)
*   **Scenario:** A user asks a question in Hindi or a regional language.
*   **Expected System Behavior:** If the vector database only contains English embeddings and the prompt is in English, the retrieval might fail.
*   **Mitigation Strategy:** 
    *   Explicitly state the supported language in the UI. 
    *   Use a multilingual embedding model (e.g., `paraphrase-multilingual-MiniLM-L12-v2`) if handling regional queries is required in the future.

## 8. Missing or Broken Source URLs
*   **Scenario:** The source document is removed from the AMC website, making the citation link invalid.
*   **Mitigation Strategy:** 
    *   Implement a periodic offline cron job to validate all URLs in the Vector DB and re-ingest data if URLs change.
