import os

import streamlit as st
from bs4 import BeautifulSoup
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

os.environ["OPENAI_API_KEY"] = st.secrets["open_ai_api_key"]


class StreamHandler(BaseCallbackHandler):
    def __init__(self, soup, chat_output):
        self.soup = soup
        self.bot_div = self.soup.new_tag("div", **{'class': 'bot-message'})
        self.bot_div.string = f"Bot: "
        self.chat_output = chat_output

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.bot_div.string += f"{token}"
        self.chat_output.append(self.bot_div)
        st.session_state.chat_placeholder.markdown(self.soup, unsafe_allow_html=True)
        st.session_state.html_content = str(self.soup)


def setup_chat_with_memory():
    sk_prompt = """   
Don't write the prompt titles as answer. And dont write "Chatbot>" as answer 
     
Context Articles and Recommendations:
{context}

Previous Chat Dialogue:
{chat_history}

User's Question: {user_input}

ChatBot's Reply will about to:
[Content Tailoring]: Crafting the response to align with the user's preferences, using language and topics that mirror their interests.
[Engagement and Continuity]: Engaging the user by asking questions or suggesting actions that are likely to align with their interests.
[Learning and Adaptation]: Ending the conversation in a way that allows for continuous learning from the user's feedback.
""".strip()

    prompt = PromptTemplate(
        template=sk_prompt, input_variables=["context", "user_input", "chat_history"]
    )
    chain = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.8, streaming=True, max_tokens=256)

    return chain, prompt


def generate_session_context(session):
    context = "Recommended context from Firstbatch's recommendation algorithm:"
    for doc in session["batches"][:5]:
        context += (
                "\nArticle text is: " + doc.data["text"] + " Link: " + doc.data["link"] + "\n"
        )
    return context


def chat(model, prompt, message):
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = ""
    context = generate_session_context(st.session_state)
    runnable = prompt | model | StrOutputParser()
    soup = BeautifulSoup(st.session_state.html_content, 'html.parser')
    chat_output = soup.find(id='chat-output')
    if "init" in st.session_state:
        user_div = soup.new_tag("div", **{'class': 'user-message'})
        user_div.string = f"{st.session_state.username}: {message}"
        chat_output.append(user_div)
    stream_handler = StreamHandler(soup=soup, chat_output=chat_output)
    answer = runnable.invoke(
        ({"context": context, "user_input": message, "chat_history": st.session_state["chat_history"]}),
        config={"callbacks": [stream_handler]})
    st.session_state["chat_history"] += f"\nUser:> {message}\nChatBot:> {answer}\n"
