import os, asyncio, humanize
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import ADMINS, OWNER_ID, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, FILE_AUTO_DELETE
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user, is_requested_one, is_requested_two, delete_all_one, delete_all_two, is_admin

class A:
    async def __call__(self, c, m):
        u = m.from_user.id
        ok, _ = await is_admin(u)
        if u == OWNER_ID or ok or u in ADMINS:
            return True
        await m.reply("❌ You can't use this.")
        return False

a = A()
mad = FILE_AUTO_DELETE
mad_h = humanize.naturaldelta(mad)

@Bot.on_message(filters.command('start') & filters.private)
async def st(c: Client, m: Message):
    u = m.from_user.id
    if not await present_user(u):
        try:
            await add_user(u)
        except Exception as e:
            print(f"Add user err: {e}")
    sub = await subscribed(c, m)
    adm = u in ADMINS
    if not sub and not adm:
        btn = []
        if getattr(c, 'invitelink', None):
            btn.append([InlineKeyboardButton("Join Channel 1", url=c.invitelink)])
        if getattr(c, 'invitelink2', None):
            btn.append([InlineKeyboardButton("Join Channel 2", url=c.invitelink2)])
        if len(m.command) > 1:
            btn.append([InlineKeyboardButton('🔄 Try Again', url=f"https://t.me/{c.username}?start={m.command[1]}")])
        await m.reply(
            text=FORCE_MSG.format(
                first=m.from_user.first_name,
                last=m.from_user.last_name or '',
                username=None if not m.from_user.username else '@' + m.from_user.username,
                mention=m.from_user.mention,
                id=u
            ),
            reply_markup=InlineKeyboardMarkup(btn),
            quote=True,
            parse_mode=ParseMode.MARKDOWN
        )
        return
    t = m.text
    btn = []
    if len(t) > 7:
        if not adm:
            j1 = await is_requested_one(m)
            j2 = await is_requested_two(m)
            if c.link_one and not j1:
                btn.append([InlineKeyboardButton("📢 Join Channel 1", url=c.link_one)])
            if c.link_two and not j2:
                btn.append([InlineKeyboardButton("📢 Join Channel 2", url=c.link_two)])
            if btn:
                if len(m.command) > 1:
                    btn.append([InlineKeyboardButton('🔄 Try Again', url=f"https://t.me/{c.username}?start={m.command[1]}")])
                await m.reply(
                    text="**Please join the following channels to continue:**",
                    reply_markup=InlineKeyboardMarkup(btn),
                    parse_mode=ParseMode.MARKDOWN
                )
                return
        try:
            b64 = t.split(" ", 1)[1]
            s = await decode(b64)
            arg = s.split("-")
            if len(arg) == 3:
                try:
                    stt = int(int(arg[1]) / abs(c.db_channel.id))
                    end = int(int(arg[2]) / abs(c.db_channel.id))
                    ids = list(range(stt, end + 1)) if stt <= end else list(range(stt, end - 1, -1))
                except:
                    return
            elif len(arg) == 2:
                try:
                    ids = [int(int(arg[1]) / abs(c.db_channel.id))]
                except:
                    return
            else:
                return
            tmp = await m.reply("Please Wait...")
            try:
                msgs = await get_messages(c, ids)
            except:
                await m.reply_text("Something Went Wrong..!")
                return
            await tmp.delete()
            out = []
            for msg in msgs:
                if bool(CUSTOM_CAPTION) and bool(msg.document):
                    cap = CUSTOM_CAPTION.format(
                        previouscaption="" if not msg.caption else msg.caption.html,
                        filename=msg.document.file_name
                    )
                else:
                    cap = "" if not msg.caption else msg.caption.html
                rm = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None
                try:
                    mm = await msg.copy(
                        chat_id=u,
                        caption=cap,
                        parse_mode=ParseMode.HTML,
                        reply_markup=rm,
                        protect_content=PROTECT_CONTENT
                    )
                    out.append(mm)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    mm = await msg.copy(
                        chat_id=u,
                        caption=cap,
                        parse_mode=ParseMode.HTML,
                        reply_markup=rm,
                        protect_content=PROTECT_CONTENT
                    )
                    out.append(mm)
                except Exception as e:
                    print(f"Send err: {e}")
            if FILE_AUTO_DELETE > 0 and out:
                k = await c.send_message(
                    chat_id=u,
                    text=f"<blockquote><b>❗️ <u>𝗜𝗠𝗣𝗢𝗥𝗧𝗔𝗡𝗧</u> ❗️</b></blockquote>\n\n"
                         f"<blockquote><b>Tʜɪs Fɪʟᴇ Wɪʟʟ Bᴇ Dᴇʟᴇᴛᴇᴅ Iɴ {mad_h} minutes (Dᴜᴇ Tᴏ Cᴏᴘʏʀɪɢʜᴛ Issᴜᴇs)</b></blockquote>\n"
                         f"<blockquote><b>📌 Pʟᴇᴀsᴇ Fᴏʀᴡᴀʀᴅ Tʜɪs Fɪʟᴇ Tᴏ Sᴏᴍᴇᴡʜᴇʀᴇ Eʟsᴇ Aɴᴅ Sᴛᴀʀᴛ Dᴏᴡɴʟᴏᴀᴅɪɴɢ Tʜᴇʀᴇ.</b></blockquote>\n\n"
                         f"<blockquote>𝙁𝙤𝙧 🤖 𝘼𝙣𝙞𝙢𝙚 𝘾𝙝𝙚𝙘𝙠𝙤𝙪𝙩: @Anime_Harvest</blockquote>\n"
                         f"<blockquote>𝙁𝙤𝙧 🥵 𝙋𝙤𝙧𝙣 𝙉𝙚𝙩𝙬𝙤𝙧𝙠: @Pleasures_Mortal</blockquote>",
                    parse_mode=ParseMode.HTML
                )
                asyncio.create_task(del_files(out, c, k))
            return
        except Exception as e:
            print(f"File req err: {e}")
    menu = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇧 🇦 🇨 🇰  🇺 🇵", url="https://t.me/+bN2p7tc23uxkZDM1")
        ],
        [
            InlineKeyboardButton("𝗛𝗲𝗻𝘁𝗮𝗶", url="https://t.me/+Tz--UjhSzP9jZDdl"),
            InlineKeyboardButton("𝗝𝗮𝘃", url="https://t.me/+gdgN9LhKn74zMGU9")
        ],
        [
            InlineKeyboardButton("𝗔𝗱𝘂𝗹𝘁𝘀", url="https://t.me/+hvbqfOasZd5iMDZl"),
            InlineKeyboardButton("𝗗𝗲𝘀𝗶", url="https://t.me/+KwoA0-KjknY3ZGU1")
        ],
        [
            InlineKeyboardButton("𝗜𝗻𝘀𝘁𝗮/𝗦𝗻𝗮𝗽 𝗟𝗲𝗮𝗸𝘀", url="https://t.me/+eNy9hIdk71s5Y2E9"),
            InlineKeyboardButton("𝗢𝗻𝗹𝘆𝗳𝗮𝗻𝘀", url="https://t.me/+Z0_maxrY-2kyOTQ1")
        ],
        [
            InlineKeyboardButton("𝗣𝗼𝗿𝗻𝗵𝘄𝗮", url="https://t.me/+Vfxvk2AZ3oc5ZDI1")
        ],
        [
            InlineKeyboardButton("𝗝𝗼𝗶𝗻 𝗮𝗹𝗹 𝗮𝘁 𝗢𝗻𝗰𝗲", url="https://t.me/addlist/q7ouVTPB1xhiZmM1")
        ],
        [  
            InlineKeyboardButton("⛩ About", callback_data="about"),
            InlineKeyboardButton("🔐 Close", callback_data="close")          
        ]
    ])
    await m.reply_text(
        text=START_MSG.format(
            first=m.from_user.first_name,
            last=m.from_user.last_name or '',
            username=None if not m.from_user.username else '@' + m.from_user.username,
            mention=m.from_user.mention,
            id=u
        ),
        reply_markup=menu,
        disable_web_page_preview=True,
        quote=True
    )
    return

