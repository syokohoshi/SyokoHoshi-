import os
import random
import re
import discord

TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# -----------------------
# MOOD SYSTEM + AFFECTION
# -----------------------
mood = "neutral"
hug_count = 0

MOOD_POOL = ["neutral", "happy", "shy", "sleepy", "excited"]

def update_mood():
    global mood
    if random.random() < 0.05:
        mood = random.choice(MOOD_POOL)

def update_status():
    """Rotating presence based on mood"""
    try:
        if mood == "happy":
            activity = discord.Game(name="fuhihi… happy 🍄")
        elif mood == "shy":
            activity = discord.Game(name="…watching quietly")
        elif mood == "sleepy":
            activity = discord.Game(name="…sleepy mushrooms…")
        elif mood == "excited":
            activity = discord.Game(name="HYAHAAA energy!!")
        else:
            activity = discord.Game(name="fuhihi… 🍄")

        return activity
    except:
        return discord.Game(name="fuhihi… 🍄")


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
    global mood, hug_count

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
        await message.channel.send(random.choice(HI_REPLIES))
        return

    # -----------------------
    # HYAHAAA
    # -----------------------
    if re.search(r"hy+a+h+a+[ha!]*", content_lower):
        mood = "excited"
        await message.channel.send("HYAHAAA!! <:hyaha:1492681248257085491>")
        return

    # -----------------------
    # HUG (ANY SENTENCE VERSION)
    # -----------------------
    if "hug" in content_lower and "syoko" in content_lower:
        hug_count += 1

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

        # affection bonus line
        if hug_count % 5 == 0:
            msg += " …you’ve hugged me a lot… fuhihi…"

        await message.channel.send(msg)
        return

    # -----------------------
    # WELCOME (UNCHANGED)
    # -----------------------
    if "welcome" in content_lower:
        reply = random.choice(WELCOME_REPLIES).format(
            mention=f"<@{message.author.id}>"
        )
        await message.reply(reply)
        return

    # -----------------------
    # OCCASIONAL CHAT
    # -----------------------
    if random.random() < OCCASIONAL_CHANCE:
        reply = random.choice(OCCASIONAL_REPLIES)

        if mood == "shy":
            reply = "…um… " + reply
        elif mood == "sleepy":
            reply = "… " + reply
        elif mood == "happy":
            reply += " ✨"
        elif mood == "excited":
            reply = reply.upper() + "!! <:hyaha:1492681248257085491>"

        await message.channel.send(reply)


client.run(TOKEN)
