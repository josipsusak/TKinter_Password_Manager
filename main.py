from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import json
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {"email": email, "password": password, }}

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(
            title="Oops", message="Please dont leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)

        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, "end")
            email_entry.delete(0, "end")
            password_entry.delete(0, "end")


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    user_entry = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")

    else:
        for website in data:
            email = data[website]['email']
            password = data[website]['password']
            if user_entry == website:
                messagebox.showinfo(
                    title=website, message=f"Email: {email}\nPassword: {password}")
                pyperclip.copy(password)
            else:
                messagebox.showinfo(
                    title="Error", message=f"No details for the {website} exist.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
generator_logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=generator_logo)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

website_entry = Entry(width=51)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=51)
email_entry.grid(row=2, column=1, columnspan=2)
password_entry = Entry(width=33)
password_entry.grid(row=3, column=1)

password_button = Button(text="Generate Password",
                         width=14, command=generate_password)
password_button.grid(row=3, column=2)
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)
add_button = Button(text="Add", width=43, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
