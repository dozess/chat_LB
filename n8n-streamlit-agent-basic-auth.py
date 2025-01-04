import streamlit as st
import requests
import uuid

# Custom CSS for chat alignment
st.markdown("""
<style>
[data-testid="stChatMessage"] {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    max-width: 80%;
}
.user-message {
    display: flex;
    justify-content: flex-end;
}
[data-testid="stChatMessage"].user [data-testid="stImage"] {
    order: 2;
    margin-left: 10px;
    margin-right: 0;
}
.user-message [data-testid="stMarkdownContainer"] {
    margin-left: auto;
    background-color: #0084ff;
    color: white;
    border-radius: 15px;
    padding: 10px;
}
.assistant-message [data-testid="stMarkdownContainer"] {
    margin-right: auto;
    background-color: #f0f0f0;
    border-radius: 15px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# Constants
WEBHOOK_URL = "https://n8n.savaitgalioprojektai.lt/webhook/f9f3653a-633e-4949-91c7-70bad1425006"
BEARER_TOKEN = "LABAS"

def generate_session_id():
    return str(uuid.uuid4())

def send_message_to_llm(session_id, message):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "sessionId": session_id,
        "chatInput": message
    }
    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    #print (response.json())
    if response.status_code == 200:
        return response.json()["output"]
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    st.title("Chat with LLM")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = generate_session_id()

    # Display chat messages
    for message in st.session_state.messages:
        avatar = "🧑" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            div_class = "user-message" if message["role"] == "user" else "assistant-message"
            st.markdown(f'<div class="{div_class}">{message["content"]}</div>', unsafe_allow_html=True)

    # User input
    user_input = st.chat_input("Type your message here...")
 
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(f'<div class="user-message">{user_input}</div>', unsafe_allow_html=True)

        # Get LLM response
        llm_response = send_message_to_llm(st.session_state.session_id, user_input)

        # Add LLM response to chat history
        st.session_state.messages.append({"role": "assistant", "content": llm_response})
        with st.chat_message("assistant", avatar=None):
            st.markdown(f'<div class="assistant-message">{llm_response}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
