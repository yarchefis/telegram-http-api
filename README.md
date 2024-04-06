## Использование:
```ip:port/api/chats``` список всех чатов    
```ip:port/api/chat/<id>``` последние 10 сообщений чата(число изменяется в config.py)    
```ip:port/api/chat/<id>/msg?text=ваш текст``` отправка сообщений в чат    


## Инструкция для установки сервера на linux:    

#### Установка python на debian/Ubuntu:    
Обновите систему ```sudo apt update```
Установите питон    
```sudo apt install python3 python3-pip```

#### Установка python на Arch/Manjaro:    
Обновите систему ```sudo pacman -Sy```
Установите питон    
```sudo pacman -S python python-pip```
    
#### Установка библиотек:    
```pip install telethon --break-system-packages```
    
## Инструкция для установки сервера на android(termux):

- Если термукс установлен из плей маркета смело его удаляйте и установите к примеру из f-droid https://f-droid.org/ru/packages/com.termux/

- Смените репозиторий если при выполнении команд ниже возникают ошибки
termux-change-repo
и выберите другой к примеру cloudflare

#### Установка python:
Обновите термукс ```pkg update```
Установите питон ```apt install python3 python-pip```

#### Установка библиотек:
```pip install telethon --break-system-packages```


  
## Настройка:    
- Перейдите на страницу https://my.telegram.org/apps и создайте приложение.    
- Клонируйте репозиторий(необходимо установить пакет git)
```git clone https://github.com/yarchefis/telegram-http-api```   
- откройте config.py(предварительно войдя в cклонированную папку cd telegram-http-api)
```nano config.py```    
- На странице создания приложения вы получили api_id и api_hash   
- вставьте их в переменные в файле между кавычками
пример    
```
api_id = '12345678'
api_hash = 'g56ogrp6gro65656565gfghy'
max_msg = 10 
```
- Запустите сервер командой ```python3 main.py```
- Вы получите id адрес и порт
- перейдите на страницу ipадрес:порт/api/chats, страница будет долго грузится.
тем временем в консоли вас попросят ввести номер телефона затем код(его пришлет официальный бот телеграма) и облачный пароль если он есть(пароль при печати отображатся не будет)
после успешного входа у вас должна загрузится страница со списком ваших контактов.
