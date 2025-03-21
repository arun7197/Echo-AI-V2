# Echo-AI-V2
![Screenshot 2025-03-19 070644](https://github.com/user-attachments/assets/53c40a91-8833-4414-8445-6ec55d3af857)
Project Demo

https://github.com/user-attachments/assets/e0fcc7c6-5194-4128-b662-091d9b0cf4e9

Echo AI - Emotional Assistant
Overview
Echo is an emotionally intelligent AI voice assistant designed to provide supportive, uplifting conversations. Unlike conventional assistants that focus on task completion, Echo prioritizes emotional connection, sensing the user's mood and responding with empathy and warmth.
Key Features

Voice-Based Interaction: Natural conversation through speech recognition
Emotional Intelligence: Uses advanced AI to detect emotional cues and respond appropriately
Mood Elevation: Gently shifts conversations from negative to positive topics
Natural Voice Responses: High-quality text-to-speech using ElevenLabs
Contextual Memory: Remembers conversation history for more coherent interactions
Intuitive UI: Clean, chat-like interface with real-time status updates

Technology Stack

Frontend: Streamlit for responsive web interface
AI Processing: Groq API with LLaMA 3 (8B parameter model)
Speech Recognition: SpeechRecognition library with Google's speech-to-text
Text-to-Speech: ElevenLabs API for natural-sounding voice synthesis

How It Works

The application listens for user speech input
Audio is converted to text using speech recognition
User's message is processed by the Groq LLM with contextual history
The AI generates an emotionally appropriate response
Response is converted to speech using ElevenLabs TTS
Both text and audio responses are presented to the user

Use Cases

Emotional Support: Provides a listening ear during difficult times
Mood Improvement: Helps users shift perspective toward positivity
Companionship: Reduces feelings of loneliness through engaging conversation
Practice Tool: Safe space for practicing social interactions and emotional expression

Installation & Setup
Prerequisites

Python 3.8+
ffmpeg (required for audio processing)
Groq API key
ElevenLabs API key

Installation
bashCopy# Install ffmpeg (Ubuntu/Debian)
sudo apt update
sudo apt install ffmpeg

# Install ffmpeg (macOS)
brew install ffmpeg

# Install ffmpeg (Windows)
# Download from https://ffmpeg.org/download.html

# Clone the repository
git clone https://github.com/arun7197/Echo-AI-V2.git
cd Echo-AI-V2

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
Secrets Configuration
Create a .streamlit/secrets.toml file in the project directory with:
tomlCopyGROQ_API_KEY = "your_groq_api_key"
ELEVENLABS_API_KEY = "your_elevenlabs_api_key"
Future Improvements

Sentiment Analysis: Implementation of advanced sentiment analysis to better detect user emotions
Reduced Latency: Optimize speech processing and model response times
Full Stack Application: Develop a comprehensive application with dedicated backend, frontend, and mobile interfaces
User Profiles: Allow multiple users with personalized conversation history and preferences
Offline Mode: Enable basic functionality without internet connection

License
MIT
Acknowledgements

Groq for their powerful and accessible LLM API
ElevenLabs for their realistic text-to-speech technology
Streamlit for enabling rapid development of interactive web applications

