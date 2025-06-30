#(©)@EdgeBots

from pyrogram import __version__

import config
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"""<b>╭───────────⍟
├➽ Dᴇᴠᴇʟᴏᴩᴇʀ : <a href='tg://user?id={5543390445}'>Aaru</a>
├➽ Lɪʙʀᴀʀy : <a href=https://github.com/pyrogram>Pʏʀᴏɢʀᴀᴍ</a>
├➽ Lᴀɴɢᴜᴀɢᴇ : <a href=https://www.python.org>Pʏᴛʜᴏɴ 3</a>
├➽ ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ : <a href=https://t.me/Anime_Harvest>Anime Harvest</a>
├➽ ᴍᴀɴɢᴀ ᴄʜᴀɴɴᴇʟ : <a href=https://t.me/Manga_Campus>Manga Campus</a>
├➽ ᴄʜᴀᴛ ɢᴄ : <a href=https://t.me/Manga_Campus_Chat>Chat GC</a></b>
╰───────────────⍟ """,
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("𝙲𝚕𝚘𝚜𝚎", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
