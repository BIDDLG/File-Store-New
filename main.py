import uvicorn
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os

from bot.handlers import app as telegram_app
from bot.utils import get_file_by_id

load_dotenv()

PORT = int(os.getenv("PORT", 8080))

app = FastAPI()
app.mount("/telegram", telegram_app)

@app.get("/f/{file_id}")
async def redirect_to_telegram(file_id: str):
    file = await get_file_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return {
        "ok": True,
        "redirect": f"https://t.me/{file['bot_username']}?start={file_id}"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
