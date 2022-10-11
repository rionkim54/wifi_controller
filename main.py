
import socket
import time

host = "192.168.0.37"
# host = "127.0.0.1"
port = 8899
MaxBytes = 1024*1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(30)

client.connect((host, port))

index = 0
client.send(bytes(bytearray([0x55,0xaa,0x5a,0xa5,0x7e,index,0x80,0x00,0x80,0x08,0x68,0x00,0x00,0x01,0x00,0x0a,0x01,0x00,0x01,0x00,0x7e])))

def sendData(value):
    global index
    index += 1
    if(0x0f < index) :
        index = 1
    client.send(bytes(bytearray([0x55,0xaa,0x5a,0xa5,0x7e,index,0x80,0x11,0x00,0x39,0xaf,0x00,0x00,0x01,0x00,0x07,0x02,0x00,0x00,value,0x00,0x7e])))

dimmingValue = 0

while True:

    # sendBytes = client.send('')
    sendData(dimmingValue)
    print(dimmingValue)

    recvData = client.recv(MaxBytes)
    if not recvData:
        print('      ，     ')
    else:
        localTime = time.asctime( time.localtime(time.time()))
        print(localTime, '         :',len(recvData))
        print(recvData)

    dimmingValue += 80
    if(255 < dimmingValue) :
        dimmingValue = 0 
    time.sleep(1)

    pass

client.close()






