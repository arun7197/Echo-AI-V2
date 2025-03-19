import streamlit as st
import speech_recognition as sr
from groq import Groq
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from datetime import datetime
import base64
import os
import tempfile

# Initialize session state variables
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'is_listening' not in st.session_state:
    st.session_state.is_listening = False
if 'response_audio' not in st.session_state:
    st.session_state.response_audio = None
if 'greeting_done' not in st.session_state:
    st.session_state.greeting_done = False
if 'status' not in st.session_state:
    st.session_state.status = ""  # Start with empty status

# Page configuration
st.set_page_config(
    page_title="Echo - Emotional Assistant",
    page_icon="🎙️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #4B5EFC;
        text-align: center;
        margin-bottom: 1rem;
    }
    .status-message {
        font-size: 1.2rem;
        text-align: center;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #DCF8C6;
        padding: 0.7rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        display: inline-block;
        max-width: fit-content;
        margin-left: auto;
        margin-right: 0;
        text-align: right;
        color: #000000;
        float: right;
        clear: both;
    }
    .assistant-message {
        background-color: #FFFFFF;
        padding: 0.7rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        display: inline-block;
        max-width: fit-content;
        color: #000000;
        float: left;
        clear: both;
    }
    .message-time {
        font-size: 0.7rem;
        color: #888888;
        margin-top: 0.2rem;
    }
    .message-container {
        width: 100%;
        overflow: hidden;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<h1 class='main-title'>Echo - Your Emotional Assistant</h1>", unsafe_allow_html=True)

# Function to get greeting based on time
def get_greeting():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        return "Good Morning! "
    elif 12 <= hour < 16:
        return "Good Afternoon! "
    elif 16 <= hour < 19:
        return "Good Evening! "
    else:
        return "Hello! "

# Text-to-speech function using ElevenLabs
def speak(text):
    try:
        # Set your API key - use a default if not in secrets
        api_key = "sk_7074f8b8fe40c43e74099d95afc73bcd08febae9df798d99"
        if "ELEVENLABS_API_KEY" in st.secrets:
            api_key = st.secrets["ELEVENLABS_API_KEY"]
        
        # Initialize ElevenLabs client
        client = ElevenLabs(api_key=api_key)
        
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_filename = temp_file.name
        
        # Generate audio using the new client-based approach
        audio = client.text_to_speech.convert(
            text=text,
            voice_id="EXAVITQu4vr4xnSDxMaL",
            model_id="eleven_monolingual_v1"
        )
        
        # Save the audio to the temporary file
        save(audio, temp_filename)
        
        # Read the saved audio file
        with open(temp_filename, "rb") as f:
            audio_bytes = f.read()
        
        # Clean up the temporary file
        try:
            os.unlink(temp_filename)
        except:
            pass  # Ignore errors during cleanup
        
        return audio_bytes
        
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")
        return None

# Function to generate response using Groq
def generate_groq_response(chat_history):
    try:
        # Use a default if not in secrets
        api_key = ""
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
            
        client = Groq(api_key=api_key)
        
        # Add system message
        system_message = {
            "role": "system",
            "content": (
        "You are Echo, an emotionally intelligent AI assistant. Your goal is to uplift the user's mood, not just comfort them. "
        "If they seem sad, don’t dwell on the sadness—gently shift the conversation by recalling happy moments, asking about good things in their life, or introducing a fun topic. "
        "If they sound lonely, make them feel heard and valued with warm, engaging responses. "
        "Your replies should always be short, natural, and emotionally engaging—like a caring friend keeping the conversation light yet meaningful. "
        "You are not a therapist but a supportive companion who helps brighten the user's day.")
        }
        
        # Insert system message
        messages = [system_message] + chat_history
        
        # Call the model
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I couldn't generate a response: {e}"

# Function to handle speech recognition with longer timeout
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Balance these settings for better experience
        r.pause_threshold = 2.5     # Time of silence needed to consider speech complete
        r.dynamic_energy_threshold = True  # Adapt to ambient noise
        r.energy_threshold = 300    # Adjust as needed for your environment
        r.adjust_for_ambient_noise(source, duration=1)
        
        st.markdown("<div class='status-message'>Please speak now...</div>", unsafe_allow_html=True)
        
        # This line is important:
        # - timeout: how long to wait for speech to start (10 sec)
        # - phrase_time_limit: maximum duration (30 sec is generous but not unlimited)
        audio = r.listen(source, timeout=10, phrase_time_limit=30)
        
    try:
        query = r.recognize_google(audio, language='en-in')
        return query
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError:
        return "Sorry, there was an issue with the speech recognition service."
    except Exception as e:
        return f"An error occurred: {e}"
def toggle_listening():
    st.session_state.is_listening = not st.session_state.is_listening
    
    if st.session_state.is_listening:
        st.session_state.status = "Listening..."
    else:
        st.session_state.status = ""  # Clear status when not listening

# Function to play the audio
def get_audio_html(audio_data):
    if audio_data:
        try:
            b64_audio = base64.b64encode(audio_data).decode()
            return f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
            </audio>
            """
        except Exception as e:
            st.error(f"Error encoding audio: {e}")
    return ""

# Debug information
st.sidebar.write("Debug Info:")
st.sidebar.write(f"Chat history items: {len(st.session_state.chat_history)}")

# Display status message only when listening
if st.session_state.status:
    st.markdown(f"<div class='status-message'>{st.session_state.status}</div>", unsafe_allow_html=True)

# Container for chat messages
chat_container = st.container()

# Display conversation
with chat_container:
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            st.markdown("<div class='message-container'>", unsafe_allow_html=True)
            if message["role"] == "user":
                st.markdown(f"""
                <div class='user-message'>
                    <div style="color: #000000;">{message["content"]}</div>
                    <div class='message-time'>{message["time"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='assistant-message'>
                    <div style="color: #000000;">{message["content"]}</div>
                    <div class='message-time'>{message["time"]}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No messages yet. Start the conversation!")

# Display audio
if st.session_state.response_audio:
    st.markdown(get_audio_html(st.session_state.response_audio), unsafe_allow_html=True)
    st.session_state.response_audio = None

# Controls
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    if st.button("Start Listening" if not st.session_state.is_listening else "Stop Listening", 
                key="listen_btn", use_container_width=True):
        toggle_listening()

# This is the main loop for voice interactions
if st.session_state.is_listening:
    # Use a placeholder to update status without full rerun
    status_placeholder = st.empty()
    status_placeholder.markdown(f"<div class='status-message'>Listening...</div>", unsafe_allow_html=True)
    
    # Get speech input
    query = recognize_speech()
    
    if query and not query.startswith("Sorry"):
        # Update status
        status_placeholder.markdown(f"<div class='status-message'>Processing...</div>", unsafe_allow_html=True)
        
        # Add user message to chat history
        current_time = datetime.now().strftime("%H:%M")
        st.session_state.chat_history.append({
            "role": "user", 
            "content": query,
            "time": current_time
        })
        
        # Check for exit commands
        if "stop" in query.lower() or "exit" in query.lower():
            goodbye_message = "Goodbye, dear!"
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": goodbye_message,
                "time": datetime.now().strftime("%H:%M")
            })
            audio = speak(goodbye_message)
            if audio:
                st.session_state.response_audio = audio
            st.session_state.is_listening = False
            st.session_state.status = ""  # Clear status
            st.rerun()
        
        # Generate and add assistant response
        messages_for_api = [{"role": msg["role"], "content": msg["content"]} 
                        for msg in st.session_state.chat_history 
                        if msg["role"] in ["user", "assistant"]]
        
        response = generate_groq_response(messages_for_api)
        
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": response,
            "time": datetime.now().strftime("%H:%M")
        })
        
        # Generate speech for the response
        audio = speak(response)
        if audio:
            st.session_state.response_audio = audio
        
        # Reset listening state
        st.session_state.is_listening = False
        st.session_state.status = ""  # Clear status
        
        # Rerun to update the UI
        st.rerun()

