import os
import random
import discord
from discord import app_commands
from googleapiclient.discovery import build

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def get_random_video():
    random_letter = random.choice("abcdefghijklmnopqrstuvwxyz")

    request = youtube.search().list(
        part="snippet",
        q=random_letter,
        type="video",
        maxResults=50
    )

    response = request.execute()
    items = response.get("items", [])

    if not items:
        return None

    video = random.choice(items)
    video_id = video["id"]["videoId"]

    return f"https://www.youtube.com/watch?v={video_id}"


@tree.command(name="randomvideo", description="Stuurt een random YouTube video")
async def randomvideo(interaction: discord.Interaction):
    await interaction.response.defer()

    video_url = get_random_video()

    if video_url:
        await interaction.followup.send(video_url)
    else:
        await interaction.followup.send("No video found hahaha L for you skill issue LMFAO")


@client.event
async def on_ready():
    await tree.sync()
    print(f"Ingelogd als {client.user}")


if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
