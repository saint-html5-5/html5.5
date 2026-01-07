#!/usr/bin/env python3
from telethon import TelegramClient
from telethon.tl.types import MessageMediaDocument
import random, os

# --- Credentials ---
api_id = 27030051
api_hash = '3ca35e8e44b13eac9bf10e9091796f9a'
phone = '+212656652174'
channel = "@tforgithub"

client = TelegramClient('session_random_lime', api_id, api_hash)

async def main():
    print("🔗 Connecting...")
    await client.start(phone=phone)

    print("🔍 Scanning channel for Lime_Breach_ CSV files...")
    messages = await client.get_messages(channel, limit=1000)

    lime_files = []

    for msg in messages:
        if msg.media and isinstance(msg.media, MessageMediaDocument):
            name = msg.file.name if msg.file else ""
            if name.startswith("Lime_Breach_") and name.lower().endswith(".csv"):
                lime_files.append(msg)

    if not lime_files:
        print("❌ No Lime_Breach_ CSV files found.")
        return

    chosen = random.choice(lime_files)
    filename = chosen.file.name

    # If already downloaded, force new random choice
    while os.path.exists(filename):
        chosen = random.choice(lime_files)
        filename = chosen.file.name

    print(f"🎯 Randomly selected: {filename}")
    print("⬇ Downloading...")

    await client.download_media(chosen, file=filename)

    print(f"✅ Downloaded: {filename}")

with client:
    client.loop.run_until_complete(main())
