import threading
import socket

def ts2():
    try:
        ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS2]: TS2 socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50014)
    ts2.bind(server_binding)
    ts2.listen(1)
    host = socket.gethostname()
    print("[TS2]: TS2 host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[TS2]: TS2 IP addrets2 is {}".format(localhost_ip))
    csockid, addr = ts2.accept()
    print ("[TS2]: Got a connection request from a client at {}".format(addr))

    # Open DNS file  
    dns = open('PROJ2-DNSTS2.txt','r')
    lines = dns.readlines()
    dns.close()
    dns_dict = {}
    for line in lines:
        v = line.strip() + " IN"
        k = line.strip().split()[0].lower()
        dns_dict[k] = v.strip()
    
    # recive queries from the client
    while True:
        try:
            data_client=csockid.recv(200).decode('utf-8')
            if (data_client == "q"):
                print("[TS2]: TS2 Timed Out")
                break
            response = dns_dict[data_client.lower()]
            csockid.send(response.encode('utf-8'))
        except KeyError as err:
            print("No match found! {}".format(data_client))


    # Close the TS2 socket
    ts2.close()
    print("Done.")
    exit()
    
if __name__ == "__main__":
    t1 = threading.Thread(name='ts2', target=ts2)
    t1.start()