from ast import Lambda
from textwrap import fill
import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
import sqlite3
from tkinter import messagebox

class BankingController(tk.Tk):

    def __init__(self):
        super().__init__()      
        self.geometry("1600x1000")
        self.resizable(False, False)

        uniqueID = 0

        conn = sqlite3.connect("bankingAccounts.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS bankingInfo (userName text, password text, accountType text, balance real)")
        c.execute("SELECT *,oid FROM bankingInfo")
        records =c.fetchall()
        print(records)
        conn.commit()
        conn.close()

        #Create the Container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Empty dictionary to hold all frame and frame object pairings
        self.frames = {}

        #Iterate through all frames

        for F in (LoginPage, CreateAnAccount, HomePage, DepositPage, WithdrawPage, TransferPage, AccountDetails):

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

    def validateEntry(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if text:            
            try:
                if text == "." or float(text):
                    return True
            except ValueError:
                return False
        else:
            return False

    def validInfo(self, userN, passwrd):
        if(userN == "" or passwrd == ""):
            messagebox.showinfo(title="Error", message="Please fill all fields")
            return False
        conn = sqlite3.connect("bankingAccounts.db")
        c = conn.cursor()
        c.execute("SELECT *,oid FROM bankingInfo")
        records =c.fetchall()
        for record in records:
            if (userN == str(record[0])):
                conn.commit()
                conn.close()
                messagebox.showinfo(title="Error", message="Please try a different UserName")
                return False
        conn.commit()
        conn.close()       
        return True

    def dbCreateAccount (self, userN, passwrd, accType):
        if(self.validInfo(userN, passwrd)):
            conn = sqlite3.connect("bankingAccounts.db")
            c = conn.cursor()
            c.execute("INSERT INTO bankingInfo VALUES (:userN, :passwrd, :accType, :bal)",
                        {
                            'userN': userN,
                            'passwrd': passwrd,
                            'accType': accType,
                            'bal':0                     
                        })           
            conn.commit()

            c.execute("SELECT oid FROM bankingInfo WHERE userName =?", (userN,))
            records =c.fetchall()
            print(records[0])
            conn.close()
            self.show_frame("HomePage")

    def loginCredentials(self, userN, passwrd):
        conn = sqlite3.connect("bankingAccounts.db")
        c = conn.cursor()
        c.execute("SELECT oid FROM bankingInfo WHERE userName = ? AND password=? ", (userN, passwrd))
        records =c.fetchall()
        print(records)
        if (len(records) == 0):
            conn.close()
            return False
        conn.close()
        return True

    def dbLogin (self, userN, passwrd):
        if(self.loginCredentials(userN, passwrd)):
            print(userN, passwrd)
            self.show_frame("HomePage")
 
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
        
        LoginButton = tk.Button(self, text="Login", width=20,font=("Times New Roman",16),borderwidth=3, relief="solid",bg="#016846", command=lambda:controller.dbLogin(usernameTextbox.get(),passwordTextbox.get()))

        LoginButton.pack(side = RIGHT,padx=(0,500),pady=(10,350))
        

class CreateAnAccount(tk.Frame):

    def __init__(self, cont, controller):
        tk.Frame.__init__(self, cont, bg="white")
        titleLabel = tk.Label(self, text="Money Safe", height=2, font=("Times New Roman",64),borderwidth=3, relief="solid",bg="#016846", fg="white")
        titleLabel.pack(side="top", fill= "x")

        usernameTextbox = tk.Entry(self, justify=CENTER, width=60, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        #usernameTextbox.insert(INSERT, "Username")
        usernameTextbox.pack(side="top", pady=(250,25))

        passwordTextbox = tk.Entry(self, justify=CENTER, width=60, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        #passwordTextbox.insert(INSERT, "Password")
        passwordTextbox.pack(side="top")

        OPTIONS=["Personal","Business"]
        variable = StringVar(self)
        variable.set(OPTIONS[0]) # default value

        w = OptionMenu(self, variable, *OPTIONS)
        w.config(justify=CENTER, width=40, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        w.pack(side ="top", pady=25, padx=(15,0))

        createAnAccountButton = tk.Button(self, text="Create Account", width=20, font=("Times New Roman",16),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.dbCreateAccount(usernameTextbox.get(),passwordTextbox.get(),variable.get()))
        createAnAccountButton.pack(side= "top",pady=(15,0))

class HomePage(tk.Frame):

    def __init__(self, cont, controller):        
        tk.Frame.__init__(self, cont, bg="white")
        titleLabel = tk.Label(self, text="Money Safe", height=2, font=("Times New Roman",64),borderwidth=3, relief="solid",bg="#016846", fg="white")
        titleLabel.pack(side="top", fill= "x")

        AccountButton = tk.Button(self, text="Account", width=20, font=("Times New Roman",32),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.show_frame("CreateAnAccount"))
        AccountButton.pack(side= "top",padx=(0,700),pady=(75,0))

        DepositButton = tk.Button(self, text="Deposit", width=20, font=("Times New Roman",32),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.show_frame("DepositPage"))
        DepositButton.pack(side= "top",padx=(0,700), pady=(100,0))

        WithdrawButton = tk.Button(self, text="Withdraw", width=20, font=("Times New Roman",32),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.show_frame("WithdrawPage"))
        WithdrawButton.pack(side= "top",padx=(0,700), pady=(100,0))

        TransferButton = tk.Button(self, text="Transfer", width=20, font=("Times New Roman",32),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.show_frame("CreateAnAccount"))
        TransferButton.pack(side= "left",padx=(200,0), pady=(50,0))

        backButton = tk.Button(self, text="Back", width=20, font=("Times New Roman",32),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.show_frame("CreateAnAccount"))
        backButton.pack(side= "left",padx=(350,0), pady=(50,0))

class DepositPage(tk.Frame):

    def __init__(self, cont, controller):        
        tk.Frame.__init__(self, cont, bg="white")
        titleLabel = tk.Label(self, text="Money Safe", height=2, font=("Times New Roman",64),borderwidth=3, relief="solid",bg="#016846", fg="white")
        titleLabel.pack(side="top", fill= "x")

        vcmd = (self.register(controller.validateEntry),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        depositTextbox = tk.Entry(self, justify=CENTER, width=60, font=("Times New Roman",24),
                                  borderwidth=3, relief="solid",bg="#016846", fg="white", validate="key", validatecommand=vcmd)    
        depositTextbox.pack(side="top", pady=(100,0))
        depositButton = tk.Button(self, text="Deposit Amount", width=20, font=("Times New Roman",32),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.show_frame("CreateAnAccount"))
        depositButton.pack(side= "top", pady=(50,0))

class WithdrawPage(tk.Frame):

    def __init__(self, cont, controller):        
        tk.Frame.__init__(self, cont, bg="white")
        titleLabel = tk.Label(self, text="Money Safe", height=2, font=("Times New Roman",64),borderwidth=3, relief="solid",bg="#016846", fg="white")
        titleLabel.pack(side="top", fill= "x")

        vcmd = (self.register(controller.validateEntry),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        withdrawTextbox = tk.Entry(self, justify=CENTER, width=60, font=("Times New Roman",24),
                                  borderwidth=3, relief="solid",bg="#016846", fg="white", validate="key", validatecommand=vcmd)    
        withdrawTextbox.pack(side="top", pady=(100,0))
        withdrawButton = tk.Button(self, text="Withdraw Amount", width=20, font=("Times New Roman",32),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.show_frame("CreateAnAccount"))
        withdrawButton.pack(side= "top", pady=(50,0))


    

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

class AccountDetails(tk.Frame):

    def __init__(self, cont, controller):
        tk.Frame.__init__(self, cont, bg="white")
        titleLabel = tk.Label(self, text="Money Safe", height=2, font=("Times New Roman",64),borderwidth=3, relief="solid",bg="#016846", fg="white")
        titleLabel.pack(side="top", fill="x")

        accountList = ("option 1", "option 2", "option 3")
        self.v = tk.StringVar()
        self.v.set(accountList[0])
        selectBox = tk.OptionMenu(self, self.v, *accountList)
        selectBox.config(justify=CENTER, width=40, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        selectBox["menu"].config(font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        selectBox.pack(side="left", pady=(0, 500), padx=(50, 0))

        titleLabel = tk.Label(self, text="ACCOUNT DETAILS", height=2, font=("Times New Roman",64),borderwidth=3, relief="solid",bg="#016846", fg="white")
        titleLabel.pack(side="right", fill="y")


if __name__ == "__main__":
    app = BankingController()
    app.mainloop()