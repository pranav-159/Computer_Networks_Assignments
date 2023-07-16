import socket
# import json

#WRITE CODE HERE:
#1. Create a KEY-VALUE pairs (Create a dictionary OR Maintain a text file for KEY-VALUES).

# dict_file = open("table.json","r+")
# dict = json.load(dict_file,) 
dict = {}
# dst_ip = str(input("Enter Server IP: "))
dst_ip = "10.0.1.2"

s = socket.socket()
print ("Socket successfully created")

dport = 12346

s.bind((dst_ip, dport))
print ("socket binded to %s" %(dport))

s.listen(5)
print ("socket is listening")

while True:
  c, addr = s.accept()
  print ('Got connection from', addr )

  while True:

    recvmsg = c.recv(1024).decode()
    if not recvmsg:
     break
    print('Server received '+recvmsg)

    recvlist = recvmsg.split(" ")

    if len(recvlist) != 3 or recvlist[2] != "HTTP/1.1\r\r\n":
      c.send("HTTP/1.1 400 Bad Request\r\r\n".encode())

    elif recvlist[0] == "GET":
      query = recvlist[1].split("=")

      if len(query) != 2 or query[0] != "/assignment1?request":
        c.send("HTTP/1.1 400 Bad Request\r\r\n".encode())
      elif query[1] in dict:
        c.send(("HTTP/1.1 200 OK\r\r\n"+"Value = "+str(dict[query[1]])+"\r\r\n").encode())
      else:
        c.send("HTTP/1.1 404 Not Found\r\r\n".encode())

    elif recvlist[0] == "PUT":
      query = recvlist[1].split("/")

      if len(query) != 4 or query[0] != "" or query[1] != "assignment1":
        c.send("HTTP/1.1 400 Bad Request\r\r\n".encode())
      else:
        dict[query[2]] = query[3]
        c.send("HTTP/1.1 201 Created\r\r\n".encode())

    elif recvlist[0] == "DELETE":
      query = recvlist[1].split("/")
      if len(query) != 3 or query[0] != "" or query[1] != "assignment1":
        c.send("HTTP/1.1 400 Bad Request\r\r\n".encode())
      else:
        k = dict.pop(query[2],1)
        if k==1:
          c.send("HTTP/1.1 200 OK\r\r\n".encode())
        else:
          c.send(("HTTP/1.1 200 OK\r\r\n"+"Deleted {}\r\r\n".format(query[2])).encode())

    else:
      c.send("HTTP/1.1 400 Bad Request\r\r\n".encode())



  #Write your code here
  #1. Uncomment c.send 
  #2. Parse the received HTTP request
  #3. Do the necessary operation depending upon whether it is GET, PUT or DELETE
  #4. Send response
  ##################
  # json.dump(dict,dict_file)
  # dict_file.close()
  c.close()
  #break