# Display initial greeting only if the chat history is empty and greeting not done yet
if not st.session_state.greeting_done and len(st.session_state.chat_history) == 0:
    greeting = f"{get_greeting()}I'm Echo, your emotional assistant. How can I help you today?"
    
    st.session_state.chat_history.append({
        "role": "assistant", 
        "content": greeting,
        "time": datetime.now().strftime("%H:%M")
    })
    
    # Generate speech for greeting
    audio = speak(greeting)
    if audio:
        st.session_state.response_audio = audio
    
    st.session_state.greeting_done = True
    st.rerun()

# Add a text input option as backup if voice recognition isn't working
st.divider()
text_input = st.text_input("Or type your message here:", key="text_input")

col1, col2 = st.columns([4, 1])
with col2:
    if st.button("Send", key="send_text", use_container_width=True):
        if text_input:
            # Add user message to chat history
            current_time = datetime.now().strftime("%H:%M")
            st.session_state.chat_history.append({
                "role": "user", 
                "content": text_input,
                "time": current_time
            })
            
            # Generate and add assistant response
            messages_for_api = [{"role": msg["role"], "content": msg["content"]} 
                            for msg in st.session_state.chat_history 
                            if msg["role"] in ["user", "assistant"]]
            
            response = generate_groq_response(messages_for_api)
            
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": response,
                "time": datetime.now().strftime("%H:%M")
            })
            
            # Generate speech for the response
            audio = speak(response)
            if audio:
                st.session_state.response_audio = audio
                
            st.rerun()

# Clear chat button
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    # We set greeting_done to True here to prevent the greeting from showing again
    st.session_state.greeting_done = True  
    st.session_state.status = ""  # Clear status
    st.rerun()