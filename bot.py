import os
import random
import re
import discord

TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

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
    "…that's a star point… ✨",
    "fuhihi… I was listening…",
    "…um… I agree… 🍄",
    "…thank you… fuhihi…",
    "…let's shine together… ✨",
    "fuhihi… you're all so bright…",
    "…I like it here… 🍄",
]

OCCASIONAL_CHANCE = 0.03


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("Syoko is here… fuhihi… 🍄")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content_lower = message.content.lower()

    if "hi" in content_lower.split() or content_lower in ("hi", "hello", "hey"):
        await message.channel.send(random.choice(HI_REPLIES))
        return

    if re.search(r"hy+a+h+a+[ha!]*", content_lower):
        await message.channel.send("HYAHAAA!! <:hyaha:1492681248257085491>")
        return

    if "welcome" in content_lower:
        reply = random.choice(WELCOME_REPLIES).format(mention=f"<@{message.author.id}>")
        await message.reply(reply)
        return

    if random.random() < OCCASIONAL_CHANCE:
        await message.channel.send(random.choice(OCCASIONAL_REPLIES))


client.run(TOKEN)

