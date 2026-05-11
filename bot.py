import os
import random
import re
import time
import discord

TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# -----------------------
# MOOD SYSTEM + MEMORY + COOLDOWN
# -----------------------
mood = "neutral"
hug_count = 0

memory = {
    "hugs": {}
}

MOOD_POOL = ["neutral", "happy", "shy", "sleepy", "excited"]

# 🧠 mood changes every 2 hours
last_mood_change = time.time()

def update_mood():
    global mood, last_mood_change

    if time.time() - last_mood_change > 7200:
        mood = random.choice(MOOD_POOL)
        last_mood_change = time.time()


# 🕒 reply cooldown system
last_reply_time = 0
REPLY_COOLDOWN = 6

def can_reply():
    global last_reply_time

    now = time.time()

    if now - last_reply_time < REPLY_COOLDOWN:
        return False

    last_reply_time = now
    return True


def update_status():
    try:
        if mood == "happy":
            return discord.Game(name="fuhihi… happy 🍄")
        elif mood == "shy":
            return discord.Game(name="…watching quietly...")
        elif mood == "sleepy":
            return discord.Game(name="…sleeping kinoko…")
        elif mood == "excited":
            return discord.Game(name="HYAHAAA energy!!")
        else:
            return discord.Game(name="fuhihi… 🍄")
    except:
        return discord.Game(name="fuhihi…")


# -----------------------
# RESPONSES
# -----------------------
HI_REPLIES = [
    "fuhihi… hello… 🍄",
    "fuhihi… oh… hi… 🍄",
    "h-hello… f-fuhi… 🍄",
    "fuhihi… you noticed me… 🍄",
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
    "…mushrooms are nice… 🍄",
    "…I'm here… fuhihi…",
    "fuhihi… I was listening…",
    "…let's shine together… ✨",
    "…I like it here… 🍄",
]

OCCASIONAL_CHANCE = 0.03


# -----------------------
# READY EVENT
# -----------------------
@client.event
async def on_ready():
    await client.change_presence(activity=update_status())

    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("Syoko is here… fuhihi… 🍄")


# -----------------------
# MESSAGE HANDLER
# -----------------------
@client.event
async def on_message(message):
    global mood, hug_count, memory

    if message.author == client.user:
        return

    content_lower = message.content.lower()

    update_mood()

    # -----------------------
    # STATUS REFRESH
    # -----------------------
    if random.random() < 0.05:
        await client.change_presence(activity=update_status())

    # -----------------------
    # HI
    # -----------------------
    if content_lower.strip() in ("hi", "hello", "hey"):
        if not can_reply():
            return

        await message.channel.send(random.choice(HI_REPLIES))
        return

    # -----------------------
    # HYAHAAA
    # -----------------------
    if re.search(r"hy+a+h+a+[ha!]*", content_lower):
        mood = "excited"

        await message.channel.send(
            "HYAHAAA!! <:hyaha:1492681248257085491>"
        )
        return

    # -----------------------
    # HUG + MEMORY
    # -----------------------
    if "hug" in content_lower and "syoko" in content_lower:
        if not can_reply():
            return

        hug_count += 1

        user_id = str(message.author.id)

        if user_id not in memory["hugs"]:
            memory["hugs"][user_id] = 0

        memory["hugs"][user_id] += 1
        user_hugs = memory["hugs"][user_id]

        # mood reactions
        if mood == "shy":
            msg = "f-fuhihi… a hug…?"
        elif mood == "happy":
            msg = "fuhihi!! hug!! ✨ this feels warm… 🍄"
        elif mood == "sleepy":
            msg = "…mm… soft hug… fuhihi… <:sleeping:1492681477417078865>"
        elif mood == "excited":
            msg = "HYAHAAA hug energy!! ✨ <:hyaha:1492681248257085491>"
        else:
            msg = "fuhihi… hug received… 🍄"

        # global milestone
        if hug_count % 5 == 0:
            msg += " …you’ve hugged me a lot… fuhihi…"

        # personal memory
        if user_hugs == 1:
            msg += " …first hug… I’ll remember it… 🍄"
        elif user_hugs == 10:
            msg += " …10 hugs… that’s warm… 🍄"
        elif user_hugs % 25 == 0:
            msg += " …I remember you… fuhihi…"

        await message.channel.send(msg)
        return

    # -----------------------
    # THANK YOU
    # -----------------------
    if "thank you" in content_lower or "thanks" in content_lower:
        if not can_reply():
            return

        reply = random.choice(THANK_REPLIES).format(
            mention=f"<@{message.author.id}>"
        )

        await message.reply(reply)
        return

    # -----------------------
    # WELCOME
    # -----------------------
    if "welcome" in content_lower:
        if not can_reply():
            return

        reply = random.choice(WELCOME_REPLIES).format(
            mention=f"<@{message.author.id}>"
        )

        await message.reply(reply)
        return

    # -----------------------
    # OCCASIONAL CHAT
    # -----------------------
    if random.random() < OCCASIONAL_CHANCE:
        if not can_reply():
            return

        reply = random.choice(OCCASIONAL_REPLIES)

        if mood == "shy":
            reply = "…um… " + reply
        elif mood == "sleepy":
            reply = "… " + reply
        elif mood == "happy":
            reply += " ✨"
        elif mood == "excited":
            reply = (
                reply.upper()
                + "!! <:hyaha:1492681248257085491>"
            )

        await message.channel.send(reply)


client.run(TOKEN)
