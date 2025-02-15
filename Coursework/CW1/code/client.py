import hashlib
import json
import os
import struct
import time
import argparse
from socket import *
from tqdm import tqdm
from datetime import datetime
import logging
import sys

MAX_PACKET_SIZE = 20480

# Const Value
OP_SAVE, OP_DELETE, OP_GET, OP_UPLOAD, OP_DOWNLOAD, OP_BYE, OP_LOGIN, OP_ERROR = 'SAVE', 'DELETE', 'GET', 'UPLOAD', 'DOWNLOAD', 'BYE', 'LOGIN', "ERROR"
TYPE_FILE, TYPE_DATA, TYPE_AUTH, DIR_EARTH = 'FILE', 'DATA', 'AUTH', 'EARTH'
FIELD_OPERATION, FIELD_DIRECTION, FIELD_TYPE, FIELD_USERNAME, FIELD_PASSWORD, FIELD_TOKEN = 'operation', 'direction', 'type', 'username', 'password', 'token'
FIELD_KEY, FIELD_SIZE, FIELD_TOTAL_BLOCK, FIELD_MD5, FIELD_BLOCK_SIZE = 'key', 'size', 'total_block', 'md5', 'block_size'
FIELD_STATUS, FIELD_STATUS_MSG, FIELD_BLOCK_INDEX = 'status', 'status_msg', 'block_index'
DIR_REQUEST, DIR_RESPONSE = 'REQUEST', 'RESPONSE'


