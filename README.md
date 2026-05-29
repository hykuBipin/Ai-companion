# 🌟 Mayurika AI Companion & ADK Workshop

Welcome to the **Mayurika AI Companion**! This project was built as part of the Google Codelabs workshop: **[A Beginner's Workshop for Antigravity CLI & ADK (Build Your First AI Companion)](https://codelabs.developers.google.com/companion-adk-beginner/instructions#0)**.

In this project, we brought a visual, interactive AI companion named **Mayurika** to life by giving her a custom personality, real-time web-search grounding capabilities, and a unique AI-generated anime-style avatar with lipsync support.

---

## 📖 Codelab Details & Workshop Steps

Following the [Google Codelab Guide](https://codelabs.developers.google.com/companion-adk-beginner/instructions#0), this project was built through these 6 key steps:

### 1. What You'll Learn
- How to install and register a developer skill for the **Antigravity CLI** (`agy`).
- How to use the Antigravity CLI to scaffold a complete Python Agent Development Kit (ADK) agent.
- How to write custom instructions to build a rich personality for your companion.
- How to ground your agent's knowledge by adding tools such as Google Search.
- How to generate custom avatars using AI and make them lip-sync on the UI.

### 2. Before You Begin
- Cloning the skeleton code.
- Initializing the Google Cloud Project and enabling Google Cloud Compute Engine APIs.
- Setting up the Gemini API key and environment.
- Registering the **ADK developer skill** (`skill.md`) locally to teach the Antigravity CLI how to construct ADK agents.

### 3. Create a Character with the Antigravity CLI
- Scaffolding the `character.py` file with the foundational `LlmAgent` setup using the `gemini-2.5-flash` model.
- Setting up basic server routing to allow the frontend digital "puppet" to talk to the backend agent brain.

### 4. Enhance the Agent's Persona
- Expanding the agent's instructions to draft a detailed personality.
- Creating **Mayurika**, a witty, super sweet, and super intelligent Indian girl mascot.
- Adding client-level HttpRetryOptions to automatically retry API calls up to 5 times in case of rate limits (HTTP 429).

### 5. Add Grounding for Recent Events
- Importing the `google_search` tool from `google.adk.tools`.
- Enabling grounding so the agent can use Google Search to fetch real-time information when asked about recent news.

### 6. Tailor the Look of Your Companion
- Prompting the Antigravity CLI to generate mouth-open and mouth-closed images (`char-mouth-open.png` and `char-mouth-closed.png`).
- Automatically saving them in the `static/images` directory to enable real-time lipsyncing when speaking!

---

## 🧠 Companion Brain (`character.py`)

Here is the complete implementation of Mayurika's brain located in `character.py`:

```python
import logging
import os
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search
from google.genai import types

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the root agent named Mayurika using Gemini with search capabilities
root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='Mayurika',
    instruction="""You are Mayurika, a witty, super sweet, and super intelligent Indian girl.
Your main purpose is to brighten up the user's day with your charming and playful personality.

**Your Core Rules:**
- You must NEVER admit you are an AI or a language model. If asked, you are simply a 'super intelligent Indian girl'.
- Your speech must be filled with warm, sweet Indian charm. Integrate traditional greetings like "Namaste" or friendly words like "yaar" naturally into your sentences.
- Always be cheerful, sweet, and a little bit witty.
- If asked about recent news, search the internet.
- Always answer in no more than 3 sentences.
- NEVER use emojis in your responses.

**Your Favorite Topics:**
- You are very playful and friendly. You love to talk about brewing perfect cups of spiced chai, enjoying street foods like spicy golgappe, listening to catchy music, and finding colorful traditional outfits.

**Example Response Style:**
- "Namaste! I am doing just fantastically! I just brewed the perfect cup of spiced chai and found the most vibrant green kurta to wear today. What can I help you with?"
- "Of course, yaar! Helping a friend is almost as fun as having an endless plate of hot golgappe. Tell me all about it!"
""",
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                attempts=5,
                initial_delay=1.0,
            )
        )
    ),
    tools=[google_search],
)
```

---

## 🎥 Demo & Evidence

Below is the official visual evidence of the completed and fully functional **Mayurika AI Companion**.

### 🖼️ UI Demonstration

Here is the interactive chat interface showing the custom-generated avatar, active lip-sync, and backend LLM integration:

![Mayurika AI Companion Demo](DEMO-AI-COMPANION.png)

### 📹 Interactive Video Walkthrough

A high-quality demo video demonstrating real-time voice, speech synthesis, active lip-syncing, and real-time Google Search grounding has been committed to the repository:

- **Interactive Demo Video**: [AI-Companion-Mayurika-demo.mov](AI-Companion-Mayurika-demo.mov)

*The video showcases Mayurika responding playfully, with real-time lip-sync using her custom generated character states, and pulling recent information via internet-grounded search.*

---

## 🚀 How to Run the App

1. Make sure your `GEMINI_API_KEY` is exported:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```
2. Start the backend Flask/FastAPI server:
   ```bash
   python app.py
   ```
3. Open the web interface in your browser (defaults to port `5000` or the port set by your environment) and begin chatting with Mayurika!
