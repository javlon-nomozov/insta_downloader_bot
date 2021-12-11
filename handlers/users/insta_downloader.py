import logging

from googletrans import Translator
import requests
import re

from aiogram import types

from loader import dp

translator = Translator()


@dp.message_handler()
async def insta_download(msg: types.Message):
    async def get_response(url):
        r = requests.get(url)
        while r.status_code != 200:
            r = requests.get(url)
        return r.text

    async def prepare_urls(matches):
        return list({match.replace("\\u0026", "&") for match in matches})

    url = msg.text
    response = await get_response(url)

    vid_matches = re.findall('"video_url":"([^"]+)"', response)
    vid_matches = re.findall('"video_url":"([^"]+)"', response)
    pic_matches = re.findall('"display_url":"([^"]+)"', response)

    vid_url = await prepare_urls(vid_matches)
    pic_url = await prepare_urls(pic_matches)
    videos = list()
    pictures = list()
    if vid_url:
        videos = ("/ ".join(vid_url)).split()

    if pic_url:
        pictures = ("/ ".join(pic_url)).split()

    if not (pic_url or vid_url):
        await msg.reply("Could not recognize the media in the provided URL.")

    album = types.MediaGroup()
    if pictures:
        for media in pictures:
            album.attach_photo(photo=media, caption="@fo4r_X_4our")
    if videos:
        for media in videos:
            album.attach_video(video=media)
    # album.attach_photo(caption="Downloaded by: <a href='t.me/zeepy_bot'>@zeepy_bot</a>")
    logging.info(album)
    # album["caption"] = "<a href='t.me/zeepy_bot>Fo4u X 4our</a>"
    await msg.reply_media_group(album)
