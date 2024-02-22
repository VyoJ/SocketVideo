# import socket, cv2, pickle, struct, imutils

# server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# host_name  = socket.gethostname()
# host_ip = "192.168.1.7"
# print('HOST IP:',host_ip)
# port = 9111
# socket_address = (host_ip,port)

# server_socket.bind(socket_address)

# # Socket Listen
# server_socket.listen(5)
# print("LISTENING AT:",socket_address)

# # Socket Accept
# while True:
# 	client_socket,addr = server_socket.accept()
# 	print('GOT CONNECTION FROM:',addr)
# 	if client_socket:
# 		vid = cv2.VideoCapture(0)
		
# 		while(vid.isOpened()):
# 			img,frame = vid.read()
# 			frame = imutils.resize(frame,width=320)
# 			a = pickle.dumps(frame)
# 			message = struct.pack("Q",len(a))+a
# 			client_socket.sendall(message)
			
# 			cv2.imshow('TRANSMITTING VIDEO',frame)
# 			if cv2.waitKey(1) == '13':
# 				client_socket.close()

import socket, cv2, pickle, struct, imutils
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "192.168.1.7"
port =  9111
socket_address = (host_ip, port)

server_socket.bind(socket_address)
server_socket.listen(2)  # Listen for  2 clients
print("LISTENING AT:", socket_address)

clients = []
while len(clients) <  2:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    clients.append(client_socket)

def relay_frames(client_socket):
    while True:
        data = b""
        payload_size = struct.calcsize("Q")
        while len(data) < payload_size:
            packet = client_socket.recv(4096)
            if not packet: break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)

        # Send the frame to the other client
        other_client = clients[0] if client_socket is clients[1] else clients[1]
        other_client.sendall(frame_data)

# Start relaying frames for each client
for client_socket in clients:
    client_thread = threading.Thread(target=relay_frames, args=(client_socket,))
    client_thread.start()