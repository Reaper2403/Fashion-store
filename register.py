from tkinter import *
from tkinter import messagebox
import mysql.connector

# Connect to the database
mydb = mysql.connector.connect(
    host="Ideaknight",
    user="epiloger",
    password="mysql",
    database="ananya"
)

root = Tk()
root.title('Register')
root.geometry('400x400')
root.config(bg='#ffffff')
root.resizable(False, False)
root.iconbitmap('send_message_icon_251493.ico')


def register():
    # Get the user details entered by the user
    username = user.get()
    password = word.get()
    fname = first_name.get()
    lname = last_name.get()
    dob = date_of_birth.get()
    
    # Execute the SQL query to insert the new user into the database
    mycursor = mydb.cursor()
    sql = "INSERT INTO users (username, password, F_name, l_name, dob) VALUES (%s, %s, %s, %s, %s)"
    val = (username, password, fname, lname, dob)
    mycursor.execute(sql, val)
    mydb.commit()

    # Show a success message and clear the fields
    messagebox.showinfo('Success', 'Registration Successful!')
    user.delete(0, END)
    word.delete(0, END)
    first_name.delete(0, END)
    last_name.delete(0, END)
    date_of_birth.delete(0, END)

def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username')

def on_enter1(e):
    word.delete(0, 'end')

def on_leave1(e):
    name = word.get()
    if name == '':
        word.insert(0, 'Password')

def on_enter2(e):
    first_name.delete(0, 'end')

def on_leave2(e):
    name = first_name.get()
    if name == '':
        first_name.insert(0, 'First Name')

def on_enter3(e):
    last_name.delete(0, 'end')

def on_leave3(e):
    name = last_name.get()
    if name == '':
        last_name.insert(0, 'Last Name')

def on_enter4(e):
    date_of_birth.delete(0, 'end')

def on_leave4(e):
    name = date_of_birth.get()
    if name == '':
        date_of_birth.insert(0, 'Date of Birth')

frame = Frame(root, width=350, height=350, bg='white')
frame.place(x=25, y=25)

heading = Label(frame, text='Registration Form', fg='#0047ab', bg='white', font='Arimo,15,bold')
heading.place(x=80, y=5)

user = Entry(frame, width=25, fg='black', borderwidth=0, bg='white', font='Arimo,11')
user.place(x=50, y=50)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=77)

word = Entry(frame, width=25, fg='black', borderwidth=0, bg='white', font='Arimo,11', show='*')
word.place(x=50, y=100)
word.insert(0, 'Password')
word.bind('<FocusIn>', on_enter1)
word.bind('<FocusOut>', on_leave1)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=127)

first_name = Entry(frame, width=25, fg='black', borderwidth=0, bg='white', font='Arimo,11')
first_name.place(x=50, y=150)
first_name.insert(0, 'First Name')
first_name.bind('<FocusIn>', on_enter2)
first_name.bind('<FocusOut>', on_leave2)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

last_name = Entry(frame, width=25, fg='black', borderwidth=0, bg='white', font='Arimo,11')
last_name.place(x=50, y=200)
last_name.insert(0, 'Last Name')
last_name.bind('<FocusIn>', on_enter3)
last_name.bind('<FocusOut>', on_leave3)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=227)

date_of_birth = Entry(frame, width=25, fg='black', borderwidth=0, bg='white', font='Arimo,11')
date_of_birth.place(x=50, y=250)
date_of_birth.insert(0, 'Date of Birth')
date_of_birth.bind('<FocusIn>', on_enter4)
date_of_birth.bind('<FocusOut>', on_leave4)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=277)

register_button = Button(frame, text='Register', width=15, bg='#0047ab', fg='white', font='Arimo, 11', command=register)
register_button.place(x=120, y=310)

root.mainloop()
