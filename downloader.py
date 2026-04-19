import yt_dlp
import os
import uuid
import logging
from config import DOWNLOAD_PATH

async def download_media(url: str, type: str = "video"):
    """
    url: Havola (YouTube yoki Instagram)
    type: 'video' yoki 'audio'
    """
    random_name = str(uuid.uuid4())
    
    # Cookies fayli bor yoki yo'qligini tekshiramiz
    cookie_file = 'cookies.txt'
    
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_PATH}/{random_name}.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        # User-Agent'ni insonga o'xshatib qo'yamiz
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    # Agar cookies fayli bo'lsa, uni ishlatamiz
    if os.path.exists(cookie_file):
        logging.info(f"Cookies fayli topildi va ishlatilmoqda: {cookie_file}")
        ydl_opts['cookiefile'] = cookie_file
    else:
        logging.warning("DIQQAT: cookies.txt fayli topilmadi! YouTube bloklashi mumkin.")

    if type == "audio":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Agar audio bo'lsa, extension o'zgaradi (.mp3)
            if type == "audio":
                filename = os.path.splitext(filename)[0] + ".mp3"
                
            return filename
    except Exception as e:
        print(f"Xatolik: {e}")
        return None
