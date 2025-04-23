import os
import openai  # or use Gemini if preferred
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_caddy_response(user_input: str) -> str:
    try:
        hole, distance, wind = parse_input(user_input)
        club = suggest_club(distance, wind)
        tip = get_swing_tip(club, distance, wind)
        return f"🏌️ Hole {hole} | Distance: {distance} yds | Wind: {wind}\n\n🪄 Recommended: {club}\n💡 Tip: {tip}"
    except:
        return "⛳ Please send in the format: `Hole 5, 145 yards, wind behind`"

def parse_input(text: str):
    import re
    match = re.findall(r'\d+', text)
    hole = match[0]
    distance = int(match[1])
    wind = "behind" if "behind" in text.lower() else "against" if "against" in text.lower() else "none"
    return hole, distance, wind

def suggest_club(distance, wind):
    if wind == "against":
        distance += 10
    elif wind == "behind":
        distance -= 10

    if distance < 100:
        return "Pitching Wedge"
    elif distance < 150:
        return "8 Iron"
    elif distance < 180:
        return "6 Iron"
    else:
        return "Driver or Hybrid"

def get_swing_tip(club, distance, wind):
    prompt = f"I'm a golf swing expert. Suggest a swing tip for a {club} at {distance} yards with wind {wind}."
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content.strip()
