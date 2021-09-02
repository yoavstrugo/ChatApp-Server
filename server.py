import socket
from abc import abstractmethod, ABC
from threading import Thread
from protocol import get_msg, send_msg


class Server(ABC):
    def __init__(self):
        self.__server_socket = None
        self.__clients = []

    @abstractmethod
    def __msg_handler(self, client: socket, data: any) -> None:
        pass

    def open(self, host, port):
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.__server_socket.bind((host, port))

            self.__server_socket.listen()
            print(f'Listening on {host}:{port}')

            # Start accepting clients
            self.__accept_clients()
        except OSError as e:
            print('An error has occurred:')
            print(e)
            input('Press ENTER to restart...')
            self.open(host, port)




    def close(self):
        for client in self.__clients:
            client.send('{method:\'close\'}'.encode('utf-8'))
            client.close()
        self.__server_socket.close()

    def broadcast(self, msg: str, exclude: list[socket] = None):
        for client in self.__clients:
            try:
                if client not in exclude:
                    send_msg(client, msg)
            except OSError:
                self.__clients.remove(client)

    def __handle_client(self, conn):
        while True:
            try:
                msg = get_msg(conn)
            except OSError:
                self.__clients.remove(conn)
                break

            self.__msg_handler(conn, msg)

    def __accept_clients(self):
        if self.__server_socket is not None:
            while True:
                conn, addr = self.__server_socket.accept()
                print(f'{addr[0]}:{addr[1]} has joined the chat.')

                self.__clients.append(conn)

                thread = Thread(target=self.__handle_client, args=(conn,))
                thread.start()
