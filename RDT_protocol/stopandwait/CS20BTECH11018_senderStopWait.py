


from socket import *
from time import *
import sys
import struct
import select

s = socket(AF_INET,SOCK_DGRAM)
host ="10.0.0.2"
port = 20002
buf =1024
addr = (host,port)



def make_pkt(seq,flag,data):
    hdr = struct.pack('h?',seq,flag)
    return hdr+data


def extract_pkt(rcvpkt):
    hdr = rcvpkt[:3]
    hdr = struct.unpack('h?',hdr)
    data = rcvpkt[3:]
    return (hdr[0],hdr[1],data)


def isACK(rcvpkt:bytes,ack):
    hdr = rcvpkt[:3]
    hdr = struct.unpack('h?',hdr)
    return hdr[0]==ack

timeouts=0

# s.setblocking(0)
TIMEOUT = float(sys.argv[2])

f= open(sys.argv[1], "rb") 
tp = open("timeouts.csv","a+")


data = f.read(buf)
seq = 0
end = not bool(data)
snd_pkt = make_pkt(seq,end,data)

start=time()
while (data or end):

    if(s.sendto(snd_pkt,addr)):
        print("sending {}".format(seq))
        # sleep(0.01)
        if end: break
        ready = select.select([s],[],[],TIMEOUT)

        if ready[0]:
            rcv_pkt, addr = s.recvfrom(1027)
            if isACK(rcv_pkt,seq):
                data = f.read(buf)
                seq = (seq+1)%2
                end = not bool(data)
                snd_pkt = make_pkt(seq,end,data)
        else:
            timeouts = timeouts+1
        
end=time()

tp.write("{},{},{}\n".format(TIMEOUT,timeouts,1145/(end-start)))
tp.close()

s.close()
f.close()