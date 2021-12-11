from aiogram import types

from filters import IsGroupFilter
from loader import dp


@dp.message_handler(IsGroupFilter())
async def set_new_photo(msg: types.Message):
    await msg.reply("bot doesn't work in groups")
