# sutic-chatapp

This project has been written for the final project, some features:

* Designed by all the software design principles.
* Simple and colorful UI + easy to use
* Group chat
* Sound notification
* Uploading file
* different color for each file format
* Up to 5 parallel connections

## server-side

I have used two python packages 1- socket 2- threading, back-end can quickly transfer all the incoming messages to all other clients with their preferred username.

## Front end

I have used Tkinter and pygame together. it is a 600 x 600 square box with three different type of grids:

* upper grid for username input and joining to the chat
* middle grid for chat messages
* bottom grid for typing messages + send and browse button

You cannot write directly to the chat box and have to type your messages and then click on send.
