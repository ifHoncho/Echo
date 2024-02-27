import socket

UDP_IP = "0.0.0.0"  # Listen on all available interfaces
UDP_PORT = 14545  # Port to listen on

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
sock.bind((UDP_IP, UDP_PORT))

print("UDP server listening on port", UDP_PORT)

while True:
    # Receive data from the socket
    data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
    message = data.decode()
    print("Data Received :", message)

    # Extract node, strength, and target_strength from received message
    parts = message.split(", ")
    node = parts[0]
    strength, target_strength = parts[1][:], parts[2]

    # Update signal_strength_data.txt based on the received message
    with open('signal_strength_data.txt', 'r') as file:
        lines = file.readlines()

    if node == 'A':
        lines[1] = strength + '\n'
        lines[7] = target_strength + '\n'
    elif node == 'B':
        lines[3] = strength + '\n'
        lines[9] = target_strength + '\n'
    elif node == 'C':
        lines[5] = strength + '\n'
        lines[11] = target_strength + '\n'

    with open('signal_strength_data.txt', 'w') as file:
        file.writelines(lines)