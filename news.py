import streamlit as st
from firstbatch import FirstBatch, AlgorithmLabel, Pinecone, Config, UserAction, Signal
import pinecone
from markdowns.markdowns import css_, sidebar
from st_pages import Page, show_pages

# Configurations
FIRST_BATCH_API_KEY = st.secrets["api"]["firstbatch_api_key"]
PINECONE_API_KEY = st.secrets["api"]["pinecone_api_key"]
PINECONE_ENV = st.secrets["api"]["pinecone_env"]
PINECONE_INDEX_NAME = st.secrets["pinecone_index"]
FIRSTBATCH_DB_NAME = st.secrets["firstbatch_db_name"]
CUSTOM_ALGO_ID = st.secrets["custom_algo_id"]
EMBEDDING_SIZE = st.secrets["embedding_size"]

st.set_page_config(
    page_title="Personalized Agent",
    layout="wide",
    initial_sidebar_state="expanded",
)

show_pages(
    [
        Page("news.py", "News", "📰"),
        Page("pages/chatbot.py", "Personalized Chatbot ", "🤖"),
    ]
)


def setup():
    """Set up FirstBatch and Pinecone configurations."""
    config = Config(batch_size=10, verbose=False, enable_history=True)
    personalized = FirstBatch(api_key=FIRST_BATCH_API_KEY, config=config)
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    index = pinecone.Index(PINECONE_INDEX_NAME)
    personalized.add_vdb(FIRSTBATCH_DB_NAME, Pinecone(index, embedding_size=EMBEDDING_SIZE))
    st.session_state.personalized = personalized
    initialize_session()


def initialize_session(user_input=""):
    """Initialize or restart the session."""
    if user_input:
        st.session_state.username = user_input
    username_suffix = st.session_state.username if "username" in st.session_state else None
    if username_suffix:
        st.session_state.session = st.session_state.personalized.session(
            AlgorithmLabel.CUSTOM,
            custom_id=CUSTOM_ALGO_ID,
            vdbid=FIRSTBATCH_DB_NAME,
            session_id="rss_feed" + username_suffix
        )
    else:
        st.session_state.session = st.session_state.personalized.session(
            AlgorithmLabel.CUSTOM,
            custom_id=CUSTOM_ALGO_ID,
            vdbid=FIRSTBATCH_DB_NAME
        )
    st.session_state.batches = []
    st.session_state.ids = []
    st.session_state.likes = []
    st.session_state.html_content = """
         <div class="chat-container">
            <div class="chat-box">
                <div class="chat-output" id="chat-output"></div>
            </div>
        </div>
        """
    st.session_state.chat_placeholder = st.empty()
    st.session_state.chat_history = ""
    st.session_state.chat_loader = 0


def fetch_content():
    """Fetch content for the current session."""
    ids, batch = st.session_state.personalized.batch(st.session_state.session)
    st.session_state.batches += batch
    st.session_state.ids += ids


def display_feed_item():
    """Display feed items."""
    for i, b in enumerate(st.session_state.batches):
        display_rss_item(b)
        if st.button(f'♥️️', i):
            signal(st.session_state.ids[i])
            st.session_state.likes.append(b)


def display_rss_item(item):
    """Render a single RSS item."""
    with st.container():
        st.markdown(f"""
            <div class="rss-item">
                <img src="{item.data['img_link']}" alt="Image Description">
                <div class="rss-content">
                    <h2><a href="{item.data['link']}">{item.data['title']}</a></h2>
                    <p>{item.data['text'] + "..."}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)


def display_sidebar():
    """Display the sidebar and handle user input."""
    user_input = st.sidebar.text_input("Username/Session Name", st.session_state.get("username", ""))
    if user_input and user_input != st.session_state.get("username", ""):
        with st.spinner('Collecting data for personalized news...'):
            st.session_state.username = user_input
            initialize_session()
            fetch_content()
            st.rerun()
    st.sidebar.title("Personalized Agent")
    st.sidebar.markdown(sidebar)
    display_liked_items()


def display_liked_items():
    """Display the items liked by the user."""
    st.sidebar.subheader("Liked Items")
    for item in st.session_state.likes:
        st.sidebar.markdown(f"[{item.data['title']}]({item.data['link']})")


def signal(cid):
    """Add liked contents as signals."""
    st.session_state.personalized.add_signal(st.session_state.session, UserAction(Signal.LIKE), cid)


def main():
    """Main function to render the app."""
    st.title("News")
    st.markdown(css_, unsafe_allow_html=True)
    with st.expander("**Explanation of Personalized AI Agent**", expanded=True):
        st.write("""*Embark on a bespoke chatbot journey with our Enhanced Personalized AI Agent, designed to deliver 
        a truly individualized experience across various communication channels. This intelligent system offers a 
        dynamic news feed that refines its output based on your interactions, narrowing a wide spectrum of topics 
        into a tailored selection that resonates with your interests. Starting with broad strokes, the AI quickly 
        hones in on your preferences, presenting a curated mix of familiar favorites punctuated by unexpected, 
        yet relevant, discoveries.* \n\n *To engage with this chatbot, simply initiate a session with 
        your username in the left sidebar and proceed to the **"Personalized Chatbot"** area. The agent's advanced 
        session management remembers your likes ensuring a customized dialogue every time you return, even as you switch
         between devices.* """)

    if 'personalized' not in st.session_state:
        with st.spinner('Configuring Firstbatch Engine and documents are fetching...'):
            setup()
            fetch_content()
    display_feed_item()
    display_sidebar()
    if "loading" not in st.session_state:
        st.session_state.loading = 1
    if st.button("Load More", "btn" + str(st.session_state.loading)):
        spinner = st.spinner('Loading more contents...', )
        with spinner:
            ids, batch = st.session_state.personalized.batch(st.session_state.session)
            st.session_state.batches += batch
            st.session_state.ids += ids
            st.session_state.loading += 1
            st.rerun()


if __name__ == '__main__':
    main()
