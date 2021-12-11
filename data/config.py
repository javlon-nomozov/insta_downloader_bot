# from environs import Env
#
# # environs kutubxonasidan foydalanish
# env = Env()
# env.read_env()
#
# # .env fayl ichidan quyidagilarni o'qiymiz
# BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
# ADMINS = env.list("ADMINS")  # adminlar ro'yxati
# IP = env.str("ip")  # Xosting ip manzili
# CHANNELS = env.list("CHANNELS")
# GROUPS = env.list("GROUPS")
# #
import os
#
#
# # .env fayl ichidan quyidagilarni o'qiymiz
#
BOT_TOKEN = str(os.environ.get("BOT_TOKEN"))
# ADMINS = list(os.environ.get("ADMINS"))
# # IP = str(os.environ.get("ip"))
# CHANNELS = list(os.environ.get("CHANNELS"))
# GROUPS = ["@gdfnjdu"]


GROUPS = ["@gdfnjdu"]
CHANNELS = ['-1001678147207']
ADMINS = ['1559808421']
