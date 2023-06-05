from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

TITLE = "Password Generator"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []
    password_list += [str(choice(letters)) for letter in range(randint(8, 10))]
    password_list += [str(choice(symbols)) for symbol in range(randint(2, 4))]
    password_list += [str(choice(numbers)) for number in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)
    entry_password.delete(0, END)
    entry_password.insert(0, password)

    pyperclip.copy(password)
    messagebox.showinfo("Password", "Password is generated and copied to your clipboard")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website = entry_website.get().upper()
    email = entry_email.get()
    password = entry_password.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(TITLE, "Please complete all the fields!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open("data.json", "w") as data_file:
                data.update(new_data)
                json.dump(data, data_file, indent=4)
        finally:
            entry_website.delete(0, END)
            entry_password.delete(0, END)
            messagebox.showinfo(TITLE, f"Email and password for {website} are saved.")


# ---------------------------- SEARCH ------------------------------- #
def search():
    website = entry_website.get().upper()
    if website == "":
        messagebox.showinfo(title=TITLE, message="Please enter website to search.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title=TITLE, message=f"Email and password for {website} are not found.")
        else:
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"Email: {email}\n"
                                                           f"Password: {password}")
            else:
                messagebox.showinfo(title=TITLE, message=f"Email and password for {website} are not found.")

# ---------------------------- UI SETUP ------------------------------- #


def display_msg():
    to_close_app = messagebox.askokcancel(title=TITLE, message="Are you sure you want to close the app?")
    if to_close_app:
        window.destroy()


window = Tk()
window.title(TITLE)
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=200)
my_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=my_img)
canvas.grid(row=0, column=1)

label_website = Label(text="Website:")
label_website.grid(row=1, column=0, sticky="e", padx=5)
label_email = Label(text="Email/Username:")
label_email.grid(row=2, column=0, sticky="e", padx=5)
label_password = Label(text="Password:")
label_password.grid(row=3, column=0, sticky="e", padx=5)

entry_website = Entry(width=35)
entry_website.focus()
entry_website.grid(row=1, column=1)
entry_email = Entry(width=54)
entry_email.insert(0, "name@email.com")
entry_email.grid(row=2, column=1, columnspan=2, pady=5)
entry_password = Entry(width=35)
entry_password.grid(row=3, column=1)

button_search = Button(text="Search", width=15, command=search)
button_search.grid(row=1, column=2)
button_generate_password = Button(text="Generate password", width=15, command=generate_password)
button_generate_password.grid(row=3, column=2)
button_add = Button(text="Add", width=46, command=save_data)
button_add.grid(row=4, column=1, columnspan=2, pady=5)

window.protocol("WM_DELETE_WINDOW", display_msg)

window.mainloop()
