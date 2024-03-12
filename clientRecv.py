import socket
import cv2
import pickle
import struct
import ssl

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.1.118'
port = 9995

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('domain.crt')
context.check_hostname = False
client_socket = context.wrap_socket(client, server_hostname=host_ip)
client_socket.connect((host_ip, port))

data = b""
payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024)
        if not packet:
            break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("Receiving...", frame)
    key = cv2.waitKey(10)
    if key == 13:
        break

client_socket.close()