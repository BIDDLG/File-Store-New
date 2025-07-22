from motor.motor_asyncio import AsyncIOMotorClient
from bot.config import Config

client = AsyncIOMotorClient(Config.MONGODB_URI)
db = client["file_share_bot"]
collection = db["files"]

async def save_file(file_id: str, message_id: int, chat_id: int, bot_username: str):
    await collection.update_one(
        {"file_id": file_id},
        {"$set": {
            "file_id": file_id,
            "message_id": message_id,
            "chat_id": chat_id,
            "bot_username": bot_username
        }},
        upsert=True
    )

async def get_file_by_id(file_id: str):
    return await collection.find_one({"file_id": file_id})
