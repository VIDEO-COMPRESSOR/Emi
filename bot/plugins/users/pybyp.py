from pyrogram import Client, filters
from pyrogram.types import Message
from bot.config import *
from time import time
from re import search
from bot.modules.regex import is_a_url, URL_REGEX
from bot.modules import bypasser
from bot.logging import LOGGER
from bot.helpers.functions import get_readable_time
from bot.helpers.decorators import user_commands

prefixes = COMMAND_PREFIXES
commands = ["multi", f"multi@{BOT_USERNAME}"]


@Client.on_message(filters.command(commands, **prefixes))
@user_commands
async def multi(_, message: Message):
   """
   Bypass Short Links using PyBypass Library
   """
   msg_args = message.text.split(" ", maxsplit=1)
   reply_to = message.reply_to_message
   if len(msg_args) > 1:
      cmd = msg_args[0]
      url = msg_args[1]
   elif reply_to is not None:
      try:
         reply_text = search(URL_REGEX, reply_to.text)[0]
      except BaseException:
         reply_text = (
            search(URL_REGEX, reply_to.caption_markdown_v2)[0]
            .replace("\\", "")
            .split("*")[0]
         )
      url = reply_text.strip()
      cmd = msg_args[0]
   else:
      return "Bot could not retrieve your URL!"
   valid_url = is_a_url(url)
   if valid_url is not True or url is None:
      return "You did not seem to have entered a valid URL!"
   uname = message.from_user.mention
   uid = f"<code>{message.from_user.id}</code>"
   start = time()
   LOGGER(__name__).info(f" Received : {cmd} - {url}")
   abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>"
   await message.reply_text(text=abc, disable_web_page_preview=True, quote=True)
   res = bypasser.multi_pybyp(url)
   time_taken = get_readable_time(time() - start)
   LOGGER(__name__).info(f" Destination : {cmd} - {res}")
   xyz = f"<b>Bypassed Result :\n</b>{res}\n\n<i>Time Taken : {time_taken}</i>"
   await message.reply_text(text=xyz, disable_web_page_preview=True, quote=True)