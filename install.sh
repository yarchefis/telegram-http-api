#!/bin/bash

# Обновление термукс
pkg update

# Установка Python и pip
apt install python3 python-pip

# Установка git
apt install git

# Установка библиотеки telethon
pip install telethon --break-system-packages

# Клонирование репозитория
git clone https://github.com/yarchefis/telegram-http-api
cd telegram-http-api

# Создание файла config.py
echo "Введите api_id:"
read api_id
echo "Введите api_hash:"
read api_hash
echo "max_msg = 10" > config.py
echo "api_id = '$api_id'" >> config.py
echo "api_hash = '$api_hash'" >> config.py

# Создание файла start.sh
echo "#!/bin/bash" > start.sh
echo "python3 main.py" >> start.sh
chmod +x start.sh

echo "Установка завершена. Теперь запустите start.sh для запуска сервера."
