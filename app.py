import streamlit as st
from classifier import IntentClassifier
from retriever import Retriever
from generator import Generator
from postprocessor import PostProcessor

# Configure the page
st.set_page_config(
    page_title="Mutual Fund FAQ Assistant",
    page_icon="📈",
    layout="centered"
)

# Initialize components once using session state for performance
if "components_initialized" not in st.session_state:
    try:
        st.session_state.classifier = IntentClassifier(use_llm=True)
        st.session_state.retriever = Retriever(k=2)
        st.session_state.generator = Generator()
        st.session_state.postprocessor = PostProcessor()
        st.session_state.components_initialized = True
    except Exception as e:
        st.error(f"Error initializing components: {e}")
        st.stop()

# --- UI Setup ---
st.title("Mutual Fund FAQ Assistant")

# Disclaimer banner (highly visible)
st.warning("**Facts-only. No investment advice.**")
st.markdown("I retrieve factual data strictly from official scheme information documents. I cannot provide recommendations or compare performance.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Provide 3 Example Prompts as buttons
st.markdown("### Example Questions")
col1, col2, col3 = st.columns(3)

if col1.button("Exit load for Tata Gold ETF?"):
    st.session_state.example_query = "What is the exit load for Tata Gold ETF?"
if col2.button("Expense ratio for Tata Small Cap?"):
    st.session_state.example_query = "What is the expense ratio for Tata Small Cap Fund?"
if col3.button("Should I invest in Tata Silver ETF?"):
    st.session_state.example_query = "Should I invest in Tata Silver ETF?"

# Display chat history from previous interactions
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
user_input = st.chat_input("Ask a factual question about a Tata Mutual Fund...")

# Check if an example button was clicked or text was submitted
query = user_input or st.session_state.pop("example_query", None)

if query:
    # Display the user's query
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    # Generate and display assistant's response
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            # Step 1: Guardrail / Intent Classification
            is_factual, refusal_msg = st.session_state.classifier.is_factual(query)
            
            if not is_factual:
                # Respond with the refusal template
                final_response = refusal_msg
            else:
                # Step 2: Retrieve similar chunks
                docs = st.session_state.retriever.retrieve(query)
                
                # Step 3: LLM Generation
                raw_answer = st.session_state.generator.generate(query, docs)
                
                # Step 4: Add Source Citations
                final_response = st.session_state.postprocessor.format_response(raw_answer, docs)
            
            # Display final answer
            st.markdown(final_response)
            
            # Add to history
            st.session_state.messages.append({"role": "assistant", "content": final_response})
