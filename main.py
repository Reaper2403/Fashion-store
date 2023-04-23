from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import mysql.connector

# Connect to the database
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="sqluser",
#     password="password",
#     database="ananya"
# )

# # Connect to the database #Ananya's version
mydb = mysql.connector.connect(
    host="localhost",
    user="sqluser",
    password="password",
    database="ananya"
)



root = Tk()
root.title('LogIn')
root.geometry('925x480')
root.config(bg='#ffffff')
root.resizable(True, True)
root.iconbitmap('send_message_icon_251493.ico')

def signin():
    # Get the username and password entered by the user
    username = user.get()
    password = word.get()

    # Execute the SQL query to check if the user exists in the database
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    result = mycursor.fetchone()

    if result:
        # If the user exists, run the store functionality from store.py
        root.destroy()
        from store import inventory_pages
        inventory_pages()

    else:
        # If the user does not exist, show an error message
        messagebox.showerror('Invalid', 'Invalid Username or Password')

        # If the user wants to register, open the registration window
        if messagebox.askyesno('Register', 'Do you want to register?'):
            root.destroy()
            import register

def on_enter(e):
    # print("lol")
    user.configure(fg="black")
    user.delete(0, 'end')

def on_leave(e):
    name = user.get()
    if name == '':
        user.configure(fg="indigo")
        user.insert(0, 'Username')

img = Image.open('images.png')
img = img.resize((460, 450), Image.LANCZOS)
my_img = ImageTk.PhotoImage(img)
my_label = Label(root, image=my_img).pack(side=LEFT, padx=15, pady=15, fill=X)#.place(x=40, y=50)

Login_frame = Frame(root, width=350, height=350, bg='white')
Login_frame.pack()
# Login_frame.place(x=480, y=70)

heading = Label(Login_frame, text='Sign In'.upper(), fg='blue', bg='white', font='Arimo,60,bold')
heading.pack(side=TOP, fill=X, padx=15, pady=15, ipadx=25, ipady=25)
# heading.place(x=150, y=5)

# user = Entry(Login_frame, width=25, fg='indigo', borderwidth=(0, 0, 0, 2), relief='solid', padx=5, pady=5, ipadx=5, ipady=5)
user = Entry(Login_frame, width=25, fg='indigo', borderwidth=0.5, bg='white', font='Arimo,20')
user.pack(fill=X, padx=15, pady=15, ipadx=5, ipady=10)
# user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

# Frame(Login_frame, width=295, height=2, bg='black').pack(side=TOP, fill=X, padx=15, pady=15)#.place(x=25, y=107)

def on_enter(e):
    word.delete(0, 'end')

def on_leave(e):
    name = word.get()
    if name == '':
        word.insert(0, 'Password')

word = Entry(Login_frame, width=25, fg='indigo', borderwidth=0.5, bg='white', font='Arimo,20')
# word = Entry(Login_frame, width=25, fg='black', borderwidth=0, bg='white', font='Arimo,11')
word.pack(fill=X, padx=15, pady=15, ipadx=5, ipady=10)
# word.place(x=30, y=150)
word.insert(0, 'Password')
word.bind('<FocusIn>', on_enter)
word.bind('<FocusOut>', on_leave)

# Frame(Login_frame, width=295, height=2, bg='black').pack(side=TOP, fill=X, padx=15, pady=15)#.place(x=25, y=177)

Button(Login_frame, width=39, pady=7, text='Sign In',
command=lambda: signin(), fg='white', bg='#0047ab', font='Arimo,12,bold').pack(fill=X, padx=15, pady=15)#.place(x=30, y=220)

def open_register_window(event):
    root.destroy()
    import register

register_label = Label(Login_frame, text='Register new employee here', fg='blue', bg='white', font='Arimo,10', relief="groove")
register_label.pack(fill=X, padx=15, pady=15, ipadx=10, ipady=10)
# register_label.place(x=100, y=280)
register_label.bind('<Button-1>', open_register_window)
# widget_list = root.winfo_children()
# for widget in widget_list:
#     print(widget)

root.mainloop()