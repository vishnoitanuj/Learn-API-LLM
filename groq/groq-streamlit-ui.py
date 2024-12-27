import os
import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="Groq Chat Interface",
    page_icon="💬",
    layout="centered"
)

# Add custom CSS for better styling
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .stMarkdown {
        font-family: 'Arial', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Groq client
@st.cache_resource
def get_groq_client():
    return Groq(api_key=os.environ.get("GROQ_API_KEY"))

client = get_groq_client()

# Title and description
st.title("💬 Groq Chat Interface")
st.markdown("Chat with Groq's LLama3 model. Enter your message below and get AI-powered responses!")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama3-8b-8192",
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Add a sidebar with information
with st.sidebar:
    st.title("About")
    st.markdown("""
    This is a Streamlit-powered chat interface for Groq's LLama3 model.
    
    **Features:**
    - Real-time chat interface
    - Message history
    - Error handling
    - Responsive design
    
    Make sure you have your `GROQ_API_KEY` set in your environment variables.
    """) 