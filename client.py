# import socket,cv2,pickle,struct
# client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# host_ip = "192.168.1.7"
# port = 9222
# client_socket.connect((host_ip,port))
# data = b""
# payload_size = struct.calcsize("Q")
# while True:
# 	while len(data) < payload_size:
# 		packet = client_socket.recv(8*1024) 
# 		if not packet: break
# 		data+=packet
# 	packed_msg_size = data[:payload_size]
# 	data = data[payload_size:]
# 	msg_size = struct.unpack("Q",packed_msg_size)[0]
	
# 	while len(data) < msg_size:
# 		data += client_socket.recv(8*1024)
# 	frame_data = data[:msg_size]
# 	data  = data[msg_size:]
# 	frame = pickle.loads(frame_data)
# 	cv2.imshow("RECEIVING VIDEO",frame)
# 	if cv2.waitKey(1) == '13':
# 		break
# client_socket.close()

import socket, cv2, pickle, struct
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "192.168.1.7"
port =  9111
client_socket.connect((host_ip, port))

def send_frames(client_socket):
    vid = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    while vid.isOpened():
        ret, frame = vid.read()
        if not ret:
            break
        frame = cv2.resize(frame, (320,  240))
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        client_socket.sendall(message)
        cv2.imshow('TRANSMITTING VIDEO', frame)
        if cv2.waitKey(1) &  0xFF == ord('q'):
            break
    client_socket.close()

def receive_frames(client_socket):
    while True:
        data = b""
        payload_size = struct.calcsize("Q")
        while len(data) < payload_size:
            try:
                packet = client_socket.recv(4096)
            except OSError as e:
                if e.errno ==  9:  # Bad file descriptor
                    print("Socket is not open or already closed.")
                else:
                    print(f"Unexpected error: {e}")
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("RECEIVING VIDEO", frame)
        if cv2.waitKey(1) &  0xFF == ord('q'):
            break
    client_socket.close()

# Create threads for sending and receiving frames
send_thread = threading.Thread(target=send_frames, args=(client_socket,))
receive_thread = threading.Thread(target=receive_frames, args=(client_socket,))

send_thread.start()
receive_thread.start()

send_thread.join()
receive_thread.join()