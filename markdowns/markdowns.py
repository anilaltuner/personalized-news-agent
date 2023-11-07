css_ = """
<style>
    .rss-item {
        display: flex;
        flex-direction: row;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        margin: 10px 0;
        transition: box-shadow 0.3s ease;
    }
    .rss-item:hover {
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .rss-item img {
        width: 200px;
        height: 200px;
        object-fit: cover;
        margin-right: 15px;
    }
    .rss-content {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }
    .rss-content h2 {
        font-size: 1.0em;
    }
    .rss-content h2 a {
        color: inherit;
    }
    .rss-content h2 a:hover {
    color: #0078e7;
    }
    .rss-content p {
        color: #777;
        line-height: 1.5;
        font-size: 1.1em;
    }

    /* Mobile */
    @media only screen and (max-width: 600px) {
        .rss-item {
            flex-direction: column;
            align-items: center;
        }
        .rss-item img {
            width: 100%;
            height: auto;
            margin-right: 0;
            margin-bottom: 15px;
        }
    }
    .streamlit-expanderHeader {
        background-color: white;
        color: black; # Adjust this for expander header color
    }
    .streamlit-expanderContent {
        background-color: white;
        color: black; # Expander content color
    }
</style>
"""

sidebar = """
    Personalized Chatbot Powered by Firstbatch Recommendation Algorithm
    
    *Our chatbot, integrated with the Firstbatch recommendation engine, ensures a seamless and tailored news feed 
    experience for users. As users interact and express their preferences, the chatbot refines its responses, 
    drawing from Firstbatch's recommendation capabilities. Here's a breakdown of how the recommendation 
    personalization progresses:* 
    
    **Level 1: Initialization Phase**
    
    *State: The chatbot starts with no user-specific data. Content is delivered in a fully randomized manner, 
    awaiting user interactions for further refinement.*
    
    **Level 2: Signal Anchoring**
    
    *State: As users start to like news content, the chatbot becomes more aligned with these preferences. Content is 
    now generated with minimal randomness, primarily based on direct user signals.*
    
    **Level 3: Signal Integration with Random Exploration**
    
    *State: The chatbot now starts to balance between user signals and new content exploration. It delivers news that 
    aligns with users' demonstrated preferences while also introducing them to contextually relevant content.*
    
    *Throughout these levels, it's imperative to note that only the last three user signals predominantly influence 
    the recommendation embeddings. This ensures that the news feed remains dynamic and is largely influenced by 
    recent user interactions.*
    
    Further Details: For a deeper understanding of the underlying mechanisms, refer to the algorithm [details](
    https://firstbatch.gitbook.io/rss-feed-algorithm/). 
    
    SDK Documentation: Developers looking to integrate or understand the functionalities can refer to the [FirstBatch 
    SDK Docs](https://firstbatch.gitbook.io/firstbatch-sdk/get-started/introduction).* """