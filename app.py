from flask import Flask, render_template, request, jsonify
from google.adk.runners import InMemoryRunner
from google.genai import types
import asyncio
import os

app = Flask(__name__)


runner = None
fallback_runner = None
character_exists = os.path.exists('character.py')

if character_exists:
    import character
    from google.adk.agents.llm_agent import LlmAgent
    
    runner = InMemoryRunner(
        agent=character.root_agent,
        app_name="Demo App",
    )
    
    fallback_agent = LlmAgent(
        model='gemini-2.5-flash',
        name=character.root_agent.name,
        instruction=character.root_agent.instruction,
    )
    fallback_runner = InMemoryRunner(
        agent=fallback_agent,
        app_name="Demo App Fallback",
    )






# Map language codes to their respective language names
LANG_MAP = {
    'hi': 'Hindi',
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'ja': 'Japanese',
    'zh': 'Chinese',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ko': 'Korean',
}

async def _run_agent(runner, session_id, content):
    """Helper to run an ADK agent runner with retry logic and session management."""
    adk_session = await runner.session_service.get_session(
        app_name=runner.app_name, user_id="inapp_user", session_id=session_id
    )
    if adk_session is None:
        adk_session = await runner.session_service.create_session(
            app_name=runner.app_name, user_id="inapp_user", session_id=session_id
        )

    for attempt in range(3):
        try:
            response_text = ""
            async for event in runner.run_async(
                user_id=adk_session.user_id,
                session_id=adk_session.id,
                new_message=content,
            ):
                if event.content and event.content.parts and len(event.content.parts) > 0:
                    response_text += event.content.parts[0].text or ""
            return response_text, True
        except Exception as e:
            print(f"Runner {runner.app_name} attempt {attempt+1} failed: {e}")
            if ("429" in str(e) or "RESOURCE_EXHAUSTED" in str(e)) and attempt < 2:
                await asyncio.sleep(5)
                continue
            break
    return "", False

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
async def chat():
    user_message = request.json.get('message')
    session_id = request.json.get('session_id', 'default_session')
    language_code = request.json.get('language', 'en-US')

    if not character_exists:
        return jsonify({'response': user_message})

    lang_prefix = language_code.split('-')[0].lower() if language_code else 'en'
    lang_name = LANG_MAP.get(lang_prefix, 'English')

    # Embed target language request in system context instructions
    prompt_text = f"{user_message}\n\n[System constraint: Please respond in {lang_name} language]"
    content = types.Content(role="user", parts=[types.Part(text=prompt_text)])

    # Try the primary runner
    response_text, success = await _run_agent(runner, session_id, content)
            
    # If the primary runner fails, run the fallback runner
    if not success:
        print("Primary runner failed. Switching to fallback_runner (gemini-2.5-flash)...")
        response_text, success = await _run_agent(fallback_runner, session_id, content)

    if not success:
        response_text = "I'm so sorry, yaar! The servers are super busy right now. Let's take a quick 10-second break, and then we can definitely try again!"

    return jsonify({'response': response_text})


if __name__ == '__main__':
    app.run(debug=True)