# Set up logging
def setup_logging():
    logger = logging.getLogger('STEP_CLIENT')
    logger.setLevel(logging.INFO)

    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Add colors to different log levels
    class ColorFormatter(logging.Formatter):
        COLORS = {
            'INFO': '\033[0;32m',  # Green
            'WARNING': '\033[0;33m',  # Yellow
            'ERROR': '\033[0;31m',  # Red
            'DEBUG': '\033[0;36m',  # Cyan
            'CRITICAL': '\033[0;35m',  # Magenta
            'RESET': '\033[0m'  # Reset
        }

        def format(self, record):
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            record.msg = f"{color}{record.msg}{self.COLORS['RESET']}"
            return super().format(record)

    formatter = ColorFormatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    # File handler
    os.makedirs('client_logs', exist_ok=True)
    file_handler = logging.FileHandler(f'client_logs/step_client_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def _argparse():
    parse = argparse.ArgumentParser()
    parse.add_argument("--server_ip", default='10.0.2.6', action='store', required=False, dest="server_ip",
                       help="Please give the destination server ip address. Default bind all IP.")
    parse.add_argument("--id", default=2254472, action='store', required=False, dest="id",
                       help="Please input your student id.")
    parse.add_argument("--f", default='test.mp4', action='store', required=False, dest="f",
                       help="Please give your transition fire path.")
    return parse.parse_args()


def get_file_md5(filename):
    """Calculate MD5 hash of file"""
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def format_size(size):
    """Convert size to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def make_packet(json_data, bin_data=None):
    j = json.dumps(dict(json_data), ensure_ascii=False)
    j_len = len(j)
    if bin_data is None:
        return struct.pack('!II', j_len, 0) + j.encode()
    else:
        return struct.pack('!II', j_len, len(bin_data)) + j.encode() + bin_data


def make_request_packet(operation, data_type, json_data, bin_data=None):
    json_data[FIELD_OPERATION] = operation
    json_data[FIELD_DIRECTION] = DIR_REQUEST
    json_data[FIELD_TYPE] = data_type
    return make_packet(json_data, bin_data)


def get_tcp_packet(conn):
    bin_data = b''
    while len(bin_data) < 8:
        data_rec = conn.recv(8)
        if data_rec == b'':
            time.sleep(0.01)
        if data_rec == b'':
            return None, None
        bin_data += data_rec
    data = bin_data[:8]
    bin_data = bin_data[8:]
    j_len, b_len = struct.unpack('!II', data)
    while len(bin_data) < j_len:
        data_rec = conn.recv(j_len)
        if data_rec == b'':
            time.sleep(0.01)
        if data_rec == b'':
            return None, None
        bin_data += data_rec
    j_bin = bin_data[:j_len]

    try:
        json_data = json.loads(j_bin.decode())
    except Exception as ex:
        return None, None

    bin_data = bin_data[j_len:]
    while len(bin_data) < b_len:
        data_rec = conn.recv(b_len)
        if data_rec == b'':
            time.sleep(0.01)
        if data_rec == b'':
            return None, None
        bin_data += data_rec
    return json_data, bin_data


def connection_and_token(logger, server_ip, server_port, args):
    start_time = time.time()
    logger.info(f"Connecting to server {server_ip}:{server_port}...")

    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        logger.info(f"Connected successfully in {(time.time() - start_time):.2f} seconds")
    except Exception as e:
        logger.error(f"Connection failed: {str(e)}")
        raise

    username = str(args.id)
    password_md5 = hashlib.md5(username.encode()).hexdigest()
    user = {
        FIELD_USERNAME: username,
        FIELD_PASSWORD: password_md5
    }

    logger.info(f"Authenticating user {username}...")
    login_packet = make_request_packet(OP_LOGIN, TYPE_AUTH, user)
    client_socket.send(login_packet)

    json_data, json_bin = get_tcp_packet(client_socket)
    if json_data and json_data.get('status') == 200:
        token = json_data[FIELD_TOKEN]
        logger.info(f"Authentication successful")
        logger.info(f"Token received: {token}")
        print(f"Token validation: {token}")
        return token, client_socket
    else:
        error_msg = json_data.get('status_msg') if json_data else 'Unknown error'
        logger.error(f"Authentication failed: {error_msg}")
        raise Exception(f"Authentication failed: {error_msg}")


def save_file(logger, token, client_socket, args):
    file_path = args.f
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    size = os.path.getsize(file_path)
    file_md5 = get_file_md5(file_path)

    logger.info(f"Preparing to upload file: {file_path}")
    logger.info(f"File size: {format_size(size)}")
    logger.info(f"Local MD5: {file_md5}")

    save_request = {
        FIELD_KEY: file_path,
        FIELD_SIZE: size,
        FIELD_TOKEN: token
    }

    client_socket.send(make_request_packet(OP_SAVE, TYPE_FILE, save_request))
    json_data, bin_data = get_tcp_packet(client_socket)

    if json_data.get('status') == 200:
        logger.info("Server accepted file upload request")
        logger.info(f"Total blocks to upload: {json_data.get(FIELD_TOTAL_BLOCK)}")
        logger.info(f"Block size: {format_size(json_data.get(FIELD_BLOCK_SIZE, MAX_PACKET_SIZE))}")
    else:
        error_msg = json_data.get('status_msg') if json_data else 'Unknown error'
        logger.error(f"Server rejected file upload: {error_msg}")

    return json_data


def upload_file(logger, token, client_socket, args):
    start_time = time.time()
    json_data = save_file(logger, token, client_socket, args)

    file_path = args.f
    with open(file_path, 'rb') as f:
        image_data = f.read()

    if json_data['status'] == 200:
        upload_start_time = time.time()
        failed_blocks = []
        retry_count = 0
        total_blocks = json_data[FIELD_TOTAL_BLOCK]

        try:
            progress_bar = tqdm(
                total=json_data[FIELD_TOTAL_BLOCK],
                desc=f'Uploading {os.path.basename(file_path)}',
                unit='block',
                unit_scale=True,
                leave=True,
                position=0
            )

            for i in range(total_blocks):
                block_start_time = time.time()
                start_index = i * MAX_PACKET_SIZE
                end_index = (i + 1) * MAX_PACKET_SIZE if i < total_blocks - 1 else len(image_data)
                segment_data = image_data[start_index:end_index]

                upload_request = {
                    FIELD_KEY: json_data[FIELD_KEY],
                    FIELD_SIZE: json_data[FIELD_SIZE],
                    FIELD_BLOCK_INDEX: i,
                    FIELD_TOKEN: token,
                }

                client_socket.send(make_request_packet(OP_UPLOAD, TYPE_FILE, upload_request, segment_data))
                response, bin_data = get_tcp_packet(client_socket)

                if response.get('status', 500) == 200:
                    block_time = time.time() - block_start_time
                    transfer_rate = len(segment_data) / block_time / 1024 / 1024  # MB/s
                    logger.debug(f"Block {i + 1}/{total_blocks} uploaded successfully "
                                 f"({format_size(len(segment_data))} in {block_time:.2f}s, "
                                 f"{transfer_rate:.2f} MB/s)")
                    progress_bar.update(1)
                else:
                    error_msg = response.get('status_msg', 'Unknown error')
                    logger.error(f"Failed to upload block {i}: {error_msg}")
                    failed_blocks.append(i)
                    continue

                # Final block - check if upload is complete
                if i == total_blocks - 1:
                    progress_bar.close()
                    upload_duration = time.time() - upload_start_time
                    average_speed = (json_data[FIELD_SIZE] / upload_duration) / 1024 / 1024  # MB/s

                    logger.info("\nUpload Summary:")
                    logger.info(f"Upload completed in {upload_duration:.2f} seconds")
                    logger.info(f"Average transfer rate: {average_speed:.2f} MB/s")

                    if FIELD_MD5 in response:
                        server_md5 = response[FIELD_MD5]
                        local_md5 = get_file_md5(file_path)
                        if server_md5.lower() == local_md5.lower():
                            logger.info(f"MD5 verification successful")
                            logger.info(f"Server MD5: {server_md5}")
                            logger.info(f"Local MD5:  {local_md5}")
                        else:
                            logger.error(f"MD5 verification failed!")
                            logger.error(f"Server MD5: {server_md5}")
                            logger.error(f"Local MD5:  {local_md5}")
                    else:
                        logger.warning("No MD5 verification received from server")

        except Exception as e:
            logger.error(f"Upload error: {str(e)}")
            if 'progress_bar' in locals():
                progress_bar.close()
        finally:
            total_time = time.time() - start_time
            logger.info(f"Total operation time: {total_time:.2f} seconds")
            if failed_blocks:
                logger.error(f"Failed blocks: {failed_blocks}")
                logger.error(f"Total failed blocks: {len(failed_blocks)}")
    else:
        logger.error(f"Upload initialization failed: {json_data.get('status_msg', 'Unknown error')}")


def main():
    logger = setup_logging()
    args = _argparse()
    server_ip = args.server_ip
    server_port = 1379

    try:
        logger.info("Starting STEP client...")
        logger.info(f"Server: {server_ip}:{server_port}")
        logger.info(f"File to upload: {args.f}")

        token, client_socket = connection_and_token(logger, server_ip, server_port, args)
        upload_file(logger, token, client_socket, args)

    except Exception as e:
        logger.error(f"Operation failed: {str(e)}")
    finally:
        if 'client_socket' in locals():
            client_socket.close()
            logger.info("Connection closed")


if __name__ == '__main__':
    main()