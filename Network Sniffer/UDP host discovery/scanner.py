import ipaddress
import os
import socket
import struct
import sys
import time
import threading
# subnet target
SUBNET = '192.168.122.0/24'
# Check ICMP responses
MESSAGE = 'PYTHONRULES!'

class IP :
    def __init__(self,buff=None):
        header = struct.unpack('<BBHHHBBH4s4s',buff)
        self.ver = header[0] >> 4
        self.ihl = header[0] >> 4

        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)
        # map protocol constants to their names
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            print('%s No protocol for %s' % (e, self.protocol_num))
            self.protocol = str(self.protocol_num)

class ICMP:
    def __init__(self,buff):
        header = struct.unpack('<BBHHH',buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

# send UDP Datagram to all host of network

def udp_sender():
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sender :
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sender.sendto(bytes(MESSAGE,'utf8'),(str(ip),65212))
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        myIP = s.getsockname()[0]
    except Exception:
        myIP = '127.0.0.1'
    finally:
        s.close()
    return myIP

class Scanner :
     def __init__(self,host):
        self.host=host
        if os.name == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else :
            socket_protocol = socket.IPPROTO_ICMP
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)
        self.socket.bind((host,0))
        self.socket.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
        
        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

     def sniff(self):
            # check the system
            hosts_up = set([f'{str(self.host)}'])
            try :
                while True:
                    raw_buffer = self.socket.recvfrom(65535)[0]
                    ip_header = IP(raw_buffer[0:20])
                    if ip_header.protocol == "ICMP":
                        print('Protocol : %s %s -> %s'%(ip_header.protocol,ip_header.src_address,ip_header.dst_address))
                        print(f'Version : {ip_header.ver}')
                        print(f'Header Length : {ip_header.ihl} TTL:{ip_header.ttl}')

                        # start of ICMP Packet
                        offset = ip_header.ihl*4
                        buf = raw_buffer[offset:offset + 8]
                        # Creat ICMP Structure
                        icmp_header=ICMP(buf)
                        # Check for TYPE 3 and CODE
                        #print(f"code {icmp_header.code} type {icmp_header.type}")
                        if icmp_header.code ==168 and icmp_header.type == 192:
                            #print("code & type")
                            if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(SUBNET):
                                # Check for our magic message
                                if raw_buffer[len(raw_buffer)-len(MESSAGE):]==bytes(MESSAGE,'utf8'):
                                    tgt = str(ip_header.src_address)
                                    if tgt != self.host and tgt not in hosts_up :
                                        hosts_up.add(str(ip_header.src_address))
                                        print(f'Host Up : {tgt}')
                                #print('ICMP -> Type : %s Code : %s \n'%(icmp_header.type,icmp_header.code))
            except KeyboardInterrupt :
                if os.name == 'nt':
                    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)
                print('\n User interrupted')
                if hosts_up:
                    print(f'\n\n Summary : Hosts up on {SUBNET}')
                for host in sorted(hosts_up):
                    print(f'{host}')
                print('')
                sys.exit()
    
if __name__=='__main__':
    if len(sys.argv)==2:
        host = sys.argv[1]
    else:
        host = get_ip()
    print("________ \n Welcome to our custom network sniffer \n ________ \n Use CTRL+C to stop sniffing ")
    s = Scanner(host)
    time.sleep(5)
    t=threading.Thread(target=udp_sender)
    t.start()
    s.sniff()