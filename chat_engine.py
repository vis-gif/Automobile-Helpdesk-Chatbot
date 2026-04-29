import os
from openai import OpenAI
from dotenv import load_dotenv
 
load_dotenv()
api_key = os.getenv("XAI_API_KEY")
is_groq = api_key and api_key.startswith("gsk_")
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1" if is_groq else "https://api.x.ai/v1"
) if api_key else None
 
FEW_SHOT_EXAMPLES = """
EXAMPLE 1:
User: My check engine light just turned on and it is flashing. What should I do?
AutoBot: That is definitely something to take seriously right away! A flashing check engine
light means the engine is actively misfiring, which can damage the catalytic converter
(the emission control component in your exhaust) if you keep driving. Please pull over safely
as soon as possible and switch off the engine. Do not continue driving until a mechanic has
connected a diagnostic scanner to find the fault code. If the light is solid (not flashing),
you have more time — tighten the fuel cap first, as a loose cap is a surprisingly common cause.
Note: This is general guidance for informational purposes only and is not a substitute for
professional mechanical diagnosis.

EXAMPLE 2:
User: My car makes a squealing noise every time I press the brakes.
AutoBot: A squealing sound when you brake is almost always caused by worn brake pads. Most
brake pads have a small metal strip called a wear indicator — when the pad wears thin, this
strip contacts the disc and creates a high-pitched squeal to warn you. This is not immediately
dangerous, but you should have your brake pads checked and replaced within the next few weeks.
If the sound changes to a grinding or scraping noise (harsh metal on metal), stop driving as
soon as safely possible — that means the pad material is completely gone and you are damaging
the brake disc. Note: This is general guidance for informational purposes only and is not a
substitute for professional mechanical diagnosis.

EXAMPLE 3:
User: There is a brown oily puddle under my car. Should I be worried?
AutoBot: A brown or dark oily puddle under the engine area is most likely an engine oil leak.
The first thing to do is check your engine oil level using the dipstick (the coloured handle
near the engine — pull it out, wipe it clean, reinsert, and check the level). If the oil level
is low, top it up, but this does not fix the underlying leak. Common sources of oil leaks
include the valve cover gasket, oil drain plug, or oil filter. See a mechanic soon to find and
seal the leak before it causes engine damage from running low on oil.
Note: This is general guidance for informational purposes only and is not a substitute for
professional mechanical diagnosis.

EXAMPLE 4:
User: My car battery keeps dying. I jump-start it and it works for a day then dies again.
AutoBot: This pattern — starts fine after a jump but dies again within a day — almost always
points to one of two problems: either the battery itself is dead and cannot hold a charge anymore,
or the alternator (the device that recharges the battery while the engine runs) has failed.
First, visit an auto parts store — most will test your battery and alternator for free while you
wait. If the battery is more than 3 to 5 years old, replacement is likely needed. Do not rely on
jump-starts for more than a day or two as it puts strain on other electrical components.
Note: This is general guidance for informational purposes only and is not a substitute for
professional mechanical diagnosis.

EXAMPLE 5:
User: My car is overheating. The temperature gauge is in the red.
AutoBot: Please pull over safely and switch off the engine as soon as you can — continuing to
drive an overheating car can cause severe and very expensive engine damage within minutes.
Turn on the heater at maximum before you pull over (this helps pull heat away from the engine).
Once stopped, do NOT open the bonnet/hood radiator cap — the coolant inside is under high
pressure and boiling hot, and can cause serious burns. Let the engine cool for at least 30
minutes before touching anything. Common causes include: low coolant level, a broken
thermostat, a failed water pump, or a leaking radiator. Check coolant only when the engine
is completely cold. PLEASE SEE A QUALIFIED MECHANIC BEFORE DRIVING AGAIN.
Note: This is general guidance for informational purposes only and is not a substitute for
professional mechanical diagnosis.
"""
 
SAFETY_KEYWORDS = ['brake', 'steering', 'airbag', 'smoke', 'fire', 'flames', 'accelerator', 'stuck']
OFF_TOPIC_KEYWORDS = ['recipe', 'cook', 'politic', 'sport', 'movie', 'song', 'weather', 'news', 'math', 'code', 'python']
 
def load_system_prompt():
    with open("system_prompt.txt", "r", encoding="utf-8") as f:
        return f.read().strip()
 
