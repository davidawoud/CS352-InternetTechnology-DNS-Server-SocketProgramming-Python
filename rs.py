import threading
import time
import socket
import select
import errno

def rs():
    # TS1 Client
    try:
        ts1_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS1_Client]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    ts1_client.connect(server_binding)
    ts1_client.setblocking(0)
    ts1_client.settimeout(5)

    # TS2 Client
    
    try:
        ts2_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS1_Client]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = 50014
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    ts2_client.connect(server_binding)
    ts2_client.setblocking(0)
    ts2_client.settimeout(5)


    # root server
    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[RS]: RS socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50021)
    rs.bind(server_binding)
    rs.listen(5)
    host = socket.gethostname()
    print("[RS]: RS host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[RS]: RS IP addrers is {}".format(localhost_ip))
    csockid, addr = rs.accept()
    csockid.setblocking(0)
    csockid.settimeout(60)
    print ("[RS]: Got a connection request from a client at {}".format(addr))

    # send a intro mersage to the client
    msg = "Welcome to RS!"
    try:
        csockid.send(msg.encode('utf-8'))     
    except socket.error as e:
        if e.errno != errno.EAGAIN:
            raise e
        select.select([], [csockid], [])
        
    # Receive data from the client
    data_client = ""
    res_ts = ""
    while True:
        time.sleep(1)
        try:
            data_client = csockid.recv(200).decode('utf-8')
            print("Looking Up: {}".format(data_client))
            if (data_client == "q"):
                break
        except socket.timeout as e:
            break

        try:
            ts1_client.send(data_client.encode('utf-8'))
            ts2_client.send(data_client.encode('utf-8'))
        except socket.error as e:
            if e.errno != errno.EAGAIN:
                raise e
            pass

        time.sleep(1)
        try:
            res_ts = ts1_client.recv(200).decode('utf-8')
            print("{}\n".format(res_ts))
        except socket.timeout as e:
            try:
                res_ts = ts2_client.recv(200).decode('utf-8')
                print("{}\n".format(res_ts))
            except socket.timeout as e:
                try:
                    csockid.send("{} - TIMED OUT\n".format(data_client).encode('utf-8'))
                    print("{} - TIMED OUT\n".format(data_client))
                except socket.error as e:
                    if e.errno != errno.EAGAIN:
                        raise e
                    pass
                continue

        try:
            csockid.send("{}\n".format(res_ts).encode('utf-8'))
        except socket.error as e:
            if e.errno != errno.EAGAIN:
                raise e
            pass

    # Close the rs, ts1_client & ts2_client socket
    ts1_client.send("q".encode('utf-8'))
    ts1_client.close()
    ts2_client.send("q".encode('utf-8'))
    ts2_client.close()
    rs.close()
    print("Done.")
    exit()
    
if __name__ == "__main__":
    t1 = threading.Thread(name='rs', target=rs)
    t1.start()