
from telethon import TelegramClient, events
import re
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables (for Render deployment)
load_dotenv()

# Telegram API credentials from environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# Source and destination group IDs
source_group_ids = [
    -1002594375860, -1002381073397, -1002233048756, -1002376277107, -1001949379900
]
destination_group_id = -1002237262741

# Signal header to be added before each message
signal_header = '''TIME ZONE UTC +6:00
TIME : 1 MINUTE
1 STEP MTG MAX
BROKER: QUOTEX

"USE SAFETY MARGIN FOR BETTER ACCURACY"\n'''

# Regular expression pattern to match trading signals
signal_pattern = re.compile(
    r'([A-Z]{3,6})\s*[-=]*\s*OTC\s*=\s*(\d{2}:\d{2})\s*=\s*(CALL|PUT)', re.IGNORECASE
)

# Initialize the client
client = TelegramClient("signal_bot_session", api_id, api_hash)

@client.on(events.NewMessage(chats=source_group_ids))
async def handler(event):
    message = event.message.message
    if signal_pattern.search(message):
        matched_lines = signal_pattern.findall(message)
        formatted_signals = "\n".join(
            f"{pair} OTC = {time} = {direction.upper()}"
            for pair, time, direction in matched_lines
        )
        final_message = f"{signal_header}\n{formatted_signals}"
        await client.send_message(destination_group_id, final_message)
        print("✅ Signal forwarded successfully.")

async def main():
    await client.start()
    print("🚀 Bot is running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
