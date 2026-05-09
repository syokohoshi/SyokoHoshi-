import os
import random
import re
import discord

TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# -----------------------
# MOOD SYSTEM
# -----------------------
mood = "neutral"

def update_mood():
    global mood
    if random.random() < 0.05:
        mood = random.choice(["neutral", "happy", "shy", "sleepy", "excited"])


# -----------------------
# RESPONSES
# -----------------------
HI_REPLIES = [
    "fuhihi… hello… 🍄",
    "fuhihi… oh… hi… 🍄",
    "h-hello… fuhihi… 🍄",
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
    "…thank you… fuhihi…",
    "…let's shine together… ✨",
    "fuhihi… you're all so bright…",
    "…I like it here… 🍄",
]


OCCASIONAL_CHANCE = 0.03


# -----------------------
# READY EVENT
# -----------------------
@client.event
async def on_ready():
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

    content_lower = message.content.lower()

    # update mood slightly over time
    update_mood()

    # -----------------------
    # HI COMMAND
    # -----------------------
    if content_lower.strip() in ("hi", "hello", "h..hi.. fuhihi"):
        await message.channel.send(random.choice(HI_REPLIES))
        return

    # -----------------------
    # HYAHAAA TRIGGER
    # -----------------------
    if re.search(r"hy+a+h+a+[ha!]*", content_lower):
        mood = "excited"
        await message.channel.send("HYAHAAA!! <:hyaha:1492681248257085491>")
        return

    # -----------------------
    # HUG COMMAND
    # -----------------------
    if content_lower.strip() in ("syoko hug", "hug syoko", "give hug"):
        if mood == "shy":
            await message.channel.send("f-fuhihi… a hug…?")
        elif mood == "happy":
            await message.channel.send("fuhihi! hug!! ✨ thank you… this feels warm… 🍄")
        elif mood == "sleepy":
            await message.channel.send("…mm… soft hug… fuhihi… <:sleeping:1492681477417078865>🍄")
        elif mood == "excited":
            await message.channel.send("HYAHAAA hug energy!! ✨ <:hyaha:1492681248257085491>")
        else:
            await message.channel.send("fuhihi… hug received… star point… 🍄")
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
    # OCCASIONAL CHAT (MOOD AFFECTED)
    # -----------------------
    if random.random() < OCCASIONAL_CHANCE:
        reply = random.choice(OCCASIONAL_REPLIES)

        if mood == "shy":
            reply = "…um… " + reply
        elif mood == "sleepy":
            reply = "… " + reply
        elif mood == "happy":
            reply = reply + " ✨"
        elif mood == "excited":
            reply = reply.upper() + "!! <:hyaha:1492681248257085491>"

        await message.channel.send(reply)


client.run(TOKEN)
