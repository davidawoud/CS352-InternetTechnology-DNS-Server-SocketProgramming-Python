import threading
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
    #ts1_client.setblocking(0)

    # Receive data from the server
    data_from_server=ts1_client.recv(200)
    print("[TS1_Client]: Data received from server: {}".format(data_from_server.decode('utf-8')))

    ts1_client.send("q".encode('utf-8'))

    # TS2 Client
    
    # ---code---


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
    print ("[RS]: Got a connection request from a client at {}".format(addr))

    # send a intro mersage to the client.  
    msg = "Welcome to RS!"
    #csockid.send(msg.encode('utf-8'))

    data_client=csockid.recv(200).decode('utf-8')
    print(data_client)
    data_client=csockid.recv(200).decode('utf-8')
    print(data_client)
    data_client=csockid.recv(200).decode('utf-8')
    print(data_client)

    # Close the rs, ts1_client & ts2_client socket
    ts1_client.close()
    print("Done.") 

    rs.close()
    print("Done.")
    exit()
    
if __name__ == "__main__":
    t1 = threading.Thread(name='rs', target=rs)
    t1.start()