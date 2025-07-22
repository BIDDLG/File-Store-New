from pyrogram import Client, filters
from pyrogram.types import Message
from fastapi import FastAPI
from bot.config import Config
from bot.utils import save_file
import asyncio

app = FastAPI()
bot = Client("bot", bot_token=Config.BOT_TOKEN)

@bot.on_message(filters.document | filters.video | filters.audio)
async def handle_file(_, message: Message):
    media = message.document or message.video or message.audio
    file_id = media.file_unique_id
    await save_file(
        file_id=file_id,
        message_id=message.id,
        chat_id=message.chat.id,
        bot_username=(await bot.get_me()).username
    )
    link = f"{Config.WEBSITE_BASE_URL}/f/{file_id}"
    await message.reply_text(f"Here is your shareable link:\n{link}")

@bot.on_message(filters.command("start") & filters.private)
async def start_command(_, message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) == 2:
        file_id = parts[1]
        from bot.utils import get_file_by_id
        file = await get_file_by_id(file_id)
        if file:
            await bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=file["chat_id"],
                message_id=file["message_id"]
            )
            return
        await message.reply("File not found.")
    else:
        await message.reply("Send a file to get a shareable link.")

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(bot.start())

@app.on_event("shutdown")
async def on_shutdown():
    await bot.stop()
