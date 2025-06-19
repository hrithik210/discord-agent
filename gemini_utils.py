import google.generativeai as genai
import os
import random

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def generate_roast(lines_added):
    praise = [
        f"Okayyy! {lines_added} lines? Productivity king 😤✨",
        f"Damn, you cooked today — {lines_added} lines, let's goo 🚀",
        f"Okay coder! That’s {lines_added} lines of pure magic."
    ]

    roast = [
        f"{lines_added} lines? Bro did you just format code and call it a day?",
        f"{lines_added} lines... grandma typed more in her sleep. Get up. 😒",
        f"You committed {lines_added} lines. That's cute. Now double it."
    ]

    message_type = "praise" if lines_added > 25 and random.random() < 0.4 else "roast"
    prompt = random.choice(praise if message_type == "praise" else roast)

    response = model.generate_content(prompt)
    return response.text.strip()
