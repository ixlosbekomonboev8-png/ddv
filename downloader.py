import yt_dlp
import os
import uuid
from config import DOWNLOAD_PATH

async def download_media(url: str, type: str = "video"):
    """
    url: Havola (YouTube yoki Instagram)
    type: 'video' yoki 'audio'
    """
    random_name = str(uuid.uuid4())
    
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_PATH}/{random_name}.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }

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
