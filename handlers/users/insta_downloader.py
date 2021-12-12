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
        logging.info(f"r = {r}")
        logging.info(f"r = {r.status_code}")
        while r.status_code != 200:
            r = requests.get(url)
        return r.text

    async def prepare_urls(matches):
        logging.info(f"matches = {matches}")
        foo = {}
        for match in matches:
            match.replace("\\u0026", "&")

            foo = {match}
        return list(foo)

    url = msg.text
    logging.info(f"url: {url}")
    try:
        response = await get_response(url)
    except:
        logging.info(f"response None")

    vid_url = ''
    pic_url = ''

    try:
        vid_matches = re.findall('"video_url":"([^"]+)"', response)
        pic_matches = re.findall('"display_url":"([^"]+)"', response)

        vid_url = await prepare_urls(vid_matches)
        logging.info(f"pic_url = {prepare_urls(vid_matches)}")
        pic_url = await prepare_urls(pic_matches)
        logging.info(f"pic_url = {prepare_urls(pic_matches)}")
    except:
        logging.info(f"vid_url: {vid_url}\npic_url {pic_url}")
    videos = list()
    pictures = list()
    if vid_url:
        videos = ("/ ".join(vid_url)).split()
        logging.info(f"videos {videos}")

    if pic_url:
        pictures = ("/ ".join(pic_url)).split()
        logging.info(f"pictures {pictures}")

    album = types.MediaGroup()
    if pictures:
        for media in pictures:
            album.attach_photo(photo=media)
            # album.attach_photo(photo=media, caption="@four_X_four_bot")
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
