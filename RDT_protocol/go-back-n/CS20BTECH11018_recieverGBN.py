from socket import *
import struct
import select

host="10.0.0.2"
port = 20002
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)
buf=1027
TIMEOUT = 0.5


def extract_pkt(rcvpkt):
    hdr = rcvpkt[:3]
    hdr = struct.unpack('H?',hdr)
    data = rcvpkt[3:]
    return (hdr[0],hdr[1],data)

def makeACK(seq):
    return struct.pack('H?',seq,False)



f = open("recieved.jpg",'wb')

counter = 1


while 1:
    msg,sender_address = s.recvfrom(buf)
    msg = extract_pkt(msg)

    print("recieved - {}".format(msg[0]))

    #get ending flag
    # if msg[1]:
    #     ack = makeACK(counter)
    #     s.sendto(ack,sender_address)
    #     f.write(msg[2])
    #     break
    #when expected packet arrived
    if counter==msg[0]:
        ack = makeACK(counter)
        s.sendto(ack,sender_address)
        print("sent ack {}".format(extract_pkt(ack)[0]))
        f.write(msg[2])
        counter+=1
    #when duplicate packet arrived
    elif msg[0] < counter:
        ack = makeACK(counter-1)
        s.sendto(ack,sender_address)
        print("sent ack {}".format(extract_pkt(ack)[0]))
    #when disordered packet arrived / discard
    else:
        ack = makeACK(counter-1)
        s.sendto(ack,sender_address)

f.close()
s.close()