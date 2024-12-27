import os
import gradio as gr
from groq import Groq

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def get_groq_response(message):
    """Get response from Groq API"""
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

# Create Gradio interface
def chat_interface(message):
    if not message.strip():
        return "Please enter a message."
    
    try:
        response = get_groq_response(message)
        return response
    except Exception as e:
        return f"Error: {str(e)}"

# Create and launch the Gradio interface
iface = gr.Interface(
    fn=chat_interface,
    inputs=gr.Textbox(lines=3, placeholder="Enter your message here..."),
    outputs=gr.Textbox(label="Groq Response"),
    title="Groq Chat Interface",
    description="Chat with Groq's LLama3 model",
)

if __name__ == "__main__":
    iface.launch() 