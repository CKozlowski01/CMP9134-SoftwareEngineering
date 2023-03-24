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

        self.uniqueID = 0
        self.currentUserName=""
        self.accountList = []
        self.OPTIONS=["Personal","Business"]

        conn = sqlite3.connect("bankingAccounts.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS bankingInfo (userName text, password text, accountType text, balance real)")
        c.execute("SELECT *,oid FROM bankingInfo")
        records =c.fetchall()
        print(records)
        conn.commit()
        conn.close()

        #Create the Container
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        #Empty dictionary to hold all frame and frame object pairings
        self.frames = {}

        #Iterate through some frames

        for F in (LoginPage, CreateAnAccount, HomePage):

            #Find frame name
            page_name = F.__name__

            #Fulfil frame arguments with the container above and the pass this class so frames can use defining functions
            frame = F(cont=self.container, controller=self)

            #Add to the dictionary
            self.frames[page_name] = frame

            #Stack all frames in the same position, the last stacked will appear at the top unless changed
            frame.grid(row=0, column=0, sticky="nsew")

        #Show the first frame
        self.showFrame("LoginPage")

    #Function to change frame
    def showFrame(self, f):
        #Check if the frame is the HomePage
        if (f == "HomePage"):
            #Clear the accountList array if is already has something in it
            self.accountList = []

            #Run the function to populate the accountList array for use in other Frame
            self.populateAccountList()

            #Run through the Frames that include an optionMenu widget
            for F in (DepositPage, WithdrawPage, TransferPage, AccountDetails, AddAccount):
                #Find frame name
                page_name = F.__name__

                #Fulfil frame arguments with the container above and the pass this class so frames can use defining functions
                frame = F(cont=self.container, controller=self)

                #Add to the dictionary
                self.frames[page_name] = frame

                #Stack all frames in the same position, the last stacked will appear at the top unless changed
                frame.grid(row=0, column=0, sticky="nsew")

        #Show the frequested Frame
        frameobj = self.frames[f]
        frameobj.tkraise()
    
    #Function to test if the text inside of an entry box is a number of decimal number
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
    
    #Check new account details
    def validInfo(self, userN, passwrd):
        #Check if any of the input boxes are empty
        if(userN == "" or passwrd == ""):
            messagebox.showinfo(title="Error", message="Please fill all fields")
            return False

        #Connect to database
        conn = sqlite3.connect("bankingAccounts.db")
        c = conn.cursor()
        c.execute("SELECT *,oid FROM bankingInfo")

        #Fetch all query results
        records =c.fetchall()

        #Iterate through all results
        for record in records:
            #Check if the given username is already in the database, if so return error
            if (userN == str(record[0])):
                conn.commit()
                conn.close()
                messagebox.showinfo(title="Error", message="Please try a different UserName")
                return False
        conn.commit()
        conn.close()       
        return True

    #Create an Account
    def dbCreateAccount (self, userN, passwrd, accType):
        #Test the return state of the function
        if(self.validInfo(userN, passwrd)):
            #Open the database
            conn = sqlite3.connect("bankingAccounts.db")
            c = conn.cursor()
            #Include a new entry
            c.execute("INSERT INTO bankingInfo VALUES (:userN, :passwrd, :accType, :bal)",
                        {
                            'userN': userN,
                            'passwrd': passwrd,
                            'accType': accType,
                            'bal':4                   
                        })           
            conn.commit()

            #Find the unique ID for the newly created account
            c.execute("SELECT *,oid FROM bankingInfo WHERE userName =?", (userN,))
            records =c.fetchall()
            record = records[0]

            #Store details for later use
            self.uniqueID = record[4]
            self.currentUserName = record[0]            
            conn.close()

            self.showFrame("HomePage")

    #Check login credentials
    def loginCredentials(self, userN, passwrd):
        #Open database
        conn = sqlite3.connect("bankingAccounts.db")
        c = conn.cursor()
        #Search for matching username and password
        c.execute("SELECT *,oid FROM bankingInfo WHERE userName = ? AND password=? ", (userN, passwrd))
        records =c.fetchall()
        #If there are not matching the length will be 0
        if (len(records) == 0):
            #Return error
            conn.close()
            return False

        #Store the information for later use
        record = records[0]
        self.uniqueID = record[4]
        self.currentUserName = record[0]        
        conn.close()
        return True
    #Login
    def dbLogin (self, userN, passwrd):
        #Check return state
        if(self.loginCredentials(userN, passwrd)):
            #Move past login
            self.showFrame("HomePage")

    #Populate the account list 
    def populateAccountList (self):
        #Connect to DB
        conn = sqlite3.connect("bankingAccounts.db")
        c = conn.cursor()
        #Find all accounts related to username
        c.execute("SELECT *,oid FROM bankingInfo WHERE userName = ?", (self.currentUserName,))
        records =c.fetchall()
        #Create data arrays for each of the them and store inside of list
        for record in records:
            data = "%s, %s, %s, %s, %s" % (record[0], record[1],record[2],record[3],record[4])
            self.accountList.append(data)
        
    #Transfer Function
    def transferMoney(self, userInfo, transferMoney, transferReceiver):
        #Test if the user has selected a valid option
        try:
            userID = userInfo.split(",",4)[4] 
        except:
            return False
        #Connect to DB
        conn = sqlite3.connect("bankingAccounts.db")
        c = conn.cursor()

        #Find information related to sender
        c.execute("SELECT *,oid FROM bankingInfo WHERE oid = ?", (userID,))
        records =c.fetchall()
        record = records[0]

        #Focus on the sender balance
        senderBal = record[3]

        #Convert balance and amount requested to send to float
        senderBal = float(senderBal)
        transferMoney = float(transferMoney)

        #Test if sender has available funds
        if (senderBal<transferMoney):
            return False

        #Find information related to the receiver
        c.execute("SELECT *,oid FROM bankingInfo WHERE oid = ?", (transferReceiver,))
        records =c.fetchall()        
        #Test if the receiver exists
        try:
            record = records[0]
            receiverBal = record[3]
        except:
            return False
        #Conver receiver bal to float
        receiverBal = float(receiverBal)
        #Find new balanced for both parties
        newReceiverBal = receiverBal + transferMoney
        newSenderBal = senderBal - transferMoney
        
        #Update the table with new balances
        c.execute("UPDATE bankingInfo SET balance=? WHERE oid =?",(newSenderBal,userID))
        c.execute("UPDATE bankingInfo SET balance=? WHERE oid =?",(newReceiverBal, transferReceiver))
        conn.commit()
        conn.close()

        #Move to home page
        self.showFrame("HomePage")
    
    def addAccount(self, variable):
        conn = sqlite3.connect("bankingAccounts.db")
        c = conn.cursor()
        c.execute("INSERT INTO bankingInfo VALUES (:userN, :passwrd, :accType, :bal)",
                    {
                        'userN': self.currentUserName,
                        'passwrd': "",
                        'accType': variable,
                        'bal':0                     
                    })           
        conn.commit()

    def depositMoney(self, userInfo, depositAmount):
        #Test if the user has selected a valid option
        try:
            userID = userInfo.split(",",4)[4] 
        except:
            return False

        #Connect to DB
        conn = sqlite3.connect("bankingAccounts.db")
        c = conn.cursor()

        #Find information related to sender
        c.execute("SELECT *,oid FROM bankingInfo WHERE oid = ?", (userID,))
        records =c.fetchall()
        record = records[0]

        #Focus on the sender balance
        senderBal = record[3]

        #Convert balance and amount requested to send to float
        senderBal = float(senderBal)
        depositAmount = float(depositAmount)
        newBalance = senderBal + depositAmount

        #Update the table with new balances
        c.execute("UPDATE bankingInfo SET balance=? WHERE oid =?",(newBalance,userID))
        conn.commit()
        conn.close()
        self.showFrame("HomePage")

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

        createAnAccountButton = tk.Button(self, text="Create Account", width=20, font=("Times New Roman",16),borderwidth=3, relief="solid",bg="#016846", command=lambda:controller.showFrame("CreateAnAccount"))
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

        
        variable = StringVar(self)
        variable.set(controller.OPTIONS[0]) # default value

        w = OptionMenu(self, variable, *controller.OPTIONS)
        w.config(justify=CENTER, width=40, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        w.pack(side ="top", pady=25, padx=(15,0))

        createAnAccountButton = tk.Button(self, text="Create Account", width=20, font=("Times New Roman",16),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.dbCreateAccount(usernameTextbox.get(),passwordTextbox.get(),variable.get()))
        createAnAccountButton.pack(side= "top",pady=(15,0))

class HomePage(tk.Frame):

    def __init__(self, cont, controller):        
        tk.Frame.__init__(self, cont, bg="white")
        titleLabel = tk.Label(self, text="Money Safe", height=2, font=("Times New Roman",64),borderwidth=3, relief="solid",bg="#016846", fg="white")
        titleLabel.pack(side="top", fill= "x")

        AccountButton = tk.Button(self, text="Account", width=20, font=("Times New Roman",32),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.showFrame("AccountDetails"))
        AccountButton.pack(side= "top",padx=(0,700),pady=(75,0))

        DepositButton = tk.Button(self, text="Deposit", width=20, font=("Times New Roman",32),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.showFrame("DepositPage"))
        DepositButton.pack(side= "top",padx=(0,700), pady=(50,0))

        WithdrawButton = tk.Button(self, text="Withdraw", width=20, font=("Times New Roman",32),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.showFrame("WithdrawPage"))
        WithdrawButton.pack(side= "top",padx=(0,700), pady=(50,0))

        TransferButton = tk.Button(self, text="Transfer", width=20, font=("Times New Roman",32),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.showFrame("TransferPage"))
        TransferButton.pack(side= "top",padx=(0,700), pady=(50,0))
        
        TransferButton = tk.Button(self, text="New Account", width=20, font=("Times New Roman",32),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.showFrame("AddAccount"))
        TransferButton.pack(side= "left",padx=(205,0), pady=(0,35))

        backButton = tk.Button(self, text="Back", width=20, font=("Times New Roman",32),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.showFrame("CreateAnAccount"))
        backButton.pack(side= "right",padx=(0,50), pady=(50,0))

class DepositPage(tk.Frame):

    def __init__(self, cont, controller):        
        tk.Frame.__init__(self, cont, bg="white")
        titleLabel = tk.Label(self, text="Money Safe", height=2, font=("Times New Roman",64),borderwidth=3, relief="solid",bg="#016846", fg="white")
        titleLabel.pack(side="top", fill= "x")

        variable = tk.StringVar()
        variable.set("Select Option")
        
        selectBox = tk.OptionMenu(self, variable, *controller.accountList)
        selectBox.config(justify=CENTER, width=60, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        selectBox["menu"].config(font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        selectBox.pack(side="top", pady=(100, 10))

        vcmd = (self.register(controller.validateEntry),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        depositTextbox = tk.Entry(self, justify=CENTER, width=60, font=("Times New Roman",24),
                                  borderwidth=3, relief="solid",bg="#016846", fg="white", validate="key", validatecommand=vcmd)    
        depositTextbox.pack(side="top", pady=(100,0))
        depositButton = tk.Button(self, text="Deposit Amount", width=20, font=("Times New Roman",32),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.depositMoney(variable.get(),depositTextbox.get()))
        depositButton.pack(side= "top", pady=(50,0))

class WithdrawPage(tk.Frame):

    def __init__(self, cont, controller):        
        tk.Frame.__init__(self, cont, bg="white")
        titleLabel = tk.Label(self, text="Money Safe", height=2, font=("Times New Roman",64),borderwidth=3, relief="solid",bg="#016846", fg="white")
        titleLabel.pack(side="top", fill= "x")

        variable = tk.StringVar()
        variable.set("Select Option")
        
        selectBox = tk.OptionMenu(self, variable, *controller.accountList)
        selectBox.config(justify=CENTER, width=60, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        selectBox["menu"].config(font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        selectBox.pack(side="top", pady=(100, 10))

        vcmd = (self.register(controller.validateEntry),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        withdrawTextbox = tk.Entry(self, justify=CENTER, width=60, font=("Times New Roman",24),
                                  borderwidth=3, relief="solid",bg="#016846", fg="white", validate="key", validatecommand=vcmd)    
        withdrawTextbox.pack(side="top", pady=(100,0))
        withdrawButton = tk.Button(self, text="Withdraw Amount", width=20, font=("Times New Roman",32),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.showFrame("CreateAnAccount"))
        withdrawButton.pack(side= "top", pady=(50,0))

class TransferPage(tk.Frame):

    def __init__(self, cont, controller):
        tk.Frame.__init__(self, cont, bg="white")
        titleLabel = tk.Label(self, text="Money Safe", height=2, font=("Times New Roman",64),borderwidth=3, relief="solid",bg="#016846", fg="white")
        titleLabel.pack(side="top", fill="x")
     
        variable = tk.StringVar()
        variable.set("Select Option") 
        
        selectBox = tk.OptionMenu(self, variable, *controller.accountList)
        selectBox.config(justify=CENTER, width=60, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        selectBox["menu"].config(font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        selectBox.pack(side="top", pady=(100, 10))

        backBtn = tk.Button(self, text="Back", width=10, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.showFrame("HomePage"))
        backBtn.pack(side="bottom", pady=(0,50), padx=(0, 1000))

        transferTextbox = tk.Entry(self, justify=CENTER, width=20, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        transferTextbox.insert(INSERT, "Transfer Amount")
        transferTextbox.pack(side="left", padx=(300, 0), pady=(0, 100))

        transferAccTextbox = tk.Entry(self, justify=CENTER, width=20, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        transferAccTextbox.insert(INSERT, "Recievers Username")
        transferAccTextbox.pack(side="right", padx=(0, 300), pady=(0, 100))

        transferBtn = tk.Button(self, text="Transfer", width=40, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.transferMoney(variable.get(),transferTextbox.get(),transferAccTextbox.get()))
        transferBtn.pack(side="bottom", pady=(0, 100))
     
class AccountDetails(tk.Frame):

    def __init__(self, cont, controller):
        self.test = 0
        tk.Frame.__init__(self, cont, bg="white")
        self.titleLabel = tk.Label(self, text="Money Safe", height=2, font=("Times New Roman",64),borderwidth=3, relief="solid",bg="#016846", fg="white")
        self.titleLabel.pack(side="top", fill="x")
        
        variable = tk.StringVar()
        variable.set("Select Option")

        selectBox = tk.OptionMenu(self, variable, *controller.accountList)
        selectBox.config(justify=CENTER, width=40, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        selectBox["menu"].config(font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        selectBox.pack(side="left", pady=(0, 500), padx=(50, 0))

        titleLabel = tk.Label(self, text="ACCOUNT DETAILS", height=2, font=("Times New Roman",64),borderwidth=3, relief="solid",bg="#016846", fg="white")
        titleLabel.pack(side="right", fill="y")

        controller.after(0, self.refresh(variable))
    def refresh(self, account):
        self.titleLabel.configure(textvariable=account)
        self.update()
            
        

class AddAccount(tk.Frame):

    def __init__(self, cont, controller):
        tk.Frame.__init__(self, cont, bg="white")
        titleLabel = tk.Label(self, text="Money Safe", height=2, font=("Times New Roman",64),borderwidth=3, relief="solid",bg="#016846", fg="white")
        titleLabel.pack(side="top", fill="x")
      
        variable = StringVar(self)
        variable.set(controller.OPTIONS[0])

        selectBox= OptionMenu(self, variable, *controller.OPTIONS)
        selectBox.config(justify=CENTER, width=40, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white")
        selectBox.pack(side ="top", pady=(50,0), padx=(15,0))

        backBtn = tk.Button(self, text="Back", width=10, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.showFrame("HomePage"))
        backBtn.pack(side="bottom", pady=(0,50), padx=(0, 1000))

        addAccountBtn = tk.Button(self, text="Add Account", width=40, font=("Times New Roman",24),borderwidth=3, relief="solid",bg="#016846", fg="white", command=lambda:controller.addAccount(variable.get()))
        addAccountBtn.pack(side="bottom", pady=(0, 100))

if __name__ == "__main__":
    app = BankingController()
    app.mainloop()