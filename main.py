
import discord
from discord.ext import tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from github_utils import get_today_commit_stats
from gemini_utils import generate_roast
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

USER_ID = 1385320007482871953

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.dm_messages = True

client = discord.Client(intents=intents)

scheduler = AsyncIOScheduler()

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    schedule_daily_roasts()
    scheduler.start()
    await send_dm_roast()  # Trigger immediately for testing

def schedule_daily_roasts():
    times = ["10:00", "13:00", "17:00", "22:00"]
    for t in times:
        hour, minute = map(int, t.split(":"))
        scheduler.add_job(send_dm_roast, "cron", hour=hour, minute=minute)

async def send_dm_roast():
    try:
        user = await client.fetch_user(USER_ID)
        stats = get_today_commit_stats(GITHUB_USERNAME)
        total_lines = stats["added"] - stats["removed"]
        roast = generate_roast(total_lines)
        await user.send(f"**Daily Code Check 🔍**\n{roast}")
        print("✅ Roast sent")
    except Exception as e:
        print(f"❌ Failed to send DM: {e}")

client.run(DISCORD_TOKEN)