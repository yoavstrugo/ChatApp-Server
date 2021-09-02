import socket
from abc import ABC
from datetime import datetime

from server import Server

HOST = '0.0.0.0'
PORT = 5555


class ChatServer(Server, ABC):
    def __init__(self):
        super().__init__()

    def _Server__msg_handler(self, client: socket, data: any) -> None:
        method = data['method']
        if method == 'msg':
            content = data['content']
            author = data['author']
            time = data['time']

            print(f'{time} | {author}:  {content}')

            packet = '{' + \
                     f'\"method\":\"msg\",' + \
                     f'\"author\":\"{author}\",' + \
                     f'\"content\":\"{content}\",' \
                     f'\"time\":\"{time}\"' \
                     '}'
            self.broadcast(packet, [client])


def main():
    chat_server = ChatServer()
    chat_server.open(HOST, PORT)


if __name__ == '__main__':
    main()
