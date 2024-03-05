# import socket
# import cv2
# import pickle
# import struct
# import threading

# def handle_client(client_socket):
#     data = b""
#     payload_size = struct.calcsize("Q")
#     print("GOT CONNECTION FROM:", client_socket.getpeername())
#     try:
#         while True:
#             while len(data) < payload_size:
#                 packet = client_socket.recv(4*1024)
#                 if not packet:
#                     break
#                 data += packet
#             packed_msg_size = data[:payload_size]
#             data = data[payload_size:]
#             msg_size = struct.unpack("Q", packed_msg_size)[0]
#             while len(data) < msg_size:
#                 data += client_socket.recv(4*1024)
#             frame_data = data[:msg_size]
#             data = data[msg_size:]
#             frame = pickle.loads(frame_data)
#             cv2.imshow("Receiving...", frame)
#             key = cv2.waitKey(10)
#             if key == 13:
#                 break
#     finally:
#         client_socket.close()

# def main():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     host_ip = '172.20.10.2'
#     print('HOST IP:', host_ip)
#     port = 9995
#     socket_address = (host_ip, port)

#     server_socket.bind(socket_address)
#     server_socket.listen(5)
#     print("LISTENING AT:", socket_address)

#     while True:
#         client_socket, addr = server_socket.accept()
#         client_handler = threading.Thread(
#             target=handle_client, args=(client_socket, ))
#         client_handler.start()


# if __name__ == "__main__":
#     main()

# import socket
# import cv2
# import pickle
# import struct
# import threading

# clients = []  # List to keep track of all connected clients

# def handle_client(client_socket):
#     global clients
#     data = b""
#     payload_size = struct.calcsize("Q")
#     print("GOT CONNECTION FROM:", client_socket.getpeername())
#     clients.append(client_socket)  # Add the new client to the list
#     try:
#         while True:
#             while len(data) < payload_size:
#                 packet = client_socket.recv(4*1024)
#                 if not packet:
#                     break
#                 data += packet
#             packed_msg_size = data[:payload_size]
#             data = data[payload_size:]
#             msg_size = struct.unpack("Q", packed_msg_size)[0]
#             while len(data) < msg_size:
#                 data += client_socket.recv(4*1024)
#             frame_data = data[:msg_size]
#             data = data[msg_size:]
#             frame = pickle.loads(frame_data)
#             cv2.imshow("Receiving...", frame)
#             key = cv2.waitKey(10)
#             if key ==  13:
#                 break
#             # Broadcast the frame to all clients except the sender
#             for client in clients:
#                 if client != client_socket:
#                     try:
#                         client.sendall(frame_data)
#                     except Exception as e:
#                         print(f"Error sending frame to client: {e}")
#     finally:
#         clients.remove(client_socket)  # Remove the client from the list when done
#         client_socket.close()

# def main():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     host_ip = '172.20.10.4'
#     print('HOST IP:', host_ip)
#     port = 9995
#     socket_address = (host_ip, port)

#     server_socket.bind(socket_address)
#     server_socket.listen(5)
#     print("LISTENING AT:", socket_address)

#     while True:
#         client_socket, addr = server_socket.accept()
#         client_handler = threading.Thread(
#             target=handle_client, args=(client_socket, ))
#         client_handler.start()

# if __name__ == "__main__":
#     main()

import socket
import cv2
import pickle
import struct
import threading

clients = []  # List to keep track of all connected clients
forward_clients = []  # List to keep track of clients for forwarding frames

def handle_client(client_socket):
    global clients
    data = b""
    payload_size = struct.calcsize("Q")
    print("GOT CONNECTION FROM:", client_socket.getpeername())
    clients.append(client_socket)  # Add the new client to the list
    try:
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
            if key ==  13:
                break
            # Forward the frame to all clients except the sender
            for client in forward_clients:
                if client != client_socket:
                    try:
                        client.sendall(frame_data)
                    except Exception as e:
                        print(f"Error sending frame to client: {e}")
    finally:
        clients.remove(client_socket)  # Remove the client from the list when done
        client_socket.close()

def handle_forward_client(forward_client_socket):
    global forward_clients
    data = b""
    payload_size = struct.calcsize("Q")
    print("GOT CONNECTION FOR FORWARDING FROM:", forward_client_socket.getpeername())
    forward_clients.append(forward_client_socket)  # Add the new client to the list
    try:
        while True:
            while len(data) < payload_size:
                packet = forward_client_socket.recv(4*1024)
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += forward_client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            cv2.imshow("Forwarded...", frame)
            key = cv2.waitKey(10)
            if key ==  13:
                break
    finally:
        forward_clients.remove(forward_client_socket)  # Remove the client from the list when done
        forward_client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    forward_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = ''
    print('HOST IP:', host_ip)
    port =  9995
    forward_port =  9996  # Different port for forwarding
    socket_address = (host_ip, port)
    forward_socket_address = (host_ip, forward_port)

    server_socket.bind(socket_address)
    forward_server_socket.bind(forward_socket_address)
    server_socket.listen(5)
    forward_server_socket.listen(5)
    print("LISTENING AT:", socket_address)
    print("LISTENING FOR FORWARDING AT:", forward_socket_address)

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket,  ))
        client_handler.start()

        # forward_client_socket, forward_addr = forward_server_socket.accept()
        # forward_client_handler = threading.Thread(
        #     target=handle_forward_client, args=(forward_client_socket,  ))
        # forward_client_handler.start()

if __name__ == "__main__":
    main()
