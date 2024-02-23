import streamlit as st
import sys
sys.path.append('../')
from bots.spotify_qa import SpotifyQA

# Initialize App
qa = SpotifyQA(
    base_url="http://localhost:11434",
    model="llama2",
    index_path="../index",
    k=2
)

# App title
st.set_page_config(page_title="💬 Spotify Reviews Chatbot")
def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I assist you today?"}
    ]
st.title("💬 Spotify Reviews Chatbot")
st.button('Clear Chat History', on_click=clear_chat_history)

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I assist you today?"}
    ]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = qa.generate_answer(query=f"{string_dialogue} \n\nUser: {prompt_input} \n\nAssistant: ")
    print(output)
    return output

# User-provided prompt
is_chat_disabled=False
if prompt := st.chat_input(disabled=is_chat_disabled):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Generating Answer..."):
            is_chat_disabled = True
            response = generate_response(prompt)
            answer = response['result']
            references = response["source_documents"]
            st.markdown(answer)

    message = {"role": "assistant", "content": answer}
    st.session_state.messages.append(message)

    with st.chat_message("log"):
        st.markdown(f"Source Documents: \n\n`{references}`")

    message = {"role": "log", "content": references}
    st.session_state.messages.append(message)