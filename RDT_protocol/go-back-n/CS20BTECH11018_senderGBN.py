


from socket import *
from time import *
import sys
import struct
import select


s = socket(AF_INET,SOCK_DGRAM)
host ="10.0.0.2"
port = 20002
mss =1024
addr = (host,port)

# s.setblocking(0)
TIMEOUT = 0.05
N = 2**int(sys.argv[1])



def make_pkt(seq,flag,data):
    hdr = struct.pack('H?',seq,flag)
    return hdr+data


def extract_pkt(rcvpkt):
    hdr = rcvpkt[:3]
    hdr = struct.unpack('H?',hdr)
    data = rcvpkt[3:]
    return (hdr[0],hdr[1],data)


def isACK(rcvpkt:bytes,ack):
    hdr = rcvpkt[:3]
    hdr = struct.unpack('H?',hdr)
    return ack<=hdr[0]

def isLast(rcvpkt:bytes):
    hdr = rcvpkt[:3]
    hdr = struct.unpack('H?',hdr)
    return hdr[1]


f= open("testFile.jpg", "rb") 
ft= open("throughput.csv", "a+")

base = 0
nextseqnum = 0


#convert file to packets
pkts = {}
count=0
data = f.read(mss)
while data:
    count+=1
    pkts[count] = make_pkt(count,len(data)<mss,data)
    data = f.read(mss)
f.close()

base=1
next=1
start = time()
while 1:
    if base>len(pkts):
        break
    #send pkts
    while next<base+N and base<=next:
        # sleep(0.01)
        s.sendto(pkts[next],addr)
        print("sent {} base {}".format(next,base))
        if isLast(pkts[next]):
            break
        next+=1
    
    #receive ack
    ready = select.select([s],[],[],TIMEOUT)

    if ready[0]:
        rcv_pkt, addr = s.recvfrom(3)
        rcv_pkt = extract_pkt(rcv_pkt)
        if base<=rcv_pkt[0]:
            print("recieved ack {}".format(rcv_pkt[0]))
            base=rcv_pkt[0]+1
    else:
        next=base
end = time()
throughput = len(pkts)/(end-start)
ft.write("{},{}\n".format(N,throughput))

s.close()