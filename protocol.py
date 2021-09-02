import json
import socket


def get_msg(conn: socket) -> any:
    buffer = ''
    length = None
    while length is None or len(buffer) < length:
        data = conn.recv(256).decode('utf-8')

        if data is None or data == '':
            raise OSError

        buffer += data

        # When the length of the content is present split it
        if length is None and ';' in buffer:
            length = int(buffer.split(';', 1)[0])
            buffer = buffer.split(';', 1)[1]

        #print(f'{buffer=}')
    return json.loads(buffer)


def send_msg(conn: socket, msg: str) -> None:
    length = str(len(msg))
    data1 = f'{length};{msg}'[:10]
    data2 = f'{length};{msg}'[10:]
    conn.send(data1.encode('utf-8'), )
    conn.send(data2.encode('utf-8'), )

