import socket
import threading
import pickle

server = socket.socket()
port = 12342
server.bind(('',port))
server.listen(20)

client_data = {}
client_data_partial = {}

def find_client_nickname(client):
    for nickname in client_data.keys():
        if client_data[nickname][0] == client:
            return nickname


def communicate(sender_client, message):
    receiver_nickname, encrypted_message = message.split(' ', 1)
    receiver_client = client_data[receiver_nickname.lower()][0]
    sender_client_nickname = find_client_nickname(sender_client)
    updated_message = f"{sender_client_nickname} {encrypted_message}"

    receiver_client.send(updated_message.encode('utf-8'))


def broadcast(message):
    client_data_partial={}
    with open("data.pickle", "rb") as f:
        client_data_partial = pickle.load(f)

    for nickname in client_data_partial.keys():
        try:
            receiver_client = client_data[nickname][0]
            receiver_client.send(message.encode('utf-8'))
        except:
            pass


def handle_client(client):
    client_nickname = find_client_nickname(client)
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            
            if message == 'leave':
                print(f"[{client_nickname.capitalize()} Left the chat]")
                client.close()
                client_data.pop(client_nickname)
                break

            else:
                communicate(client, message)

        except Exception as e:
            client_nickname = find_client_nickname(client)
            print(e)

            announcement = f"server {client_nickname} has left the chat"

            client_data_partial={}

            try:
                with open("data.pickle", "rb") as f:
                    client_data_partial = pickle.load(f)
            except:
                pass

            try:
                broadcast(announcement)
            except:
                print(f"{client_nickname.capitalize()} has left the chat")


            with open("data.pickle", "wb") as f:
                pickle.dump(client_data_partial, f)

            break


def main():
    while True:
        client, client_address = server.accept()
        
        client.send('server 1'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        print(f"[Connected with {nickname.capitalize()} ({client_address})]")
        
        client.send('server 2'.encode('utf-8'))
        public_key = client.recv(1024).decode('utf-8')
        
        client.send('server 3'.encode('utf-8'))
        N = client.recv(1024).decode('utf-8')
        
        client_data[nickname.lower()] = [client, int(public_key), int(N)]
        client_data_partial[nickname.lower()] = [int(public_key), int(N)]

        with open("data.pickle", "wb") as f:
            pickle.dump(client_data_partial, f)

        
        announcement = f"server {nickname.capitalize()} has joined the chat"
        broadcast(announcement)

        client.send("server Connected To Server".encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,) )
        thread.start()



print("[Server is Running]")
main()
