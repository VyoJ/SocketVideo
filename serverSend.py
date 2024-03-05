import socket
import cv2
import pickle
import struct
import threading
import ssl

def handle_client(client_socket):
    print("GOT CONNECTION FROM:", client_socket.getpeername())
    try:
        vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        width=1280
        height=720
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
        vid.set(cv2.CAP_PROP_FPS, 60)
        while vid.isOpened():
            img, frame = vid.read()
            if img:
                data = pickle.dumps(frame)
                message = struct.pack("Q", len(data)) + data
                client_socket.sendall(message)
            else:
                break
    finally:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '192.168.1.118'
    print('HOST IP:', host_ip)
    port = 9995
    socket_address = (host_ip, port)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('ssl/certificate.crt', 'ssl/privateKey.key')
    server_socket = context.wrap_socket(server, server_side=True)

    server_socket.bind(socket_address)
    server_socket.listen(5)
    print("LISTENING AT:", socket_address)

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    main()