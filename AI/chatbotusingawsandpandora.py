from tkinter import*

def send():
    user_message = e.get()
    text.insert(END, "\nYou: " + user_message)

    if user_message.lower() == 'hi':
        text.insert(END, "\nBot: hello!")
    elif user_message.lower() == 'hello':
        text.insert(END, "\nBot: hi!")
    elif user_message.lower() == 'how are you?':
        text.insert(END, "\nBot: I'm fine, thank you! And you?")
    elif user_message.lower() == 'i am fine':
        text.insert(END, "\nBot: Good to hear that!")
    else:
        text.insert(END, "\nBot: Sorry, I didn't understand that.")

root = Tk()
root.title('Simple Python Chatbot')

text = Text(root, bg='light yellow', width=50, height=20)
text.grid(row=0, column=0, columnspan=2)

e = Entry(root, width=50)
e.grid(row=1, column=0)

send_btn = Button(root, text='Send', bg='blue', fg='white', width=20, command=send)
send_btn.grid(row=1, column=1)

root.mainloop()