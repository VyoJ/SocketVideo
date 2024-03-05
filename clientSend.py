import socket
import cv2
import pickle
import struct
import imutils

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '172.20.10.4'
port = 9995

client_socket.connect((host_ip, port))
data = b""
payload_size = struct.calcsize("Q")

vid = cv2.VideoCapture(0)
while True:
    ret, frame = vid.read()
    if not ret:
        break
    frame = imutils.resize(frame, width=320)
    a = pickle.dumps(frame)
    message = struct.pack("Q", len(a)) + a
    client_socket.sendall(message)

    cv2.imshow('Sending...', frame)
    key = cv2.waitKey(10) & 0xFF
    if key == 13:
        break
vid.release()
cv2.destroyAllWindows()
client_socket.close()