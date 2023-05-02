from tkinter import messagebox
from tkinter import *
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_list = password_numbers + password_symbols + password_letters

    random.shuffle(password_list)
    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't have any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # Saving up updated data
                json.dump(data, data_file, indent=4)
        finally:
            password_input.delete(0, END)
            website_input.delete(0, END)
            website_input.focus()

# -----------------------------FIND PASSWORD-----------------------------


def find_password():
    website = website_input.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}.")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
canvas = Canvas(width=200, height=200)
key_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=key_img)
canvas.grid(column=1, row=0)

# Texts
website_text = Label(text="Website:")
website_text.grid(column=0, row=1)
email_text = Label(text="Email/Username:")
email_text.grid(column=0, row=2)
password_text = Label(text="Password:")
password_text.grid(column=0, row=3)

# Entries
website_input = Entry(width=35)
website_input.grid(row=1, column=1)
website_input.focus()
email_input = Entry(width=35)
email_input.grid(row=2, column=1)
email_input.insert(0, "user_test@gmail.com")
password_input = Entry(width=35)
password_input.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", command=find_password)
search_button.grid(row=1, column=2)
generate_password_button = Button(text="Generate Password", command=generate)
generate_password_button.grid(column=2, row=3)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