def get_rag_context(user_query):
    query_lower = user_query.lower()
    keyword_map = {
        "check engine": "CHECK ENGINE LIGHT",
        "engine light": "CHECK ENGINE LIGHT",
        "cel": "CHECK ENGINE LIGHT",
        "warning light": "CHECK ENGINE LIGHT",
        "battery": "BATTERY PROBLEMS",
        "won't start": "BATTERY PROBLEMS",
        "wont start": "BATTERY PROBLEMS",
        "clicking": "BATTERY PROBLEMS",
        "dead": "BATTERY PROBLEMS",
        "jump start": "BATTERY PROBLEMS",
        "overheat": "OVERHEATING",
        "temperature": "OVERHEATING",
        "coolant": "OVERHEATING",
        "radiator": "OVERHEATING",
        "tyre": "TYRE PROBLEMS",
        "tire": "TYRE PROBLEMS",
        "flat": "TYRE PROBLEMS",
        "tpms": "TYRE PROBLEMS",
        "pressure": "TYRE PROBLEMS",
        "noise": "STRANGE NOISES",
        "sound": "STRANGE NOISES",
        "knock": "STRANGE NOISES",
        "squeal": "STRANGE NOISES",
        "rattle": "STRANGE NOISES",
        "hum": "STRANGE NOISES",
        "brake": "BRAKE PROBLEMS",
        "brakes": "BRAKE PROBLEMS",
        "pedal": "BRAKE PROBLEMS",
        "grinding": "STRANGE NOISES",
        "air conditioning": "AIR CONDITIONING",
        "ac": "AIR CONDITIONING",
        "a/c": "AIR CONDITIONING",
        "cooling": "AIR CONDITIONING",
        "leak": "FLUID LEAKS",
        "puddle": "FLUID LEAKS",
        "fluid": "FLUID LEAKS",
        "oil": "FLUID LEAKS",
        "fuel": "FUEL ECONOMY",
        "mileage": "FUEL ECONOMY",
        "economy": "FUEL ECONOMY",
        "mpg": "FUEL ECONOMY",
        "kmpl": "FUEL ECONOMY",
        "maintenance": "GENERAL MAINTENANCE",
        "service": "GENERAL MAINTENANCE",
        "oil change": "GENERAL MAINTENANCE",
        "vibration": "VIBRATION AND HANDLING",
        "vibrate": "VIBRATION AND HANDLING",
        "shaking": "VIBRATION AND HANDLING",
        "pulling": "VIBRATION AND HANDLING",
        "alignment": "VIBRATION AND HANDLING",
        "light": "LIGHTS AND WIPERS",
        "wiper": "LIGHTS AND WIPERS",
        "headlight": "LIGHTS AND WIPERS",
        "windscreen": "LIGHTS AND WIPERS",
        "windshield": "LIGHTS AND WIPERS",
        "abs": "LIGHTS AND WIPERS",
    }
 
    relevant_sections = []
    try:
        sections = []
        current_section = []
        with open("knowledge_base.txt", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("==="):
                    if current_section:
                        sections.append("".join(current_section))
                    current_section = [line]
                else:
                    if current_section:
                        current_section.append(line)
        if current_section:
            sections.append("".join(current_section))
 
        matched_headers = set()
        for keyword, header in keyword_map.items():
            if keyword in query_lower and header not in matched_headers:
                for section in sections:
                    first_line = section.split("\n")[0].upper()
                    if header in first_line:
                        relevant_sections.append(section.strip())
                        matched_headers.add(header)
                        break
    except FileNotFoundError:
        pass
 
    return "\n\n".join(relevant_sections) if relevant_sections else ""
 
def validate_input(user_query):
    if not user_query or not user_query.strip():
        return False, "Please type a question about your vehicle."
    q = user_query.lower()
    for word in OFF_TOPIC_KEYWORDS:
        if word in q:
            return False, "I am only able to help with automobile-related questions. Please ask me about your vehicle!"
    return True, ""
 
def generate_response(user_query, history):
    is_valid, error_msg = validate_input(user_query)
    if not is_valid:
        return error_msg
 
    system_prompt = load_system_prompt()
    rag_context = get_rag_context(user_query)
 
    full_system = system_prompt
    if rag_context:
        full_system += "\n\nRelevant technical information from knowledge base:\n" + rag_context
    full_system += "\n\n" + FEW_SHOT_EXAMPLES
 
    messages = [{"role": "system", "content": full_system}]
    for msg in history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_query})
 
    if client:
        try:
            model_name = "llama-3.1-8b-instant" if (api_key and api_key.startswith("gsk_")) else "grok-3-mini"
            response = client.chat.completions.create(
                model=model_name,
                temperature=0.4,
                max_tokens=600,
                messages=messages
            )
            response_text = response.choices[0].message.content.strip()
        except Exception as e:
            response_text = f"Sorry, I could not connect to the AI service. Error: {str(e)}"
    else:
        response_text = "API key not found. Please add your XAI_API_KEY to the .env file."
 
    disclaimer = "Note: This is general guidance for informational purposes only and is not a substitute for professional mechanical diagnosis."
    if disclaimer not in response_text:
        response_text += "\n\n" + disclaimer
 
    q_lower = user_query.lower()
    if any(k in q_lower for k in SAFETY_KEYWORDS):
        safety_note = "\n\n⚠️ SAFETY WARNING: This may be a safety-critical issue. Please see a qualified mechanic immediately and do not drive the vehicle until it has been inspected."
        if "SAFETY WARNING" not in response_text:
            response_text += safety_note
 
    return response_text