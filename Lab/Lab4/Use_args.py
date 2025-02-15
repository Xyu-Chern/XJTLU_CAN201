import argparse

def _argparse():
    parser = argparse.ArgumentParser(description="This is description!")
    # 使用 dest='path' 指定属性名为 path，而不是默认的 input。

    ''' script.py 举例
    # import argparse

    # parser = argparse.ArgumentParser(description="Example script")
    # parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    # args = parser.parse_args()

    # if args.verbose:
    #     print("Verbose mode is enabled")
    # else:
    #     print("Verbose mode is not enabled")
        
    python script.py --verbose  # 输出：Verbose mode is enabled
    python script.py            # 输出：Verbose mode is not enabled
    '''

    parser.add_argument('--input', action='store', default='default_input_path', dest='path', help='The path of input file')
    parser.add_argument('--server', action='store', default='localhost', dest='server', help='The hostname of server')
    parser.add_argument('--port', action='store', default='8080', dest='port', help='The port of server')
    return parser.parse_args()

def main():
    parser = _argparse()
    print(parser)
    print('Input file:', parser.path)
    print('Server:', parser.server)
    print('Port:', parser.port)

if __name__ == '__main__':
    main()
