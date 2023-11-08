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
Avoid using "Answer:" or "Chatbot>" as a response header. Responses should be concise, not exceeding 400 tokens.

Prioritize articles that the user has expressed interest in for tailored recommendations. Use articles from the initial batch for suggestion purposes.

User Preferences:
{user_interaction}

Relevant Articles for Context and Suggestions:
{context}

Prior Conversation Record:
{chat_history}

User Inquiry:
{user_input}

Upcoming Chatbot Response will focus on:

[Content Customization]: Shaping the reply to reflect the user's likes using relevant language and themes.
[Interaction and Progression]: Keeping the user engaged with pertinent questions or proposed activities.
[Evolution and Adjustment]: Wrapping up the dialogue in a manner that incorporates the user's input for future interactions.

""".strip()

    prompt = PromptTemplate(
        template=sk_prompt, input_variables=["context", "user_input", "chat_history"]
    )
    chain = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.8, streaming=True, max_tokens=512)

    return chain, prompt


def generate_session_context(session):
    if len(session["likes"]) == 0:
        return "User has no interaction", "User has no recommended articles"
    user_interaction = ""
    for doc in session["likes"]:
        user_interaction += (
                "\nArticle text is: " + doc.data["text"] + " Link: " + doc.data["link"] + "\n"
        )
    context = ""
    for doc in session["batches"][:5]:
        context += (
                "\nArticle text is: " + doc.data["text"] + " Link: " + doc.data["link"] + "\n"
        )
    return context, user_interaction


def chat(model, prompt, message):
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = ""
    context, user_interaction = generate_session_context(st.session_state)
    runnable = prompt | model | StrOutputParser()
    soup = BeautifulSoup(st.session_state.html_content, 'html.parser')
    chat_output = soup.find(id='chat-output')
    if "init" in st.session_state:
        user_div = soup.new_tag("div", **{'class': 'user-message'})
        user_div.string = f"{st.session_state.username}: {message}"
        chat_output.append(user_div)
    stream_handler = StreamHandler(soup=soup, chat_output=chat_output)
    answer = runnable.invoke(
        ({"context": context, "user_interaction": user_interaction, "user_input": message, "chat_history": st.session_state["chat_history"]}),
        config={"callbacks": [stream_handler]})
    st.session_state["chat_history"] += f"\nUser:> {message}\nChatBot:> {answer}\n"
