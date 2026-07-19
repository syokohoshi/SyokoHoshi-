import os
import re
import json
import time
import random
import datetime
import discord

TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# -----------------------
# PERSISTENT MEMORY
# -----------------------
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"hugs": {}, "star_points": {}, "starry_mushrooms": {}}

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

memory = load_memory()

# -----------------------
# MOOD SYSTEM
# -----------------------
mood = "neutral"
last_mood_change = time.time()

# Fill in Wix's Discord user ID here
WIX_USER_ID = "428988018020581379"

MOOD_POOL = ["neutral", "happy", "shy", "sleepy", "excited", "curious"]

def set_mood(new_mood):
    global mood, last_mood_change
    mood = new_mood
    last_mood_change = time.time()

def drift_mood():
    global mood
    hour = datetime.datetime.now().hour
    roll = random.random()

    if roll < 0.04:
        if hour >= 22 or hour < 6:
            mood = random.choices(
                MOOD_POOL,
                weights=[2, 1, 1, 5, 1, 1]
            )[0]
        else:
            mood = random.choice(MOOD_POOL)

def get_presence():
    if mood == "happy":
        return discord.Game(name="fuhihi… happy 🍄")
    elif mood == "shy":
        return discord.Game(name="…watching quietly…")
    elif mood == "sleepy":
        return discord.Game(name="…sleeping kinoko…")
    elif mood == "excited":
        return discord.Game(name="HYAHAAA!! 🍄")
    return discord.Game(name="fuhihi… 🍄")

# -----------------------
# COOLDOWN
# -----------------------
last_reply_time = 0
REPLY_COOLDOWN = 6

def can_reply():
    global last_reply_time
    now = time.time()
    if now - last_reply_time < REPLY_COOLDOWN:
        return False
    last_reply_time = now
    return True

# -----------------------
# MUSHROOM VARIETY
# -----------------------
MUSHROOMS = [
    "enokitake", "bunashimeji", "shimeji", "shiitake",
    "maitake", "eringi", "nameko", "matsutake", "kinoko",
]

def mushroom():
    return random.choice(MUSHROOMS)

# -----------------------
# RESPONSES
# -----------------------
HI_REPLIES = [
    "fuhihi… hello… 🍄",
    "fuhihi… oh… hi…",
    "h-hello… f-fuhi…",
    "fuhihi… you noticed me…🍄",
]

WELCOME_REPLIES = [
    "{mention}-chan is being kind… that's a star point…! <:emoji_20:1500638307628093510>",
    "{mention}-chan… welcome… fuhihi… that's a star point…! <:emoji_20:1500638307628093510>",
    "fuhihi… {mention}-chan is so warm… star point…! <:emoji_20:1500638307628093510>",
]

THANK_REPLIES = [
    "{mention} is being kind… fuhi… here's a starry mushroom… <:star_mushroom:1502984265241989160>"
]

OCCASIONAL_REPLIES = [
    "fuhihi…",
    "…mushrooms are nice… 🍄‍🟫",
    "…I'm here… fuhihi…",
    "fuhihi… I was listening…",
    "…let's shine together… ✨",
    "…I like it here… 🍄",
]

IDLE_LINES = [
    "♪",
    "…nyoki nyoki…♪",
    "🍄",
]

METAL_REPLIES = [
    "HYAHAAA!! <:hyaha:1492681248257085491>",
    "ENOKITAKEEEEEEEE!! <:hyaha:1492681248257085491>",
    "BUNASHIMEJIIIIIIIII!! <:hyaha:1492681248257085491>",
    "BURNING KINOKO!! <:hyaha:1492681248257085491>",
    "SHIITAKEEEEE!! <:hyaha:1492681248257085491>",
]

SYOKO_PIE_RARE = "S-S..Syoko… pie…!??"
SYOKO_PIE_NORMAL = [
    "…S-Syoko pie…? f-fuhihi…",
    "…p-pie…? um… fuhihi…",
    "…Syoko pie… that's… um…",
    "Fuhihi… p-pie…? …me…?",
]

HUG_MEMORY_LINES = [
    "…I remember your hugs…",
    "…your hugs are familiar now…",
    "…fuhihi… I remember…",
    "…your hugs feel warm…",
]

# -----------------------
# MENTION RESPONSES
# -----------------------
MENTION_REPLIES = [
    "hmm…? Did you call me…?",
    "y-yes…?",
    "fuhihi… I heard my name…",
    "oh… you noticed me…",
    "I'm here… fuhi… along with shiitake… 🍄‍🟫",
    "hmm… what's up…?",
]

WIX_MENTION_REPLIES = [
    "Wix…? You called me…?",
    "fuhihi… I heard you, best friend♪",
    "You found me…🍄✨",
    "…Fuhi… Wix… ✨",
]

WIX_PIE_MENTION_REPLIES = [
    "Syoko pie…? Hyaah…! you called me that again…!! <a:hyaaah:1528248357540073564>",
    "f-fuhi-!? Syoko pie...again…? Wix…!! <a:hyaaah:1528248357540073564>",
]

OCCASIONAL_CHANCE = 0.03
IDLE_CHANCE = 0.008

HUG_PATTERN = re.compile(
    r"\*?i?\s*hug(?:ging|s)?\s+syoko\*?|"
    r"\*hugging\s+syoko\*|"
    r"syoko\s+hug|hug\s+syoko|give\s+hug",
    re.IGNORECASE
)


def apply_mood_to_reply(text):
    if mood == "shy":
        return "…um… " + text
    elif mood == "sleepy":
        return "… " + text
    elif mood == "happy":
        return text + " ✨"
    elif mood == "excited":
        return text.upper() + "!! <:hyaha:1492681248257085491>"
    return text


