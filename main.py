from http.server import BaseHTTPRequestHandler, HTTPServer
from telethon.sync import TelegramClient
import json
import config

api_id = config.api_id
api_hash = config.api_hash

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/chats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            with TelegramClient('session_name', api_id, api_hash) as client:
                dialogs = client.get_dialogs()

                chats = []
                for dialog in dialogs:
                    if dialog.is_user and not dialog.entity.bot:
                        entity = dialog.entity
                        chat = {
                            'id': entity.id,
                            'title': entity.first_name if entity.first_name else entity.title,
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
                messages = client.get_messages(int(chat_id), limit=10)

                messages_list = []
                for message in messages:
                    sender_name = None
                    if message.sender:
                        sender_name = message.sender.first_name
                        if not sender_name:
                            sender_name = message.sender.username
                    message_data = {
                        'id': message.id,
                        'text': message.text,
                        'sender_id': message.sender_id,
                        'sender_name': sender_name,
                        'date': message.date.timestamp()
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
                            elif message.media.document.mime_type.startswith('application'):
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
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
