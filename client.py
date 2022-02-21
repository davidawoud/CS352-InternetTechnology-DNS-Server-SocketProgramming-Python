import threading
import time
import random
import select
import socket
import errno

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = 50021
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)
    cs.setblocking(0)
    
    # Receive data from the server
    
    inputs = [cs]
    outputs = [cs]

    while inputs:
        try:
            data_rs = cs.recv(200).decode('utf-8')
            cs.send("Welcome to CS".encode('utf-8'))
            cs.send("Welcome to CS try once".encode('utf-8'))
            cs.send("Welcome to CS try twice".encode('utf-8'))
        except socket.error as e:
            if e.errno != errno.EAGAIN:
                raise e
            select.select(inputs, outputs, inputs,30)

    """
    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs, 120)

        for s in readable:
            data_rs = s.recv(200).decode('utf-8')
            #print(data_rs)
            inputs.remove(s)
            break
        for s in writable:
            s.send("Welcome to CS".encode('utf-8'))
            s.send("Welcome to CS try once".encode('utf-8'))
            s.send("Welcome to CS try twice".encode('utf-8'))
            outputs.remove(s)
            break
        for s in exceptional:
            pass
            break
    """

    
    # close the client socket
    cs.close()
    print("Done.") 
    exit()

if __name__ == "__main__":
    time.sleep(random.random() * 5)
    t2 = threading.Thread(name='client', target=client)
    t2.start()