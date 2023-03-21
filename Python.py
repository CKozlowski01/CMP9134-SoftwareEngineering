from textwrap import fill
import tkinter as tk
from tkinter import font as tkfont
from tkinter import *

class BankingController(tk.Tk):

    def __init__(self):
        super().__init__()      
        self.geometry("1600x1000")
        self.resizable(False, False)

        #Create the Container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Empty dictionary to hold all frame and frame object pairings
        self.frames = {}

        #Iterate through all frames
        for F in (LoginPage, CreateAnAccount, HomePage, TransferPage):
            #Find frame name
            page_name = F.__name__

            #Fulfil frame arguments with the container above and the pass this class so frames can use defining functions
            frame = F(cont=container, controller=self)

            #Add to the dictionary
            self.frames[page_name] = frame

            #Stack all frames in the same position, the last stacked will appear at the top unless changed
            frame.grid(row=0, column=0, sticky="nsew")

        #Show the first frame
        self.show_frame("LoginPage")

    #Function to change frame
    def show_frame(self, frame):
        frameobj = self.frames[frame]
        frameobj.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, cont, controller):
        tk.Frame.__init__(self, cont, bg="white")
        titleLabel = tk.Label(self, text="Money Safe", height=2, font=("Times New Roman",64),borderwidth=3, relief="solid",bg="#016846")
        titleLabel.pack(side="top", fill= "x")

        usernameTextbox = tk.Entry(self, justify=CENTER, width=60, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846")
        usernameTextbox.insert(INSERT, "Username")
        usernameTextbox.pack(side="top", pady=(250,25))

        passwordTextbox = tk.Entry(self, justify=CENTER, width=60, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846")
        passwordTextbox.insert(INSERT, "Password")
        passwordTextbox.pack(side="top")

        createAnAccountButton = tk.Button(self, text="Create Account", width=20, font=("Times New Roman",16),borderwidth=3, relief="solid",bg="#016846")
        createAnAccountButton.pack(side= LEFT,padx= (500,0),pady=(10,350))

        LoginButton = tk.Button(self, text="Login", width=20,font=("Times New Roman",16),borderwidth=3, relief="solid",bg="#016846")
        LoginButton.pack(side = RIGHT,padx=(0,500),pady=(10,350))
        

class CreateAnAccount(tk.Frame):

    def __init__(self, cont, controller):
        tk.Frame.__init__(self, cont)


class HomePage(tk.Frame):

    def __init__(self, cont, controller):
        tk.Frame.__init__(self, cont)

class TransferPage(tk.Frame):

    def __init__(self, cont, controller):
        tk.Frame.__init__(self, cont, bg="white")
        titleLabel = tk.Label(self, text="Money Safe", height=2, font=("Times New Roman",64),borderwidth=3, relief="solid",bg="#016846", fg="white")
        titleLabel.pack(side="top", fill="x")

        accountList = ("option 1", "option 2", "option 3")
        self.v = tk.StringVar()
        self.v.set(accountList[0])
        selectBox = tk.OptionMenu(self, self.v, *accountList)
        selectBox.config(justify=CENTER, width=60, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        selectBox["menu"].config(font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        selectBox.pack(side="top", pady=(100, 10))

        backBtn = tk.Button(self, text="Back", width=10, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        backBtn.pack(side="bottom", pady=(0,50), padx=(0, 1000))

        transferBtn = tk.Button(self, text="Transfer", width=40, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        transferBtn.pack(side="bottom", pady=(0, 100))

        transferTextbox = tk.Entry(self, justify=CENTER, width=20, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        transferTextbox.insert(INSERT, "Transfer Amount")
        transferTextbox.pack(side="left", padx=(300, 0), pady=(0, 100))

        transferAccTextbox = tk.Entry(self, justify=CENTER, width=20, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        transferAccTextbox.insert(INSERT, "Recievers Username")
        transferAccTextbox.pack(side="right", padx=(0, 300), pady=(0, 100))

        
        # usernameTextbox = tk.Entry(self, justify=CENTER, width=60, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846")
        # usernameTextbox.insert(INSERT, "Username")
        # usernameTextbox.pack(side="top", pady=(250,25))

        # selection = tk.StringVar()
        # selectBox = ttk.Combobox(self, text="Select Account", textvariable=selection, values = ["option 1", "option 2", "option 3"], justify=CENTER, width=60, font=("Times New Roman",24))
        # selectBox.pack(side="top", pady="100")


if __name__ == "__main__":
    app = BankingController()
    app.mainloop()