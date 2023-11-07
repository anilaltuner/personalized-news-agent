import streamlit as st
from firstbatch import AlgorithmLabel
from pydantic import BaseModel

from news import CUSTOM_ALGO_ID, initialize_session, fetch_content
from chat_tools.kernel import chat, setup_chat_with_memory
from markdowns.markdowns_chat import css_, sidebar


# Pydantic models
class SessionData(BaseModel):
    username: str


class PersonalizeData(BaseModel):
    message: str


class SignalData(BaseModel):
    sessionID: dict
    id: str


def get_user_input():
    return st.sidebar.text_input("Username/Session Name", st.session_state.get("username", ""))


def update_session_state(user_input):
    st.session_state.session = st.session_state.personalized.session(
        AlgorithmLabel.CUSTOM, vdbid="rss_db", custom_id=CUSTOM_ALGO_ID
    )
    st.session_state.batches = []
    st.session_state.ids = []
    st.session_state.likes = []
    ids, batch = st.session_state.personalized.batch(st.session_state.session)
    st.session_state.batches += batch
    st.session_state.ids += ids
    st.session_state.username = user_input
    st.session_state.html_content = """
         <div class="chat-container">
            <div class="chat-box">
                <div class="chat-output" id="chat-output"></div>
            </div>
        </div>
        """
    st.session_state.chat_placeholder = st.empty()
    st.session_state.chat_history = ""
    st.session_state.chat_loader = 3


def display_sidebar():
    user_input = get_user_input()
    if user_input and st.session_state.get("username") != user_input:
        update_session_state(user_input)
        initialize_session(user_input)
        fetch_content()

    st.sidebar.title("Personalized AI Agent")
    st.sidebar.markdown(sidebar)


def chat_init():
    if "html_content" not in st.session_state:
        st.session_state.html_content = """
         <div class="chat-container">
            <div class="chat-box">
                <div class="chat-output" id="chat-output"></div>
            </div>
        </div>
        """
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "init" not in st.session_state:
        if st.session_state.loading == 1:
            st.session_state.ids, st.session_state.batches = st.session_state.personalized.batch(st.session_state.session)
        chat(model=model, prompt=prompt, message="Hello!")
        st.session_state.init = True


def submit():
    st.session_state.test_st = st.session_state.user_input
    st.session_state.user_input = ''


def display_box():
    st.markdown(css_, unsafe_allow_html=True)

    if "html_content" not in st.session_state:
        st.session_state.html_content = """
         <div class="chat-container">
            <div class="chat-box">
                <div class="chat-output" id="chat-output"></div>
            </div>
        </div>
        """
    st.session_state.chat_placeholder.markdown(st.session_state.html_content, unsafe_allow_html=True)
    st.text_input("User Input", key="user_input", on_change=submit())
    if "username" not in st.session_state:
        st.session_state.username = ""
    if st.session_state.test_st != "":
        print("User input changed")
        if st.session_state.chat_loader > 2:
            ids, batch = st.session_state.personalized.batch(st.session_state.session)
            st.session_state.batches = batch
            st.session_state.ids = ids
            st.session_state.chat_loader = 0
        st.session_state.chat_loader += 1
        chat(model=model, prompt=prompt, message=st.session_state.test_st)
        st.session_state.test_st = ""


if __name__ == '__main__':
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''
    st.session_state.chat_loader = 0
    st.session_state.chat_placeholder = st.empty()
    model, prompt = setup_chat_with_memory()
    display_box()
    display_sidebar()
    chat_init()
