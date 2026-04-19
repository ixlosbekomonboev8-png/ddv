#!/bin/bash

# Ranglar
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}1. Tizimni yangilash...${NC}"
sudo apt update && sudo apt upgrade -y

echo -e "${GREEN}2. Zarur vositalarni o'rnatish (Python, FFmpeg)...${NC}"
sudo apt install python3 python3-pip python3-venv ffmpeg -y

echo -e "${GREEN}3. Virtual environment yaratish va kutubxonalarni o'rnatish...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo -e "${GREEN}4. Downloads papkasini yaratish...${NC}"
mkdir -p downloads

echo -e "${GREEN}5. Systemd servisini sozlash...${NC}"
# Fayl yo'llarini to'g'irlash
WORKING_DIR=$(pwd)
sed -i "s|WorkingDirectory=.*|WorkingDirectory=$WORKING_DIR|g" bot.service
sed -i "s|ExecStart=.*|ExecStart=$WORKING_DIR/venv/bin/python bot.py|g" bot.service

sudo cp bot.service /etc/systemd/system/bot.service
sudo systemctl daemon-reload
sudo systemctl enable bot
sudo systemctl start bot

echo -e "${GREEN}Tayyor! Bot hozir ishga tushdi.${NC}"
echo -e "Bot holatini tekshirish uchun: ${GREEN}sudo systemctl status bot${NC}"
echo -e "Loglarni ko'rish uchun: ${GREEN}journalctl -u bot -f${NC}"
