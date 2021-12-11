from aiogram import types

from loader import dp
from filters import IsPrivateFilter


# Echo bot
@dp.message_handler(IsPrivateFilter(), state=None)
async def bot_echo(message: types.Message):
    await message.answer(message.text)
