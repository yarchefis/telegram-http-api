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

# Запрос и вставка api_id и api_hash в файл config.py
echo "Введите api_id:"
read api_id
echo "Введите api_hash:"
read api_hash

# Вставка значений в файл config.py
sed -i "s/api_id = ''/api_id = '$api_id'/" config.py
sed -i "s/api_hash = ''/api_hash = '$api_hash'/" config.py

cd

# Создание файла start.sh
echo "#!/bin/bash" > start.sh
echo "python3 main.py" >> start.sh
chmod +x start.sh

echo "Установка завершена. Теперь запустите start.sh для запуска сервера."
