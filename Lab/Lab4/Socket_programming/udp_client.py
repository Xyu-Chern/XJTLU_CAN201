# client side
from socket import *

# '127.0.0.1' is only the localhost IP address for testing.
# If you want to send msg crossing different hosts,
# pls find the 'real' IP address using ipconfig (win) or ifconfig (linux/macos)
server_hostname = '127.0.0.1'
server_port = 12000
client_socket = socket(AF_INET, SOCK_DGRAM)
message = input('Input a sentence:')

# 1. message.encode()
# 发送的数据内容：这是你要发送的实际数据。message.encode() 将用户输入的消息字符串转换为字节（bytes），因为网络通信是通过字节数据来实现的。
# encode() 方法将字符串转换为字节格式，这对于套接字来说是必需的，因为它们只能传输字节数据，而不能直接传输字符串。
# 2(server_hostname, server_port)
# 目的地的地址信息：这里包含服务器的 IP地址 和 端口号，目的是告诉程序数据要发送到哪里。
# server_hostname：这个是服务器的 IP 地址或主机名。这里使用 '127.0.0.1' 表示本地回环地址（localhost），也就是在同一台计算机上进行通信。
# server_port：这是服务器监听的端口号。在这个示例中，服务器端口号是 12000，因此客户端通过该端口发送数据。
# 为什么需要这两个信息？
# 在使用 UDP（User Datagram Protocol） 进行通信时，每次发送数据都需要明确指定目标地址（IP 和端口），这样才能实现数据的无连接发送，这也是为什么要传递这两个参数的原因。不像 TCP 那样需要先建立连接，而是直接把数据发送给目标地址。
# 因此，客户端必须明确地指定 要发送的数据 和 服务器的位置（IP 和端口），这样数据报才能正确地发送到服务器上。
client_socket.sendto(message.encode(), (server_hostname, server_port))
modified_message, server_address = client_socket.recvfrom(20480)
print(modified_message.decode(), server_address)
client_socket.close()