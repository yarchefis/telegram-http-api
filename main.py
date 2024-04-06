from http.server import BaseHTTPRequestHandler, HTTPServer
from socket import gethostbyname, gethostname
from telethon.sync import TelegramClient
from telethon.tl.types import User, Channel
import json
import config
import urllib.parse

api_id = config.api_id
api_hash = config.api_hash
max_msg = config.max_msg
class RequestHandler(BaseHTTPRequestHandler):
    @staticmethod
    def get_user_id(api_id, api_hash):
        with TelegramClient('session_name', api_id, api_hash) as client:
            me = client.get_me()
            return me.id

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path_components = parsed_path.path.split('/')

        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'All OK')

        elif path_components[1] == 'api' and path_components[2] == 'chat' and len(path_components) == 5 and path_components[4] == 'msg':
            # New route /api/chat/<id>/msg?text=<тут_текст>
            chat_id = path_components[3]
            query_components = urllib.parse.parse_qs(parsed_path.query)
            if 'text' in query_components:
                message_text = query_components['text'][0]

                with TelegramClient('session_name', api_id, api_hash) as client:
                    client.send_message(int(chat_id), message_text)

                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Message sent successfully')

            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Missing text parameter in query')

        elif self.path == '/api/chats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with TelegramClient('session_name', api_id, api_hash) as client:
                dialogs = client.get_dialogs()
                chats = []
                for dialog in dialogs:
                    entity = dialog.entity
                    if isinstance(entity, User) or isinstance(entity, Channel):
                        title = None
                        if isinstance(entity, User):
                            title = entity.first_name
                            if entity.last_name:
                                title += ' ' + entity.last_name
                        elif isinstance(entity, Channel):
                            title = entity.title
                        chat = {
                            'id': entity.id,
                            'title': title,
                            'username': entity.username if entity.username else None
                        }
                        chats.append(chat)
                self.wfile.write(json.dumps(chats, ensure_ascii=False, indent=4).encode('utf-8'))

        elif self.path.startswith('/api/chat/'):
            components = self.path.split('/')
            chat_id = components[-1]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with TelegramClient('session_name', api_id, api_hash) as client:
                messages = client.get_messages(int(chat_id), limit=max_msg)
                messages_list = []
                for message in messages:
                    sender_name = None
                    if message.sender:
                        if isinstance(message.sender, User):
                            sender_name = message.sender.first_name
                            if not sender_name:
                                sender_name = message.sender.username
                        elif isinstance(message.sender, Channel):
                            sender_name = message.sender.title  # Для каналов используем атрибут title
                    you = True if message.sender_id == self.user_id else False
                    message_data = {
                        'id': message.id,
                        'text': message.text,
                        'sender_id': message.sender_id,
                        'sender_name': sender_name,
                        'date': message.date.timestamp(),
                        'you': you
                    }
                    if message.media is not None:
                        if hasattr(message.media, 'photo'):
                            message_data['text'] += "\n(ФОТО)"
                        elif hasattr(message.media, 'document'):
                            if message.media.document.mime_type.startswith('audio'):
                                message_data['text'] += "\n(ГОЛОСОВОЕ СООБЩЕНИЕ)"
                            elif message.media.document.mime_type.startswith('video'):
                                message_data['text'] += "\n(ВИДЕО)"
                            elif message.media.document.mime_type.startswith('image'):
                                message_data['text'] += "\n(ИЗОБРАЖЕНИЕ или СТИКЕР)"
                            elif message.media.document.mime_type.startswith('application') or message.media.document.mime_type.startswith('text'):
                                message_data['text'] += "\n(ФАЙЛ)"
                        elif hasattr(message.media, 'sticker'):
                            message_data['text'] += "\n(СТИКЕР)"
                    messages_list.append(message_data)
                self.wfile.write(json.dumps(messages_list, ensure_ascii=False, indent=4).encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    host_name = gethostbyname(gethostname())
    server_address = (host_name, port)
    print(f'Starting server on {host_name}:{port}...')
    
    # Получение user_id
    user_id = RequestHandler.get_user_id(api_id, api_hash)
    print(f"Your user_id: {user_id}")

    # Передача user_id в обработчик запросов
    RequestHandler.user_id = user_id
    
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
