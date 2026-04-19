# Python imijidan foydalanamiz
FROM python:3.10-slim

# Ishchi katalogni belgilaymiz
WORKDIR /app

# Tizimga ffmpeg, nodejs va boshqa kerakli vositalarni o'rnatamiz
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Kerakli kutubxonalar ro'yxatini nusxalaymiz va o'rnatamiz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bot kodlarini nusxalaymiz
COPY . .

# Yuklangan fayllar uchun papka yaratamiz
RUN mkdir -p downloads && chmod 777 downloads

# Botni ishga tushiramiz
CMD ["python", "bot.py"]