@Bot.on_message(filters.command('users') & filters.private & a)
async def users(c: Bot, m: Message):
    msg = await c.send_message(chat_id=m.chat.id, text=f"Processing...")
    us = await full_userbase()
    await msg.edit(f"{len(us)} Users Are Using This Bot")

@Bot.on_message(filters.private & filters.command('broadcast') & a)
async def bc(c: Bot, m: Message):
    if m.reply_to_message:
        q = await full_userbase()
        b = m.reply_to_message
        t = s = bl = d = u = 0
        pls = await m.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for i in q:
            try:
                await b.copy(i)
                s += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await b.copy(i)
                s += 1
            except UserIsBlocked:
                await del_user(i)
                bl += 1
            except InputUserDeactivated:
                await del_user(i)
                d += 1
            except:
                u += 1
                pass
            t += 1
        stat = f"""<b><u>Broadcast Completed</u></b>\n\n<b>Total Users :</b> <code>{t}</code>\n<b>Successful :</b> <code>{s}</code>\n<b>Blocked Users :</b> <code>{bl}</code>\n<b>Deleted Accounts :</b> <code>{d}</code>\n<b>Unsuccessful :</b> <code>{u}</code>"""
        return await pls.edit(stat)
    else:
        msg = await m.reply(f"Use This Command As A Reply To Any Telegram Message With Out Any Spaces.")
        await asyncio.sleep(8)
        await msg.delete()

async def del_files(msgs, c, k):
    await asyncio.sleep(FILE_AUTO_DELETE)
    for msg in msgs:
        try:
            await c.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            print(f"Delete fail {msg.id}: {e}")
    await k.edit_text("<blockquote>𝙁𝙤𝙧 𝙈𝙤𝙧𝙚 𝘼𝙙𝙪𝙡𝙩 𝘾𝙤𝙣𝙩𝙚𝙣𝙩 𝘾𝙝𝙚𝙘𝙠𝙤𝙪𝙩: @Pleasures_Mortal</blockquote>")

@Bot.on_message(filters.command('clear_req_1') & filters.private & a)
async def clr1(b, m):
    r = await m.reply("`processing...`")
    await delete_all_one()
    await r.edit("Request database 01 Cleared ✅" )
    
@Bot.on_message(filters.command('clear_req_2') & filters.private & a)
async def clr2(b, m):
    r = await m.reply("`processing...`")
    await delete_all_two()
    await r.edit("Request database 02 Cleared ✅" )
