import streamlit as st
import requests
from openai import OpenAI

st.title("Tanya OksaAI 🚀")
st.write("Ask me with whatever you curious about")

# using direct api-key because it is only for developement
api_key = "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"

# inisialisasi client OpenAI
# baserul untuk alamat endpoint OpenRuter.
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# Initialize default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "deepseek/deepseek-r1-distill-llama-70b:free"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# Accept user input
if prompt := st.chat_input("Write here!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user input in UI
    with st.chat_message("user"):
        st.markdown(prompt)

    # Show a spinner while waiting for the response
    with st.spinner("OksaAI is thinking..."):
        try:
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://oksaai.streamlit.app",  # Ganti dengan URL Anda
                "X-Title": "OksaAI Chatbot",
                "Content-Type": "application/json"
            }
            
            # Prepare request data
            data = {
                "model": st.session_state["openai_model"],
                "messages": st.session_state.messages
            }
            
            # Make the API call
            response = requests.post(
                f"{base_url}/chat/completions", 
                headers=headers,
                json=data
            )
            
            # Process the response
            if response.status_code == 200:
                response_data = response.json()
                answer = response_data["choices"][0]["message"]["content"]
            else:
                answer = f"Error: API returned status code {response.status_code} - {response.text}"
                st.error(f"API Error: {response.text}")
                
        except Exception as e:
            answer = f"Error: {str(e)}"
            st.error(f"An error occurred: {str(e)}")

    # Add the answer to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})

    # Display the answer in UI
    with st.chat_message("assistant"):
        st.markdown(answer)
# # Accept user input
# if prompt := st.chat_input("Write here!"):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     # Display user input in UI
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Show a spinner while waiting for the response
#     with st.spinner("OksaAI is thinking..."):
#         try:
#             # Call the OpenRouter API to get a response
#             response = client.chat.completions.create(
#                 model=st.session_state["openai_model"],
#                 messages=st.session_state.messages,
#                 extra_headers={
                    
#                     "HTTP-Referer": "https://chatbot-ai-deepseek-model.streamlit.app/",  # my url
#                     "X-Title": "OksaAI",  # my app name
#                 }
#             )

#             # Get the answer from the response
#             answer = response.choices[0].message.content

#         except Exception as e:
#             answer = f"Error: {str(e)}"
#             st.error(f"An error occurred: {str(e)}")

#     # Add the answer to chat history
#     st.session_state.messages.append({"role": "assistant", "content": answer})

#     # Display the answer in UI
#     with st.chat_message("assistant"):
#         st.markdown(answer)
