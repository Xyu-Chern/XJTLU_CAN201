from socket import *

# 定义服务器的端口号
server_port = 12000

# 创建一个 TCP 套接字, SOCK_STREAM 表示使用 TCP 协议。
# 关键区别（与UDP版本的不同）：
# TCP 是面向连接的：客户端和服务器之间必须先建立连接，然后才能进行数据传输。这在代码中由 connect() 和 accept() 函数体现。
# 可靠的数据传输：TCP 提供数据的可靠传输，确保消息的顺序和完整性。因此，在 TCP 中，发送的数据将被完整、准确地接收。
# 基于流：TCP 以字节流的方式传输数据，而 UDP 则是以数据报的形式。
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))

# 开始监听连接请求，参数 10 表示最多允许 10 个未处理的连接请求
# listen() 函数用于将服务器套接字设为被动监听模式，表示服务器已经准备好接受连接请求。它不会主动发起连接，而是等待客户端来连接。
# 10 的意义： 这个数字表示服务器允许的 未处理的连接请求的最大数量。
# 如果服务器已经有 10 个连接请求在排队等待被 accept() 处理，那么再有新的连接请求进来，它们将被拒绝或遭遇连接延迟。
# 为什么需要设定这个值？
# 设定一个合适的队列长度可以保证服务器不会因为连接请求过多而崩溃。当并发连接的请求数量超过处理能力时，服务器可以有一个“缓冲区”来排队处理这些请求，而不会直接拒绝所有新请求。
# 需要注意的是，这个参数并不表示服务器能够同时处理多少个连接（连接处理的数量取决于服务器代码的实现，如多线程或异步 I/O），而是指 排队等待 被 accept() 接受的连接请求的最大数量。
server_socket.listen(10)
print('The TCP server is listening')

# 无限循环以接受客户端的连接
while True:
    # connection_socket, addr = server_socket.accept() 这一行代码的作用是 接受客户端的连接请求。
    # 当服务器套接字（server_socket）处于监听状态时，它会等待客户端的连接请求，一旦有客户端请求连接，这个函数就会返回一个新的套接字和客户端的地址信息。
    # 当一个客户端连接到服务器时，accept() 方法会创建一个新的套接字对象（connection_socket）。服务器使用这个新的套接字与当前连接的客户端进行通信，而不会影响原本的监听套接字（server_socket）。
    # 这个设计允许服务器继续监听新的客户端连接，同时与多个客户端进行并行通信。
    connection_socket, addr = server_socket.accept()

    # 接收客户端发送的消息，最大字节数为 20480，并将其解码为字符串
    sentence = connection_socket.recv(20480).decode()

    # 将收到的消息转换为大写
    capitalized_sentence = sentence.upper()

    # 将转换后的消息发送回客户端
    connection_socket.send(capitalized_sentence.encode())
