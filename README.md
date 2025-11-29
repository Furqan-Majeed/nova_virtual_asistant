# Nova - AI Voice Assistant 🎙️

Nova is a Python-based virtual assistant designed for macOS. It leverages **Google's Gemini 2.0 Flash model** for ultra-fast conversational intelligence and uses **macOS native text-to-speech** for a natural, high-quality voice interface.

## 🚀 Features

* **Wake Word Detection:** Always listening for "Nova" to activate.
* **Intelligent Conversation:** Uses Google Gemini AI to answer complex queries concisely.
* **Web Automation:** Opens websites like Google, YouTube, LinkedIn, etc.
* **Music Player:** Plays specific songs from a library upon command.
* **News Reader:** Fetches and reads the top US headlines using NewsAPI.
* **Graceful Exit:** Shuts down via voice commands ("Bye", "Exit", "Close").

## 🛠️ Tech Stack

* **Python 3.x**
* **SpeechRecognition** (Google Speech API)
* **Google Generative AI** (Gemini 2.0 Flash)
* **Requests** (API calls)
* **OS System Calls** (Mac `say` command)

## ⚙️ Prerequisites

Since this project uses the native macOS `say` command for the voice, it is currently **optimized for macOS**. Windows/Linux users will need to replace the `speak()` function with `pyttsx3` or `gTTS`.

You will need API Keys for:
1.  **Google Gemini AI:** [Get Key Here](https://aistudio.google.com/)
2.  **NewsAPI:** [Get Key Here](https://newsapi.org/)

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Nova-Voice-Assistant.git](https://github.com/YOUR_USERNAME/Nova-Voice-Assistant.git)
    cd Nova-Voice-Assistant
    ```

2.  **Install Dependencies**
    ```bash
    pip install speechrecognition google-generativeai requests
    ```
    *(Note: PyAudio is also required. On Mac, use `brew install portaudio` then `pip install pyaudio`)*

3.  **Setup Configuration**
    Open `main.py` and replace the placeholder keys with your actual API keys:
    ```python
    news_api = "YOUR_NEWS_API_KEY"
    gemini_api_key = "YOUR_GEMINI_API_KEY"
    ```

## 🎤 Usage

Run the script:
```bash
python main.py
