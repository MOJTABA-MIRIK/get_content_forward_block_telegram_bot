# GOD WIN
#my telegram id = @LOVESUNS
#email = javadevelopermobile@gmail.com

import os
import asyncio
import logging
from pyrogram import Client, filters
import re

# Log settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API credentials
API_ID = int(os.getenv("API_ID", "94575"))
API_HASH = os.getenv("API_HASH", "a3406de8d171bb422bb6ddf3bbd800e2")
BOT_TOKEN = os.getenv("BOT_TOKEN", "YourBotToken")

# Create client
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def is_valid_link(text):
    """Validate link"""
    if not text:
        return False, None, None
        
    # Check private channel/group
    private_match = re.search(r'https://t\.me/c/(\d+)/(\d+)', text)
    if private_match:
        chat_id = int(f"-100{private_match.group(1)}")
        message_id = int(private_match.group(2))
        return True, chat_id, message_id
    
    # Check public channel/group
    public_patterns = [
        r'https://t\.me/([a-zA-Z0-9_]+)/(\d+)',
        r'@([a-zA-Z0-9_]+)/(\d+)',
        r'([a-zA-Z0-9_]+)/(\d+)'
    ]
    
    for pattern in public_patterns:
        match = re.search(pattern, text)
        if match:
            return True, match.group(1), int(match.group(2))
    
    return False, None, None

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    """Start command"""
    await message.reply_text("""🤖 Channel Message Forwarding Bot

Hello,
If a channel has a public link (a username like @username) but has disabled forwarding, you can still retrieve a post by providing its link!

Example link:
https://t.me/username/1234

Note: This is only possible for channels with a public username.""")

@app.on_message(filters.text & ~filters.command("start"))
async def handle_text(client, message):
    """Process text"""
    is_valid, channel, msg_id = is_valid_link(message.text)
    
    if not is_valid:
        await message.reply_text("Please send a valid link")
        return
    
    try:
        # Fetch message
        msg = await client.get_messages(channel, msg_id)
        if not msg:
            await message.reply_text("Please send a valid link")
            return
        
        # Forward content
        if msg.text:
            await client.send_message(message.chat.id, msg.text)
        elif msg.photo:
            await client.send_photo(message.chat.id, msg.photo.file_id, caption=msg.caption or "")
        elif msg.video:
            await client.send_video(message.chat.id, msg.video.file_id, caption=msg.caption or "")
        elif msg.document:
            await client.send_document(message.chat.id, msg.document.file_id, caption=msg.caption or "")
        elif msg.audio:
            await client.send_audio(message.chat.id, msg.audio.file_id, caption=msg.caption or "")
        elif msg.voice:
            await client.send_voice(message.chat.id, msg.voice.file_id)
        elif msg.sticker:
            await client.send_sticker(message.chat.id, msg.sticker.file_id)
        elif msg.animation:
            await client.send_animation(message.chat.id, msg.animation.file_id, caption=msg.caption or "")
        elif msg.video_note:
            await client.send_video_note(message.chat.id, msg.video_note.file_id)
        elif msg.location:
            await client.send_location(message.chat.id, msg.location.latitude, msg.location.longitude)
        elif msg.contact:
            await client.send_contact(message.chat.id, msg.contact.phone_number, msg.contact.first_name, msg.contact.last_name or "")
        elif msg.poll:
            options = [opt.text for opt in msg.poll.options]
            await client.send_poll(message.chat.id, msg.poll.question, options)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await message.reply_text("Please send a valid link")

@app.on_message(~filters.text)
async def handle_non_text(client, message):
    """Process non-text content (files, photos, etc.)"""
    await message.reply_text("Please send a valid link")

if __name__ == "__main__":
    print("🚀 Starting bot...")
    app.run()