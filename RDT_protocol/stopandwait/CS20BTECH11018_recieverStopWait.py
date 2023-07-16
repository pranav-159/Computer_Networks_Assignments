from socket import *
import struct

host="10.0.0.2"
port = 20002
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)
buf=1027


def extract_pkt(rcvpkt):
    hdr = rcvpkt[:3]
    hdr = struct.unpack('h?',hdr)
    data = rcvpkt[3:]
    return (hdr[0],hdr[1],data)

def makeACK(seq):
    return struct.pack('h?',seq,False)


while True:
    f = open("recieved.jpg",'wb')
    seq = 0


    rcv_pkt,addr = s.recvfrom(buf)

    rcv_pkt = extract_pkt(rcv_pkt)

    while(not rcv_pkt[1]):
        if seq == rcv_pkt[0]:
            f.write(rcv_pkt[2])
            seq=(seq+1)%2
        s.sendto(makeACK(rcv_pkt[0]),addr)
        rcv_pkt,addr = s.recvfrom(buf)
        rcv_pkt = extract_pkt(rcv_pkt) 


    f.close()
s.close()