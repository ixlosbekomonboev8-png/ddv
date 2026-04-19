import os

# Telegram bot tokenini bu yerga yozing yoki serverga BOT_TOKEN deb kiriting
TOKEN = os.getenv("BOT_TOKEN", "8423934246:AAEc7eAuy3Ya2_mYM-P38qWs41OeC18NTbU")

# Admin ma'lumotlari
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "@ixlos_admin")

# Yuklangan fayllarni vaqtinchalik saqlash joyi
DOWNLOAD_PATH = "downloads"

if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)
