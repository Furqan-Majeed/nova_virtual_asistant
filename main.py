import speech_recognition as sr  # Imports library to convert spoken audio into text
import webbrowser                # Imports library to open websites in the default browser
import musicLibrary              # Imports a local custom module containing song links
import requests                  # Imports library to make HTTP requests (used for News API)
import google.generativeai as genai # Imports the Google Gemini AI library
import os                        # Imports interface to interact with the operating system (used for Mac commands)

# --- CONFIGURATION ---
news_api = "fa0a48e7c23f4037b887554be0b9d0c8" # API key for authenticating with NewsAPI.org
gemini_api_key = "AIzaSyBoJbjAcQ5isOmLS-WjdIrzbI16gUCZpZA" # API key for authenticating with Google Gemini

# Configure Gemini (Using the fast 2.0 model)
genai.configure(api_key=gemini_api_key) # Sets up the Gemini client with your provided key
model = genai.GenerativeModel('models/gemini-2.0-flash') # Selects the 'Flash' model which is optimized for speed/latency

# Initialize Recognizer ONCE (Better performance)
recognizer = sr.Recognizer() # Creates the recognizer object used to process audio

def speak(text):
    # Uses Mac's native voice. 
    # Sanitizes text by removing quotes so they don't break the terminal command
    safe_text = text.replace('"', '').replace("'", "")
    # Executes the macOS 'say' command via terminal. 
    # -v Samantha: Uses the high-quality 'Samantha' voice.
    # -r 175: Sets the speaking rate to 175 words per minute.
    os.system(f'say -v Samantha -r 175 "{safe_text}"')

def aiProcess(command):
    try:
        # Defines the persona for the AI. Note: Code says 'Edith' here based on previous context.
        prompt = f"You are a helpful voice assistant named Edith. Answer this concisely in 1-2 sentences: {command}"
        # Sends the text prompt to Google servers to generate a response
        response = model.generate_content(prompt)
        # Returns the text content, removing asterisks (*) to clean up formatting
        return response.text.replace("*", "")
    except Exception as e:
        # Prints specific error if AI fails
        print(f"AI Error: {e}")
        return "I'm sorry, I couldn't reach the server."

def processCommand(c):
    print(f"Processing command: {c}") # Debugging print to show what command is being executed

    # Check if the command is exactly "open google"
    if c.lower() == "open google":
        webbrowser.open("https://google.com") # Opens Google in browser
    elif c.lower() == "open facebook":
        webbrowser.open("https://facebook.com") # Opens Facebook
    elif c.lower() == "open youtube":
        webbrowser.open("https://youtube.com") # Opens YouTube
    elif c.lower() == "open linkedin":
        webbrowser.open("https://linkedin.com") # Opens LinkedIn
    
    # Check if the command starts with the word "play"
    elif c.lower().startswith("play"):
        try:
            # Splits the sentence by space and takes the second word (index 1) as the song name
            song = c.lower().split(" ")[1]
            # Looks up the URL associated with that song name in the musicLibrary file
            link = musicLibrary.songs[song]
            webbrowser.open(link) # Opens the song link
        except:
            # Handles errors (e.g., song not found or index error)
            speak("I couldn't find that song.")

    # Check if the word "news" is anywhere in the command
    elif "news" in c.lower():
        # Requests top US headlines from the News API
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api}")
        
        # Check if the request was successful (HTTP Status 200)
        if r.status_code == 200:
            data = r.json() # Parse the JSON response
            articles = data.get("articles", []) # Extract the list of articles
            # Loop through the first 10 articles
            for article in articles[:10]:
                print(article["title"]) # Print title to console
                speak(article["title"]) # Read title aloud
    
    else:
        # AI Fallback: If no command matches above, send query to Gemini
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing NOVA...") # startup message

    while True: # Starts the infinite loop to keep the assistant running
        try:
            # Use the default microphone as the audio source
            with sr.Microphone() as source:
                print("\nListening for Wake Word...")
                # Calibrate the recognizer for 0.5 seconds to account for background noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # timeout=3: Wait 3 seconds for speech to start. 
                # phrase_time_limit=None: Do not cut off the user while they are speaking.
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=None)
            
            # Convert the recorded audio to text using Google's speech recognition service
            word = recognizer.recognize_google(audio)
            
            # --- YOUR EXIT COMMAND ---
            # Checks if the user said any of the exit keywords
            if word.lower() in ["close", "exit", "stop", "bye"]:
                speak("Will always be there to assist you. Goodbye.")
                break # Breaks the while loop, ending the program

            # --- WAKE WORD ---
            # Checks if "nova" is present anywhere in the spoken phrase
            elif "nova" in word.lower():
                print(f"Heard: {word}") # Prints what was heard for debugging
                speak("Yes?") # Acknowledges the wake word
                
                # Opens microphone again to listen for the actual command
                with sr.Microphone() as source:
                    print("Active...")
                    # Recalibrates for noise again briefly
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    # Listens for the command (timeout=5 gives user 5s to start speaking command)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=None)
                    # Converts command audio to text
                    command = recognizer.recognize_google(audio)
                    # Passes the text to the processing function
                    processCommand(command)
            else:
                # Logs that something was heard, but it wasn't the wake word
                print(f"Heard: {word} The Wake Word Is NOVA")


        # --- ERROR HANDLING BLOCKS ---
        except sr.WaitTimeoutError:
            # Triggered if no speech is detected within the timeout period
            print("❌ Error: Timeout (I didn't hear anything)")
        except sr.UnknownValueError:
            # Triggered if speech was heard but couldn't be understood (unclear audio)
            print("❌ Error: Audio was not clear (I heard sound but couldn't understand words)")
        except sr.RequestError:
            # Triggered if there is no internet connection or API issues
            print("❌ Error: No Internet Connection or API Limit reached")
        except Exception as e:
            # Catches any other unexpected errors to prevent crashing
            print(f"❌ Critical Error: {e}")