from googletrans import Translator

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import CHANNELS, GROUPS
from keyboards.inline import check_button
from loader import dp, bot
from utils.misc import subscription

translator = Translator()


# state="*" /har qaysi state(holatda) ham ishlaydi
@dp.message_handler(CommandStart(), state="*")
# @dp.message_handler(commands=['start'], state="*")
async def show_channels(msg: types.Message):
    mention = msg.from_user.get_mention()
    user_lang = msg.from_user.language_code
    await bot.send_message(GROUPS[0], text=f"til:{user_lang}\nuser:{mention}\ntype_message: start bosdi")
    fullname = msg.from_user.full_name
    text = f"Qadirli {fullname}, bot dan foydalanish uchun bu kannal(lar)ga obuna bo'ling"
    # await msg.answer(translator.translate(text=text, dest=user_lang).text)
    channels_format = str()
    for channel in CHANNELS:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        # logging.info(invite_link)
        channels_format += f"\n👉 <a href='{invite_link}'>[{chat.title}]</a>\n"

    await msg.answer(f"{translator.translate(text=text, dest=user_lang).text} \n"
                     f"{channels_format}",
                     reply_markup=check_button,
                     disable_web_page_preview=True)

    # bot command larni set qilish (foydalanuvchi tilidagi izohlar bilan)
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", translator.translate("Botni ishga tushurish", dest=user_lang).text),
            types.BotCommand("help", translator.translate("Tushunarsiz malumotlarga izoh beradi", dest=user_lang).text),
            types.BotCommand("community", translator.translate("Taklif va mulohazalar uchum", dest=user_lang).text),
            types.BotCommand("donate", translator.translate("Qo'llab quvvatlovchilar uchun", dest=user_lang).text),
        ]
    )


@dp.callback_query_handler(text="check_subs", state="*")
async def checker(call: types.CallbackQuery):
    await call.answer()
    result = str()
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        user_lang = call.from_user.language_code
        channel = await bot.get_chat(channel)
        if status:
            text = translator.translate(text="bu kanalga obuna bo'lgansiz!", dest=user_lang).text
            invite_link = await channel.export_invite_link()
            result += f"{text}\n✔<a href='{invite_link}'>{channel.title}</a>\n\n"
            await call.message.delete()
        else:
            text = translator.translate(text="bu kanalga obuna bo'lmagansiz. ", dest=user_lang).text
            invite_link = await channel.export_invite_link()
            result += f"{text}\n❌<a href='{invite_link}'>{channel.title}</a> \n\n"
    await call.message.answer(result, disable_web_page_preview=True)


