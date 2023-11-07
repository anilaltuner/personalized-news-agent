css_ = """
<style>
body {
    font-family: Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #1a1a1a;
}

.chat-container {
    background-color: #1A1A1D;
    box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.2);
    height: 70vh;
    margin: 0 auto;
    overflow-y: auto; /* adds a vertical scrollbar when needed */
}


.chat-box {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 75vh;
}

.chat-output {
    flex: 1;
    padding: 15px;
    border-bottom: 1px solid #444; /* Separation between the chat and input */
}

.chat-input {
    display: flex;
    align-items: center;
    padding: 10px;
    background-color: #1a1a1a;
}

.username-section {
    border-bottom: 1px solid #444;
    display: flex;
    align-items: center;
    padding: 10px;
    background-color: #1f1f1f;
}

input[type="text"] {
    flex: 1;
    padding: 8px;
    border: 1px solid #555;
    background-color: #1f1f1f;
    color: #e0e0e0;
    border-radius: 5px;
}

button {
    margin-left: 10px;
    padding: 8px 15px;
    border: none;
    border-radius: 5px;
    background-color: #007BFF;
    color: #fff;
    cursor: pointer;
    transition: background-color 0.3s;
}

button:hover {
    background-color: #0056b3;
}

.spinner {
    border: 4px solid rgba(255, 255, 255, 0.3);
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border-top: 4px solid #007BFF;
    animation: spin 1s linear infinite;
    display: none;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.user-message, .bot-message {
    margin: 10px 0;
    padding: 10px 15px;
    border-radius: 20px;
    width: fit-content;
}

.user-message {
    background-color: #8E8E93;
    align-self: flex-end;
}

.bot-message {
    background-color: #007AFF;
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
