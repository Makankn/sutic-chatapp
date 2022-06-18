# import required modules
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from pygame import mixer

#all the constants that we use are here, for IP, colors and fonts
#you can change color of whole program in a seconde using this varibales
HOST = socket.gethostbyname(socket.gethostname())
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
# SOCK_STREAM: we are using TCP transfer protocol for communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# mixer is a subclass inside pygame packages, we use it to
# play sound on joining and sending message functions
mixer.init()


def play(st='message'):

    if st == 'message':

        messageNotif = mixer.Sound('assets/effect.wav')
        messageNotif.play()
    else:
        joinNotif = mixer.Sound('assets/welcome.wav')
        joinNotif.play()


# Dictionaries are the fastest data structures
formatDic = {'mp3': 'red', 'wav': 'red', 'pdf': 'blue', "jpeg": "green", 'jpg': 'green',
             'png': 'pink', 'docx': 'purple', 'mkv': 'gray', 'mp4': 'gray', 'py':'black'}

#this function will help you to push all the messages into the message box
#in this function we will also config all of our tag and color configs
def add_message(message, format=''):
    message_box.config(state=tk.NORMAL)
    if format != '':
        message_box.tag_configure(
            format, background=formatDic[format], foreground="white")
        message_box.insert(tk.END, message + '\n', format)
        play()
    else:
        message_box.insert(tk.END, message + '\n')
        play()
        message_box.config(state=tk.DISABLED)

#initial function for clinets to join and connect to our server
#execption handling are all over the program
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

#this funtction wil send each indivisual client to our server then server will reply with
#sending the message to all other clients.
def send_message(event='', file=""):
    message = messageTextbox.get()
    if file:
        message = file
        client.sendall(message.encode())
    elif message != '':
        client.sendall(message.encode())
        messageTextbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

#here we will config our UI, width and height and Icon for our app
root = tk.Tk()
root.geometry("600x600")
root.title("Chat App")
root.resizable(False, False)
icon = tk.PhotoImage(file='assets/icon.png')
root.iconphoto(False, icon)

#I have used grid functionality for our UI
#I have splited our GUI window into three diffrent girds
#top 100 height, middle 400 height, bottom 100 height
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

#from here till line 147 I have implemented all the buttons and grids
#and all the lables colors etc.
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
#you may ask why scroll text, in a chat app we need to be able to scroll between
#message if there are moret han our 400 height
message_box = scrolledtext.ScrolledText(
    middleFrame, font=SMALL_FONT, bg=CHATCOLOR, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

#with the help of this function we can simulate uploading a file
#this function will be bind to our Browse button and will let us choose
#a file, after that with the help of add_message func and colorDic we
#can sen our file path and name plus we can assign it a color using colorDic
def browsefunc():
    filename = filedialog.askopenfilename()
    username = usernameTextbox.get()
    formatt = filename.split('.')[1]
    send_message(file=f"{username}~{filename}~{formatt}")


browsebutton = tk.Button(bottom_frame, text="Browse", font=BUTTON_FONT,
                         bg=BUTTONCOLOR, fg=WHITE, command=browsefunc)
browsebutton.pack()

#this fucntion will always listen to messages comming from our server
#we have used thread package to always have this function availbale by our side
#so we can easily say that no matter what happens our server is always on
def listen_for_messages_from_server(client):

    while True:
        message = client.recv(2048).decode('utf-8')
        tempFile = message.split('~')[0]
        if message != '':
            if tempFile == 'file':
                username=message.split('~')[1]
                filePath=message.split('~')[2]
                formatt=message.split('~')[3]
                add_message(f"[{username}] {filePath}", format=formatt)
                
            else:
                username = message.split("~")[0]
                content = message.split('~')[1]
                add_message(f"[{username}] {content}")
                print(f"[{username}] {content}")

        else:
            messagebox.showerror(
                "Error", "Message received from client is empty")

# main function
def main():

    root.mainloop()


if __name__ == '__main__':
    main()
