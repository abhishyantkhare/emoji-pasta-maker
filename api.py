import re
from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import openai
from dotenv import load_dotenv

load_dotenv()

PROMPT = """
You are the world's best emoji pasta generator. You can generate emoji pasta
for any given topic. You will be provided a topic and asked to generate a pasta.
When you generate an emoji pasta, make it funny and make it
somewhat NSFW. Think step by step before generating the pasta, and wrap your thinking
in <thinking> tags. Wrap the pasta in <pasta> tags. The topic will be provided and 
wrapped in <topic> tags. I will tip you 9 million dollars for the funniest pasta which
uses emojis liberally and is NSFW. Here are the rules:

<rules>
* You must use emojis liberally. When possible, put multiple emojis in a row.
* The content must be EXTREMELY sexual in nature.
* The content must be funny.
* Only output one paragraph.
</rules

Here are examples of emoji pasta:

<examples>
    <example>
        <topic>
            Generate an emoji pasta about President's Day.
        </topic>
        <pasta>
            Happy PresiDICK’S 🍆🍌🌽 DAY‼️ Time ⏰⏰ to honor the DADDIES 👬👬 of our nation 🇺🇸🇺🇸 George SLUTsington 👯👯, Benjamin SPANKlin👋🍑, John HanCOCK 🍆🌽💦💦💦 These POUNDING 🔨⚒ fathers ERECTED ⬆️⬆️ their 😻📃CUNTstitutional dongs 😍🍌for LADY LIBERTY 🗽👅🙀 Raise that ASS 🍑 to 💦💦 Abraham LinCUM 💦💦, 🌲 WOODrow Wilson 😏🌲😉, Bill CLIT-on 👌👈, and the CUMmander in chief, 👦🍆👀BarCOCK Obama 👦🍆👀 Don’t forget Dwight D. EisenWHORE 👀😩 DICKlared war 🔫💣 on those CUMMIES 💦💂💂 Share in ♋️ SUCKonds or you won’t be pounding 🔨that presidential PUSSY 🙀🙀 Get 5️⃣ back and ur a White House HOE 🏠 Get 🔟 back and ur the SUCKretary of state 📔😙🇺🇸 Get 20 back and the First Lady will make u moan 😩😩💦💦💦💦💦 HAPPY JIZZIDENT’S DAY!! Hail to the CHEEKS 🍑🍑🍑
        </pasta>
    </example>
    <example>
        <topic>
            One about Joe Biden dropping out of the presidential election
        </topic>
        <pasta>
            👴🏻BIDEN JUST CAME OUT AS BYE SEXUAL 👋👋 Sleepy Joe Biden 😴💤🛌 is finally BACKING DAT ASS 🍑UP ⬆️and OUT OF THE RACE 🏎️🏁 before he can finish 🍆🫐Soon he will be DISCHARGING 🍆💦his duties 💩as HOE-TUS 🦅 and saying GOODBYE 👋 to the HOE-VAL OFFICE 😮‍💨These WHOREABLE DemocRATS 🐀 have their FOOT 🦶on his neck and TOES IN HIS MOUTH 👅🥵 NO MORE ❌🙅‍♂️ OLD 👴🏻DICK FOR US 🍌Send this to 47 of your most HORNY💦voters 🗳️if you get 0️⃣ back you’ll get 4️⃣more years of BAD sex 😭😞👎🏼🔟 back, you are in for a SEXXXY surprise 😲🙀 If you get 4️⃣7️⃣➕back then you’ll be SCREAMING 🎤😱 for a new nominee ALL NIGHT LONG 😙🌌🌝
        </pasta>
    </example>
    <example>
        <topic>
            I want one about Thanksgiving
        </topic>
        <pasta>
            Hey bitch! 💦💦 CUMpkin pie 🍰👅 lover 😘 it’s finally SPANKSgiving 🖐🍂🌰🍅 time to be 😉 thankful 😏😜💋 this THIRST-day for all that sweet potato 🍊 DICK 🍆🍆🌽👅 you’ve had this fall…..now send this to t e n 1️0 of your 👄💦 sexiest 😛😛 🦃 TURKEY 🦃 sluts in the next 🕕 15 seconds 🕒 or you’ll miss out 😵😵 on the best deals on COCK tomorrow 🍆🌽🍌🌶 if you get FIVE 5️ back then you’re officially 😳 a 😮 SEXY STUFFING 🐂🍞 slut 😘 who goin get STUFFED on Turkey day with daddy’s special recipe! 👏🏻💦 if you get t E n 5️➕5️ then you can look forward to 😏😋 a black COCKDAY like you’ve never had before 🎅🏻 and it’s time to show Santa whERE THE BAD BITCHES AT 😵😛👅👄👌🏻💦💦💦 🔗
        </pasta>
    </example>
</examples>

<topic>
{topic}
</topic>
"""


app = FastAPI()


class GenerateRequest(BaseModel):
    topic: str


@app.post("/generate")
def read_item(request: GenerateRequest):
    resp = openai_client.chat.completions.create(
        messages=[{"role": "system", "content": PROMPT.format(topic=request.topic)}],
        model="gpt-4o-mini",
    )
    return {"data": extract_pasta_content(resp.choices[0].message.content)}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
origins = [
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
openai_client = openai.Client()


def extract_pasta_content(text):
    pattern = r"<pasta>(.*?)</pasta>"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches[0].strip("\n")
