import streamlit as st
from agent_orchestrator import run_agent_query # Our agent

st.set_page_config(page_title="AI-Powered Test Automation Assistant", layout="wide")

st.title("🤖 AI-Powered Test Automation Assistant")
st.write("Ask natural language queries to generate tests, get insights, and manage automation.")

# Initialize chat history in session_state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Capture current user input ---
# Use a chat_input widget for better conversational UX
if user_query := st.chat_input("Enter your query..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_query)

    # Get AI response and display it
    with st.chat_message("assistant"):
        with st.spinner("Processing your request..."):
            # Pass the entire conversation history to the agent
            # We'll need to adapt run_agent_query to accept history
            response = run_agent_query(user_query, chat_history=st.session_state.messages)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- Old text_area and button code (can be removed or commented out) ---
# def clear_text():
#     st.session_state.user_query = ""

# if "user_query" not in st.session_state:
#     st.session_state.user_query = ""

# st.text_area("Enter your query (e.g., 'Write a login test for Chrome', 'Explain test data management', 'Run this Java test code: class MyTest { ... }'):", key="user_query", height=150)

# if st.button("Generate/Execute"):
#     if st.session_state.user_query:
#         with st.spinner("Processing your request..."):
#             response = run_agent_query(st.session_state.user_query) # This call needs to change
#             st.success("Request Processed!")
#             st.subheader("Response:")
#             st.markdown(response)
#     else:
#         st.warning("Please enter a query.")
# --- End old code ---

st.sidebar.header("About")
st.sidebar.info(
        "This is a demo of an AI-powered test automation framework "
        "leveraging LLMs, RAG, and agentic workflows."
    )
# Streamlit app for AI-Powered Test Automation Assistant
# This app allows users to interact with an AI agent that can generate test code,
# execute tests, and provide insights on test automation concepts.
#
# **Features:**
# - Generate test code from natural language queries
# - Execute Java test code and return results
# - Retrieve contextual information from a knowledge base
# - User-friendly interface with Streamlit
#
# **Requirements:**
# - Python 3.8+
# - Streamlit
# - LangChain
# - Google Generative AI client
# - Other dependencies as specified in requirements.txt
#
# **Installation:**
# 1. Clone the repository:
#    git clone      ```
# Command * **To Run:* the app, navigate to the project directory and run:
#    cd your-repo-name
# 2. Install the required packages:
#    pip install -r requirements.txt
# 3. Set up your environment variables in a `.env` file:
#    GOOGLE_API_KEY=your_google_api_key
# 4. Run the Streamlit app: streamlit run app.py