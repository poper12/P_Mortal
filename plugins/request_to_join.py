from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest
from bot import Bot
from config import REQUEST_CHANNEL_1, REQUEST_CHANNEL_2
from database.database import add_req_one, add_req_two

@Bot.on_chat_join_request(
    filters.chat(REQUEST_CHANNEL_1) | filters.chat(REQUEST_CHANNEL_2)
)
async def join_reqs(client, join_req: ChatJoinRequest):
    user_id = join_req.from_user.id
    if join_req.chat.id == REQUEST_CHANNEL_1:
        try:
            await add_req_one(user_id)
        except Exception as e:
            print(f"Error adding join request to req_one: {e}")
    elif join_req.chat.id == REQUEST_CHANNEL_2:
        try:
            await add_req_two(user_id)
        except Exception as e:
            print(f"Error adding join request to req_two: {e}")