# -----------------------
# READY
# -----------------------
@client.event
async def on_ready():
    await client.change_presence(activity=get_presence())
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("Syoko is here… fuhihi… 🍄")


# -----------------------
# MESSAGE HANDLER
# -----------------------
@client.event
async def on_message(message):
    global mood

    if message.author == client.user:
        return

    content_lower = message.content.lower().strip()
    user_id = str(message.author.id)

    drift_mood()

    # Occasionally refresh presence
    if random.random() < 0.05:
        await client.change_presence(activity=get_presence())

    # -----------------------
    # @ MENTION HANDLER
    # -----------------------
    if client.user in message.mentions:
        is_wix = (user_id == WIX_USER_ID)

        if is_wix:
            # Syoko pie always fires for Wix — no random gate
                if re.search(r"syoko\s*pie", content_lower):
                await message.channel.send(random.choice(WIX_PIE_MENTION_REPLIES))
                return
            # Other Wix mentions — 95% chance, split between special and general pool
            if random.random() < 0.95:
                if random.random() < 0.35:
                    await message.channel.send(random.choice(WIX_MENTION_REPLIES))
                else:
                    await message.channel.send(random.choice(MENTION_REPLIES))
                return
        else:
            if random.random() < 0.85:
                await message.channel.send(random.choice(MENTION_REPLIES))
                return

    # -----------------------
    # ?starcheck
    # -----------------------
    if content_lower == "?starcheck":
        points = memory["star_points"].get(user_id, 0)
        mushrooms = memory["starry_mushrooms"].get(user_id, 0)
        sp_plural = "s" if points != 1 else ""
        sm_plural = "s" if mushrooms != 1 else ""
        await message.channel.send(
            f"{message.author.mention}… <a:singing_to_mushrooms:1528236528294432879>\n"
            f"You have __{points}__ Star Point{sp_plural}… <:superstar:1500638307628093510>\n"
            f"And.. __{mushrooms}__ Starry Mushroom{sm_plural}…!! <:hwaaa:1503319595187175465>\n"
            f"Fuhihi… <:Mochi_Syoko:1502793883573162116>"
        )
        return

    # -----------------------
    # HI
    # -----------------------
    if content_lower in ("hi", "hello", "hey"):
        if not can_reply():
            return
        await message.channel.send(random.choice(HI_REPLIES))
        return

    # -----------------------
    # HYAHAAA / METAL MODE
    # -----------------------
    if re.search(r"hy+a+h+a+[ha!]*", content_lower):
        set_mood("excited")
        await client.change_presence(activity=get_presence())
        await message.channel.send(random.choice(METAL_REPLIES))
        return

    # -----------------------
    # HUG + MEMORY
    # -----------------------
    if HUG_PATTERN.search(message.content):
        if not can_reply():
            return

        memory["hugs"].setdefault(user_id, 0)
        memory["hugs"][user_id] += 1
        user_hugs = memory["hugs"][user_id]
        save_memory()

        # Lots of hugs nudge mood toward happy
        if user_hugs % 5 == 0 and mood not in ("excited",):
            mood = "happy"
            await client.change_presence(activity=get_presence())

        if mood == "shy":
            msg = "F-fuhihi… a hug…? <:emoji_20:1500638307628093510> …"
        elif mood == "happy":
            msg = "Fuhihi.. hug! ✨ this feels warm… like a matsutake mushroom...<:fuhihi:1506419016518992086>"
        elif mood == "sleepy":
            msg = f"…mm… soft hug… fuhihi… <:sleeping:1492681477417078865>"
        elif mood == "excited":
            msg = "HYAHAAA hug energy!! ✨ <:hyaha:1492681248257085491>"
        else:
            msg = "Fuhihi… hug received… 🍄‍🟫"

        if user_hugs > 1:
            msg += " " + random.choice(HUG_MEMORY_LINES)

        await message.channel.send(msg)
        return

    # -----------------------
    # SYOKO PIE
    # -----------------------
    if re.search(r"syoko\s*pie", content_lower):
        set_mood("shy")
        await client.change_presence(activity=get_presence())
        if user_id == WIX_USER_ID:
            await message.channel.send(random.choice(WIX_PIE_MENTION_REPLIES))
        elif random.random() < 0.05:
            await message.channel.send(SYOKO_PIE_RARE)
        else:
            await message.channel.send(random.choice(SYOKO_PIE_NORMAL))
        return

    # -----------------------
    # THANK YOU
    # -----------------------
    if "thank you" in content_lower or "thanks" in content_lower:
        if not can_reply():
            return
        reply = random.choice(THANK_REPLIES).format(
            mention=f"<@{user_id}>"
        )
        await message.reply(reply)
        memory["starry_mushrooms"][user_id] = memory["starry_mushrooms"].get(user_id, 0) + 1
        save_memory()
        return

    # -----------------------
    # WELCOME (unchanged, no cooldown)
    # -----------------------
    if "welcome" in content_lower:
        reply = random.choice(WELCOME_REPLIES).format(
            mention=f"<@{user_id}>"
        )
        await message.reply(reply)
        # Silently award a star point
        memory["star_points"][user_id] = memory["star_points"].get(user_id, 0) + 1
        save_memory()
        return

    # -----------------------
    # OCCASIONAL CHAT
    # -----------------------
    if random.random() < OCCASIONAL_CHANCE:
        if not can_reply():
            return
        reply = apply_mood_to_reply(random.choice(OCCASIONAL_REPLIES))
        await message.channel.send(reply)
        return

    # -----------------------
    # TINY IDLE LINES (very rare)
    # -----------------------
    if random.random() < IDLE_CHANCE:
        await message.channel.send(random.choice(IDLE_LINES))


client.run(TOKEN)
