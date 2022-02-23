import threading
import socket
import sys

def client(rsHostname, rsListenPort):
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # connect to the server on local machine
    localhost_addr = socket.gethostbyname(rsHostname)
    server_binding = (localhost_addr, rsListenPort)
    cs.connect(server_binding)
    
    # Receive data from the RS server
    data_rs = cs.recv(200).decode('utf-8')
    print(data_rs)

    # Send data to the RS server
    hns_file = open('PROJ2-HNS.txt','r')
    lines = hns_file.readlines()
    hns_file.close()
    res_file = open('RESOLVED.txt','w')

    for line in lines:
        cs.send(line.strip().encode('utf-8'))
        resolved = cs.recv(200).decode('utf-8')
        res_file.write(resolved)
    
    # close the client socket
    cs.send("q".encode('utf-8'))
    cs.close()
    print("Done.") 
    exit()

if __name__ == "__main__":
    rsHostname = sys.argv[1]
    rsListenPort = int(sys.argv[2])
    client_args = [rsHostname, rsListenPort]

    t2 = threading.Thread(name='client', target=client, args=(client_args))
    t2.start()