import socket
import threading


# Two constant variable for host and port number
HOST = '192.168.1.4'
PORT = 5700
FORMAT = 'utf-8'
LIMIT = 5
clientsList = []


def MSGlistener(client, userName):
    while True:

        tempMSG = client.recv(2048).decode(FORMAT)

        if not tempMSG:
            print(f'the msg from User {userName} is empty!')
            
        elif '~' in tempMSG:
            MSG ='file'  +'~' + tempMSG
            MSGsenderAll(MSG)

        else:
            MSG = userName + '~' + tempMSG
            MSGsenderAll(MSG)


def MSGsenderSolo(client, MSG):

    client.sendall(MSG.encode())


def MSGsenderAll(MSG):

    for user in clientsList:

        MSGsenderSolo(user[1], MSG)


def clientHandlere(client):

    while True:
        userName = client.recv(2048).decode(FORMAT)

        if not userName:
            print('username is empty!')
        else:
            clientsList.append((userName, client))
            prompt_message = "SERVER~" + f"{userName} added to the chat"
            MSGsenderAll(prompt_message)
            break

    threading.Thread(target=MSGlistener, args=(client, userName)).start()


def main():

    # using IPV4 address family and TCP sockets
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # assignig our socket to our HOST and PORT
        serverSock.bind((HOST, PORT))
        print('server is running!')
    except:
        print(
            f'some error occured when assigning {PORT} or {HOST} to our socket!')

    serverSock.listen(LIMIT)

    while True:

        # Wait for an incoming connection. Return a new socket representing the connection, and the address of the client. For IP sockets, the address info is a pair (hostaddr, port).
        client, address = serverSock.accept()
        print(f'Client {address[0]} has been connected with port {address[1]}')

        threading.Thread(target=clientHandlere, args=(client, )).start()


if __name__ == '__main__':
    main()







