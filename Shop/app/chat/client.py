from socket import *

host = '192.168.3.6'  # 服务器的ip
port = 12345  # 接口选择大于10000
bufsize = 1024  # 定义缓冲

addr = (host, port)
udpClient = socket(AF_INET, SOCK_DGRAM)  # 创建socket客户端

while True:
    data = input('>>>用户输入信息:')
    if not data:
        break
    data = data.encode(encoding="utf-8")
    udpClient.sendto(data, addr)  # 发送数据
    data, addr = udpClient.recvfrom(bufsize)  # 成功发送至服务器端后，接收服务器发送的返回数据和返回地址
    print(data.decode(encoding='utf-8'), 'from', addr)

udpClient.close()

