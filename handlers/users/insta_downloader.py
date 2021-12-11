import logging

from googletrans import Translator
import requests
import re

from aiogram import types

from loader import dp
from filters import IsPrivateFilter

translator = Translator()


@dp.message_handler(IsPrivateFilter())
async def insta_download(msg: types.Message):
    async def get_response(url):
        r = requests.get(url)
        while r.status_code != 200:
            r = requests.get(url)
        return r.text

    async def prepare_urls(matches):
        return list({match.replace("\\u0026", "&") for match in matches})

    url = msg.text
    try:
        response = await get_response(url)
    except:
        pass

    vid_url = ''
    pic_url = ''

    try:
        vid_matches = re.findall('"video_url":"([^"]+)"', response)
        pic_matches = re.findall('"display_url":"([^"]+)"', response)

        vid_url = await prepare_urls(vid_matches)
        pic_url = await prepare_urls(pic_matches)
    except:
        pass
    videos = list()
    pictures = list()
    if vid_url:
        videos = ("/ ".join(vid_url)).split()

    if pic_url:
        pictures = ("/ ".join(pic_url)).split()

    album = types.MediaGroup()
    if pictures:
        for media in pictures:
            album.attach_photo(photo=media, caption="@four_X_four_bot")
    if videos:
        for media in videos:
            album.attach_video(video=media)
    # album.attach_photo(caption="Downloaded by: <a href='t.me/zeepy_bot'>@zeepy_bot</a>")
    logging.info(album)
    # album["caption"] = "<a href='t.me/zeepy_bot>Fo4u X 4our</a>"
    # await msg.reply_media_group(album)
    try:
        await msg.reply_media_group(album)
    except:
        await msg.reply("this link does not work\nMaybe this private users post")
