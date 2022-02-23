import threading
import socket

def ts1():
    try:
        ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS1]: TS1 socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50007)
    ts1.bind(server_binding)
    ts1.listen(1)
    host = socket.gethostname()
    print("[TS1]: TS1 host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[TS1]: TS1 IP addrets1 is {}".format(localhost_ip))
    csockid, addr = ts1.accept()
    print ("[TS1]: Got a connection request from a client at {}".format(addr))

    # Open DNS file
    dns = open('PROJ2-DNSTS1.txt','r')
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
                print("[TS1]: TS1 Timed Out")
                break
            response = dns_dict[data_client.lower()]
            csockid.send(response.encode('utf-8'))
        except KeyError as err:
            print("No match found! {}".format(data_client))


    # Close the TS1 socket
    ts1.close()
    print("Done.")
    exit()
    
if __name__ == "__main__":
    t1 = threading.Thread(name='ts1', target=ts1)
    t1.start()