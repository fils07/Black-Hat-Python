import socket

target_host = "127.0.0.1"
target_port = 9998

# udp client 
client =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# send some data
client.sendto(b"AAAABBBBCCC",(target_host,target_port))
# receive data
data,addr=client.recvfrom(4096)

print(data.close())

client.close()