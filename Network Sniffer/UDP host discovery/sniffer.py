import socket
import os

# host to listen on

HOST = '192.168.214.75'

def main():
    # create raw socket
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else :
        socket_protocol = socket.IPPROTO_ICMP
    
    sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)
    sniffer.bind((HOST,0)) # bind to public interface
    # include the IP header in the capture
    sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)
    
    # read packet
    print(sniffer.recvfrom(65565))

    # for windows system

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)

    if __name__=='__main__':
        main()