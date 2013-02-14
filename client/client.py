
import socket
import time

HOST = '127.0.0.1'
PORT = 1060

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
#	s.sendall("Hello")
time.sleep(1)  # hang
msg = s.recv(1028)  
print(msg)
