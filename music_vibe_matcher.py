 # AI-Powered Music Vibe Matcher (Enhanced Version) 

import streamlit as st
import os
import json
from datetime import datetime
from quotes import get_random_quote
from collections import Counter
import pandas as pd
from textblob import TextBlob
import openai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

#Load environment variables
load_dotenv()

# Set OpenAI and Spotify credentials
openai.api_key = os.getenv("OPENAI_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Spotify API initialization
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))


# Set page config
st.set_page_config(page_title="AI Music Mood Mate", layout="centered")

MEMORY_FILE = "user_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return {"interactions": []}

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=4)

# 🎤 Voice Output using Web Speech API (in-browser)
def speak(text):
    st.components.v1.html(f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{text}");
            window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# 🎙️ Voice Input from Microphone
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Speak now...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I didn’t catch that.")
        return ""




   
# Your existing logic (voice input, GPT reply, Spotify search) can be inserted below this comment:


# 📊 Sentiment-based Mood Detection
def detect_mood(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.2:
        return "happy"
    elif polarity < -0.2:
        return "sad"
    else:
        return "neutral"

# Spotify search
def search_spotify(query, search_type='track'):
    try:
        results = sp.search(q=query, type=search_type, limit=1)
        if search_type == 'track':
            return results['tracks']['items'][0]['external_urls']['spotify']
        elif search_type == 'playlist':
            return results['playlists']['items'][0]['external_urls']['spotify']
    except:
        return None

# GPT response
def gpt_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly music therapist. Be supportive and cheerful."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip()
    except:
        return "I'm having trouble responding at the moment."

# 📒 Log Mood & Messages
def log_interaction(memory, mood, user_input):
    memory['interactions'].append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mood": mood,
        "input": user_input
    })
    save_memory(memory)


# ------------------ Sidebar ------------------
st.sidebar.title("⚙️ Settings")
user_name = st.sidebar.text_input("Enter Your Name", "name")


# ------------------ Main UI ------------------
st.markdown(f"## 🎵 Hello, {user_name}! Let's vibe with music.")
st.markdown(f"> {get_random_quote()}")

memory = load_memory()
user_choice = st.radio("How do you want to interact?", ["🎙️ Voice Input", "📝 Type It"])

def handle_input(user_input):
    if "play" in user_input.lower():
        song_query = user_input.lower().replace("play", "").strip()
        music_link = search_spotify(song_query, search_type='track')
        if music_link:
            response_text = f"Sure! Playing {song_query}. Enjoy!"
            st.success(response_text)
            st.markdown(f"[🎶 Click to play]({music_link})", unsafe_allow_html=True)
            speak(response_text)
        else:
            st.warning("Sorry, I couldn’t find that song.")
            speak("Sorry, I couldn’t find that song.")
    else:
        mood = detect_mood(user_input)
        log_interaction(memory, mood, user_input)
        reply = gpt_response(user_input)

        # Supportive feedback for sad moods
        if mood == "sad":
            comfort = "Hey, I’m here for you. Let’s brighten your day with some music."
            st.info(comfort)
            speak(comfort)
        else:
            speak(reply)

        st.success(reply)
        st.write(f"🎵 **Detected Mood:** {mood.capitalize()}")
        playlist_link = search_spotify(f"{mood} music", search_type='playlist')
        if playlist_link:
            st.markdown(f"[🎶 Click here to listen to a {mood} playlist]({playlist_link})", unsafe_allow_html=True)

# 📈 Show Mood Insights
def show_insights(memory):
    moods = [entry['mood'] for entry in memory['interactions']]
    st.write("## Mood Insights")
    st.write(f"😊 Happy: {moods.count('happy')}")
    st.write(f"😢 Sad: {moods.count('sad')}")
    st.write(f"😐 Neutral: {moods.count('neutral')}")

# 🎙️ Voice Interaction
if user_choice == "🎙️ Voice Input":
    if st.button("Start Listening"):
        user_input = get_voice_input()
        if user_input:
            handle_input(user_input)

# 💬 Text Interaction
elif user_choice == "📝 Type It":
    text_input = st.text_input("Tell me how you feel or ask to play a song:")
    if st.button("Submit"):
        if text_input:
            handle_input(text_input)

# 📊 Mood History
if st.checkbox("📊 Show My Mood Insights"):
    show_insights(memory)

    
