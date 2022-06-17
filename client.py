# import required modules
import socket
import threading
from random import choice
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from pygame import mixer


HOST = '192.168.43.23'
PORT = 5700

BARCOLOR = '#14497a'
CHATCOLOR = '#061433'
BUTTONCOLOR = '#1f6eb8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 20)
SMALL_FONT = ("Helvetica", 13)

# Creating a socket object
# AF_INET: we are going to use IPv4 addresses
# SOCK_STREAM: we are using TCP packets for communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

mixer.init()
# print("\033[44;33mHello World!\033[m")


def play(st='message'):

    if st == 'message':

        messageNotif = mixer.Sound('effect.wav')
        messageNotif.play()
    else:
        joinNotif = mixer.Sound('welcome.wav')
        joinNotif.play()


tempDic = {'mp3': 'red', 'wav': 'red', 'pdf': 'blue', "jpeg": "green", 'jpg': 'green',
           'png': 'pink', 'docx': 'purple', 'mkv': 'gray', 'mp4': 'gray'}


def add_message(message, format=''):
    message_box.config(state=tk.NORMAL)
    if format != '':
        message_box.tag_configure(
            format, background=tempDic[format], foreground="white")
        message_box.insert(tk.END, message + '\n', format)
        play()
    else:
        message_box.insert(tk.END, message + '\n')
        play()
        message_box.config(state=tk.DISABLED)


def connect():

    # try except block
    try:

        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        play(st='welcome')
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server",
                             f"Unable to connect to server {HOST} {PORT}")

    username = usernameTextbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server,
                     args=(client, )).start()

    usernameTextbox.config(state=tk.DISABLED)
    usernameButton.config(state=tk.DISABLED)


def send_message(event=''):
    message = messageTextbox.get()
    if message != '':
        client.sendall(message.encode())
        messageTextbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")


root = tk.Tk()
root.geometry("600x600")
root.title("Chat App")
root.resizable(False, False)
icon = tk.PhotoImage(file='icon.png')
root.iconphoto(False, icon)


root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

topFrame = tk.Frame(root, width=600, height=100, bg=BARCOLOR)
topFrame.grid(row=0, column=0, sticky=tk.NSEW)

middleFrame = tk.Frame(root, width=600, height=400, bg=CHATCOLOR)
middleFrame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=BARCOLOR)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

usernameLabel = tk.Label(
    topFrame, text="Enter username:", font=FONT, bg=BARCOLOR, fg=WHITE)
usernameLabel.pack(side=tk.LEFT, padx=10)

usernameTextbox = tk.Entry(
    topFrame, font=FONT, bg=CHATCOLOR, fg=WHITE, width=23)
usernameTextbox.pack(side=tk.LEFT)

usernameButton = tk.Button(
    topFrame, text="Join", font=BUTTON_FONT, bg=BUTTONCOLOR, fg=WHITE, command=connect)
usernameButton.pack(side=tk.LEFT, padx=15)

messageTextbox = tk.Entry(bottom_frame, font=FONT,
                           bg=CHATCOLOR, fg=WHITE, width=25)
messageTextbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT,
                           bg=BUTTONCOLOR, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)
message_button.bind_all("<Return>", send_message)

message_box = scrolledtext.ScrolledText(
    middleFrame, font=SMALL_FONT, bg=CHATCOLOR, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)
# message_box.tag_config('user', foreground='red')


def browsefunc():
    filename = filedialog.askopenfilename()
    username = usernameTextbox.get()
    formatt = filename.split('.')[1]
    add_message(f"[{username}] {filename}", format=formatt)


browsebutton = tk.Button(bottom_frame, text="Browse", font=BUTTON_FONT,
                         bg=BUTTONCOLOR, fg=WHITE, command=browsefunc)
browsebutton.pack()


def listen_for_messages_from_server(client):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")
            print(f"[{username}] {content}")

        else:
            messagebox.showerror(
                "Error", "Message recevied from client is empty")

# main function


def main():

    root.mainloop()


if __name__ == '__main__':
    main()
