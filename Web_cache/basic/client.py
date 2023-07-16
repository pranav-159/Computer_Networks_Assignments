import socket
import sys

serverIP = "10.0.1.2"

# dst_ip = str(input("Enter dstIP: "))
dst_ip="10.0.1.2"
s = socket.socket()

print(dst_ip)

port = 12346

s.connect((dst_ip, port))

#Write your code here:
#1. Add code to send HTTP GET / PUT / DELETE request. The request should also include KEY.
#2. Add the code to parse the response you get from the server.
def get(key):
    s.send('GET /assignment1?request={} HTTP/1.1\r\r\n'.format(key).encode())
    resp = s.recv(1024).decode()
    print(resp)
def put(key,value):
    s.send('PUT /assignment1/{}/{} HTTP/1.1\r\r\n'.format(key,value).encode())
    resp = s.recv(1024).decode()
    print(resp)
def delete(key):
    s.send('DELETE /assignment1/{} HTTP/1.1\r\r\n'.format(key).encode())
    resp = s.recv(1024).decode()
    print(resp)
# put("key1","value1")
# put("key2","value2")
# put("key3","value3")
# put("key4","value4")
# put("key5","value5")
# put("key6","value6")
# put("key7","key7")
# get("key1")
# get(sys.argv[1])

# put("key1","value1")
# get("key1")
# delete("key1")

try:
  while True:
      req_type = input("Enter Request(PUT:'P',GET:'G',DELETE:'D'): ")
      if req_type == 'P':
          key = input("Enter Key: ")
          value = input("Enter Value: ")
          put(key,value)
      elif req_type == 'G':
          key = input("Enter key: ")
          get(key)
      elif req_type == 'D':
          key = input("Enter Deleting key: ")
          delete(key)
      else:
          print("Bad request.Try again")
except KeyboardInterrupt:
  s.close()
