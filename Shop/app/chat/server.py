from socket import *
from time import ctime

host = ''  # 默认监听所有访问本机服务器的ip主机
port = 12345  # 接受访问的本机端口号
bufsize = 1024  # 缓冲区，用于存放收到的数据
addr = (host, port)

udpServer = socket(AF_INET, SOCK_DGRAM)  # 建立服务器
udpServer.bind(addr)  # 开始监听
print('等待连接……')
while True:
    data, addr = udpServer.recvfrom(bufsize)  # 接收数据和返回地址
    # 处理数据
    data = data.decode(encoding='utf-8').upper()
    data = "at %s :%s" % (ctime(), data)
    print('收到', data, '来自', addr)
    msg = input('客服输入消息:')
    udpServer.sendto(msg.encode(encoding='utf-8'), addr)
    # 发送数据


# udpServer.close()

