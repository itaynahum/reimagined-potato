import socket
import threading

from Server_Client.Config import Config, init_logger

logger = init_logger()
lock = threading.Lock()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = []
logger.debug(msg=f"Created Socket Successfully...\r\n\t{s}")

#test
#itay
def broadcast(conn, username, message, log):
    """
    Broadcasting method
    :param conn: Connection
    :param username: Username which message is being sent from.
    :param message: The message it self
    :param log: Logger object
    :return: None
    """
    log.debug(msg=f"Received a message from connection {conn}, username {username}")
    broadcast_message = f'{username}: {message}'
    for connection in connections:
        if connection != conn:
            connection.send(broadcast_message.encode('utf-8'))
            log.debug(msg=f"Broadcasting message from username {username} to all connections..")


def send_messages_to_all_connections(conn, addr, log):
    """
    Handling Connection
    :param conn: Connection address
    :param addr: address
    :param log: logger object
    :return: None
    """
    connected = True
    connections.append(conn)
    log.debug(msg=f"Active connections - {threading.activeCount() - 1}.\r\n\tConnections: {connections}")
    log.debug(msg=f"Started listening on address {addr} for data...")
    while connected:
        try:
            data = conn.recv(Config.BUFFER)
            if data.decode(Config.STRING_FORMAT) == Config.QUIT_MESSAGE:
                conn.close()

            username = data.decode('utf-8').split(' ')[0]
            message = ' '.join(data.decode('utf-8').split(' ')[1:])
            broadcast(conn, username, message, log)
        except Exception as exc:
            log.error(msg=f"An Exception has been raised. \r\n\t{exc}")
            break


def bind_address(s, logger):
    """
    Binding given host to given port
    :param s: Socket
    :param logger: Logger object
    :return: None
    """
    logger.debug(msg=f"Trying to bind Host: {Config.HOST} to Port: {Config.PORT}...")
    try:
        logger.info(msg=f"Binded Host: {Config.HOST} to Port: {Config.PORT} Successfully")
        s.bind((Config.HOST, Config.PORT))
    except Exception as e:
        logger.error(msg=f"An Error occured while trying to bind host to port.\r\n\t{e}")


def accept_connection(sock, log):
    """
    Accepting Connection from user
    :return: None
    """
    log.info(msg="Listening for new connections...")
    sock.listen(Config.ACCEPT_CONNECTION_LIMIT)

    while True:
        try:
            conn, addr = sock.accept()
            log.debug(msg=f"Connected Successfully to address: {addr}, \r\n\tConnection: {conn}")
            thread = threading.Thread(target=send_messages_to_all_connections, args=(conn, addr, log))
            thread.start()
        except ConnectionRefusedError or KeyboardInterrupt as e:
            log.error(f"Connection Aborted by client. \r\n\t{e}")
            accept_connection(sock, logger)


if __name__ == '__main__':
    bind_address(s, logger)
    accept_connection(s, logger)
