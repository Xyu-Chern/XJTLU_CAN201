from socket import *

# 定义服务器的主机名和端口号
server_hostname = '127.0.0.1'
server_port = 12000

# 创建一个 TCP 套接字
client_socket = socket(AF_INET, SOCK_STREAM)

# 连接到服务器
client_socket.connect((server_hostname, server_port))

# 提示用户输入消息
sentence = input('Input a sentence:')

# 发送消息到服务器
client_socket.send(sentence.encode())

# 接收服务器返回的消息
modified_message = client_socket.recv(20480)

# 打印服务器返回的消息
print(modified_message.decode())

# 关闭客户端套接字，从而终止客户端与服务器之间的连接。
# 释放资源：当你创建一个套接字（socket）时，操作系统为这个套接字分配了一些系统资源，如文件描述符和网络缓冲区。在不需要这个套接字时，调用 close() 函数来释放这些资源。
# 否则，未关闭的套接字会消耗系统资源，最终可能导致资源耗尽。
# 终止连接：在使用 TCP 协议 的连接中（如你提到的代码），client_socket.close() 通知服务器客户端已经关闭了连接，并且不再发送或接收数据。这是断开连接的标准操作。
# 正确的网络编程实践：在网络编程中，始终应当在完成通信后关闭套接字。这是良好的编程实践，不仅有助于释放资源，还能避免一些未定义的行为或连接问题。
# 通知远端：在 TCP 连接中，关闭套接字还可以通知服务器端，客户端已经断开连接，允许服务器端释放对应的资源。
# 避免连接泄漏：就像在文件操作中打开的文件需要关闭一样，网络连接也是如此。如果不关闭，可能会导致程序的连接泄漏问题，使得程序和系统变得不稳定。
client_socket.close()
