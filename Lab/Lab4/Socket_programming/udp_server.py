from socket import *

# 设定服务器端口号
# 服务器端口号有什么用？端口号（Port Number）是用来区分同一设备上不同服务或应用程序的标识符。在网络通信中，一台设备（如服务器）可能会同时运行多个服务（如HTTP、FTP、SMTP等）。
# 每个服务通过不同的端口号来标识，这样网络数据可以被正确地路由到相应的服务上。
# 举例说明：一台服务器可能同时运行了一个Web服务（HTTP）和一个邮件服务（SMTP）。它们分别使用不同的端口号（如HTTP默认使用80端口，SMTP默认使用25端口）。
# 当用户访问Web服务时，服务器根据目标端口号来处理相应的HTTP请求。
server_port = 12000

# 什么是UDP协议？UDP（User Datagram Protocol） 是一种无连接的、不可靠的传输协议。
# 它是互联网协议（IP）家族的一部分，与之对应的主要传输协议是 TCP（Transmission Control Protocol）。
# UDP的特点：
# 无连接：在发送数据前，UDP 不会建立连接，因此通信速度更快、延迟更低。
# 不可靠传输：UDP 只负责发送数据，不保证数据能够被可靠接收，也没有重传机制。因此，数据可能丢失或接收顺序混乱。
# 轻量级：UDP 协议相对简单，没有复杂的握手和数据校验流程，适合对传输速度要求高但对数据准确性要求不严格的场景。
# 面向数据报：UDP 将数据封装为独立的数据报（datagram）进行传输，每个数据报是一个独立的传输单位。
# 适用场景：
# 实时通信（如视频会议、在线游戏、语音通话等），需要更低的延迟，丢包或数据顺序错乱不会严重影响体验。
# 广播和组播：适用于同时向多个接收方发送数据的场景。

# 在你的代码中，SOCK_DGRAM 表示使用 UDP 协议来传输数据。UDP 的无连接特性使得客户端和服务器之间的通信更加简单，只需发送和接收数据，而不需要建立和关闭连接。
# 创建一个 UDP 套接字，AF_INET 表示使用 IPv4，SOCK_DGRAM 表示使用 UDP 协议
server_socket = socket(AF_INET, SOCK_DGRAM)
# 将套接字绑定到指定的服务器端口号上，'' 表示监听所有可用的网络接口
server_socket.bind(('', server_port))
print('The server is ready to receive.')

# 无限循环，等待客户端的消息
while True:

# recvfrom 函数：这是一个用于接收数据的函数，适用于 UDP 套接字。
# 在调用 recvfrom() 时，它会等待从客户端接收到数据。接收到数据后，它返回一个元组，包含接收到的字节数据和发送数据的客户端地址。
# 20480：这个数字表示接收数据的最大字节数，意味着你希望一次性最多接收 20,480 字节的数据（约20 KB）。
# 如果客户端发送的数据包超过这个字节数，接收方只会接收到前 20,480 字节的数据，多余的部分将被截断丢弃。
# UDP 协议允许的数据报大小通常为 65,535 字节（包含 UDP 头部），所以 20480 在大多数应用场景下是一个合理的大小。

    message, client_address = server_socket.recvfrom(20480)
    print(message, client_address)
    
    # 将收到的消息解码为字符串并转换为大写
    modified_message = message.decode().upper()
    
    # 将修改后的消息发送回客户端
    server_socket.sendto(modified_message.encode(), client_address)