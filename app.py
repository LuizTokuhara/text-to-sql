import streamlit as st

MODEL = "gemini-2.0-flash"
TEMPERATURE = 0.7
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
SYSTEM_PROMPT = "You are a SQL expert. You will be given a natural language question and you will return the SQL query that answers the question."

MODEL_PARAMS = {
  "model": MODEL,
  "temperature": TEMPERATURE,
}

def main():
  # ---- Page config -----
  st.set_page_config(
    page_title="Text to SQL",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
  )

  # ---- Sidebar config -----
  with st.sidebar:
    st.header("Configuration")
    st.text_input("Gemini API Key", GEMINI_API_KEY, type="password")
    st.slider("Temperature", 0.0, 1.0, TEMPERATURE, 0.1)

    st.subheader("LLM setup")
    st.text_area("System prompt", SYSTEM_PROMPT, height=200)

  st.markdown("""
    <style>
    .stChatMessage {
        padding: 10px;
    }
    .stChatMessage .message-container {
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
  # ---- Initialize message state ----
  if "messages" not in st.session_state:
      st.session_state.messages = []
  
  # ---- Show message history ----
  for message in st.session_state.messages:
      with st.chat_message(message["role"]):
          if message["role"] == "user":
              st.write(message["content"])
          else:
              # ---- Assistant messages ----
              st.code(message["content"]["sql"], language="sql")
              
              if message["content"]["error"]:
                  st.error(f"Error on query execution: {message['content']['error']}")
              else:
                  st.subheader("Query:")
                  st.dataframe(message["content"]["results"])
                  
                  st.subheader("Explanation:")
                  st.write(message["content"]["explanation"])
  
  st.title("🤖 Text to SQL agent")

  # ---- User input ----
  if prompt := st.chat_input("Ask a question about your database data"):
      # ---- Add user message to history ----
      st.session_state.messages.append({"role": "user", "content": prompt})
      
      # ---- Show user message ----
      with st.chat_message("user"):
          st.write(prompt)
      
      # Process query
      # process_query(prompt, schema)



if __name__ == "__main__":
  main()
  