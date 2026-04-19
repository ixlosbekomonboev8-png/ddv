from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
from downloader import download_media
from config import ADMIN_USERNAME

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        f"Salom! Men <b>Save Bot</b>man. 📥\n\n"
        f"Menga YouTube yoki Instagram havolasini yuboring, men uni sizga yuklab beraman.\n\n"
        f"Admin: {ADMIN_USERNAME}"
    )
    await message.answer(welcome_text, parse_mode="HTML")

@router.message(F.text.contains("youtube.com") | F.text.contains("youtu.be") | F.text.contains("instagram.com"))
async def handle_link(message: Message):
    url = message.text.strip()
    
    builder = InlineKeyboardBuilder()
    builder.button(text="🎬 Video", callback_data=f"vid_{url}")
    builder.button(text="🎵 Audio (MP3)", callback_data=f"aud_{url}")
    builder.adjust(2)
    
    await message.answer("Nima yuklamoqchisiz?", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("vid_") | F.data.startswith("aud_"))
async def process_download(callback: CallbackQuery):
    data = callback.data
    type = "video" if data.startswith("vid_") else "audio"
    url = data.replace("vid_", "").replace("aud_", "")
    
    await callback.message.edit_text("⏳ Yuklanmoqda... Iltimos, kuting.")
    
    file_path = await download_media(url, type)
    
    if file_path and os.path.exists(file_path):
        try:
            media = FSInputFile(file_path)
            if type == "video":
                await callback.message.answer_video(media, caption=f"Tayyor! ✅\nAdmin: {ADMIN_USERNAME}")
            else:
                await callback.message.answer_audio(media, caption=f"Tayyor! ✅\nAdmin: {ADMIN_USERNAME}")
            
            await callback.message.delete()
        except Exception as e:
            await callback.message.edit_text(f"❌ Xatolik yuz berdi: {str(e)}")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
    else:
        await callback.message.edit_text("❌ Media yuklab bo'lmadi. Havola noto'g'ri bo'lishi mumkin.")
