from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "Email": email, 
            "Password": password,
        }
    }

    if len(password) <= 0 or len(website) <= 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any of the fields empty")
    else:
        try:
            with open("password.json", "r") as pass_bank:
                data = json.load(pass_bank)
        except FileNotFoundError:
            with open("password.json", "w") as pass_bank:
                json.dump(new_data, pass_bank, indent=4)
        else:
            # 2. Updating old Data
            data.update(new_data)
            # Open file in write mode
            with open("password.json", "w") as pass_bank:
                # 3. Saving new data
                json.dump(data, pass_bank, indent=4)
        finally:
            website_entry.delete(0, END)
            # email_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search():
    website = website_entry.get()
    try:
        with open("password.json", "r") as pass_bank:
            data = json.load(pass_bank)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No passwords saved")
    else:
        if website in data:
            password = data[website]["Password"]
            email = data[website]["Email"]
            messagebox.showinfo(title=data[website], message=f"Email: {email} \nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No passwords for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50, highlightthickness=0)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img, )
canvas.grid(column=1, row=0)

# Website label
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
# Email/User Label
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
# Password Label
password_label = Label(text="Password:", )
password_label.grid(column=0, row=3)

# Website entry
website_entry = Entry(width=23)
website_entry.grid(column=1, row=1,)
website_entry.focus()
# Email/User Entry
email_entry = Entry(width=40)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "Example@example.com")
# Password Entry
password_entry = Entry(width=23,)
password_entry.grid(column=1, row=3)

# Generate Password Button
gen_pass = Button(text="Generate Password", command=generate_password)
gen_pass.grid(column=2, row=3)
# Add Button
add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)
# Search Button
search_button = Button(text="Search",width=13, command=search)
search_button.grid(column=2, row=1)

window.mainloop()
