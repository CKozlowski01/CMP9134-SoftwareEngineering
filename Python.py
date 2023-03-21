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
        for F in (LoginPage, CreateAnAccount, HomePage):
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

        createAnAccountButton = tk.Button(self, text="Create Account", width=20, font=("Times New Roman",16),borderwidth=3, relief="solid",bg="#016846", command=lambda:controller.show_frame("CreateAnAccount"))
        createAnAccountButton.pack(side= LEFT,padx= (500,0),pady=(10,350))

        LoginButton = tk.Button(self, text="Login", width=20,font=("Times New Roman",16),borderwidth=3, relief="solid",bg="#016846")
        LoginButton.pack(side = RIGHT,padx=(0,500),pady=(10,350))
        

class CreateAnAccount(tk.Frame):

    def __init__(self, cont, controller):
        tk.Frame.__init__(self, cont, bg="white")
        titleLabel = tk.Label(self, text="Money Safe", height=2, font=("Times New Roman",64),borderwidth=3, relief="solid",bg="#016846", fg="white")
        titleLabel.pack(side="top", fill= "x")

        usernameTextbox = tk.Entry(self, justify=CENTER, width=60, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        usernameTextbox.insert(INSERT, "Username")
        usernameTextbox.pack(side="top", pady=(250,25))

        passwordTextbox = tk.Entry(self, justify=CENTER, width=60, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        passwordTextbox.insert(INSERT, "Password")
        passwordTextbox.pack(side="top")

        OPTIONS=["Personal","Business"]
        variable = StringVar(self)
        variable.set(OPTIONS[0]) # default value

        w = OptionMenu(self, variable, *OPTIONS)
        w.config(justify=CENTER, width=40, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        w.pack(side ="top", pady=25, padx=(15,0))

        createAnAccountButton = tk.Button(self, text="Create Account", width=20, font=("Times New Roman",16),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.show_frame("CreateAnAccount"))
        createAnAccountButton.pack(side= "top",pady=(15,0))



class HomePage(tk.Frame):

    def __init__(self, cont, controller):
        tk.Frame.__init__(self, cont)

if __name__ == "__main__":
    app = BankingController()
    app.mainloop()