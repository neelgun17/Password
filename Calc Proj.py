# importing the tkinter module
from tkinter import *
import pyperclip
import random
import sqlite3
from cryptography.fernet import Fernet

# Initialize encryption key and cipher suite
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_password(password):
    """Encrypts the password."""
    return cipher_suite.encrypt(password.encode())

def decrypt_password(encrypted_password):
    """Decrypts the password."""
    return cipher_suite.decrypt(encrypted_password).decode()

def setup_database():
    """Sets up the SQLite database by creating a new table with the updated schema."""
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    
    # Drop the existing table if it exists (WARNING: This will delete all existing data in the table)
    c.execute('DROP TABLE IF EXISTS passwords')
    
    # Create a new table with the desired schema
    c.execute('''CREATE TABLE passwords
                 (website TEXT, username TEXT, encrypted_password BLOB)''')
    
    conn.commit()
    conn.close()


setup_database()  # Ensure the database is set up

# initializing the tkinter
root = Tk()

# setting the width and height of the gui
root.geometry("400x400")    # x is small case here

# declaring a variable of string type and this variable will be 
# used to store the password generated
passstr = StringVar()

# declaring a variable of integer type which will be used to 
# store the length of the password entered by the user
passlen = IntVar()
passlen.set(0)

capital = False
special = False
capital_var = IntVar()
special_var = IntVar()
website_name = StringVar()
username = StringVar()

# function to generate the password
def toggle_capital():
    global capital  # Specify that we want to use the global 'capital' variable
    capital = not capital  # Toggle between True and False
    print(f"Capital letters required: {capital}")  # Print status to console for verification

def special_var_toggle():
     global special
     special = not special
     print(f"Special Characters required: {special}")
    

def generate():
    # Variable storing special characters
    special_chars = "!@#$%^&*()-_=+][}{|;:'\",.<>/?`~"
    
    # storing the keys in a list which will be used to generate 
    # the password 
    set = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
            'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
            'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 
            'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', 
            '9', '0']

    # declaring the empty string
    password = ""

    # loop to generate the random password of the length entered           
    # by the user
    for x in range(passlen.get()):
        random_number = random.randint(0, 1)
        # print(random_number)
        if random_number == 0 and special_var:
            password = password + random.choice(special_chars)
        else:
            password = password + random.choice(set)
        
    if capital and not any(ele.isupper() for ele in password):
        char_list = list(password)
        
        # Find all indices of lowercase letters
        lowercase_indices = [i for i, char in enumerate(char_list) if char.islower()]
        
        # If there are lowercase letters, choose one at random and capitalize it
        if lowercase_indices:
            random_index = random.choice(lowercase_indices)
            char_list[random_index] = char_list[random_index].upper()
        # print("Password after " + password)
    # setting the password to the entry widget
    passstr.set(password)
    

# Function to save the password along with the website
def save_password(website, username, password):
    """Saves the encrypted password and website to the database."""
    encrypted_password = encrypt_password(password)
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("INSERT INTO passwords (website, username, encrypted_password) VALUES (?, ?, ?)",
              (website, username, encrypted_password))
    conn.commit()
    conn.close()
    print("Password Saved")


def copytoclipboard():
    """Copies the password to clipboard and stores it in the database."""
    random_password = passstr.get()
    website = website_name.get()  # Get the website name from the input field
    user_name = username.get()
    if website and user_name:  # Ensure both website and username are provided
        save_password(website, user_name, random_password)
    pyperclip.copy(random_password)
    website_name.set("")  # Clear the website name field
    


Label(root, text="Password Generator Application", font="calibri 20 bold").pack()

Label(root, text="Enter website name").pack(pady=3)
Entry(root, textvariable=website_name).pack(pady=3)

Label(root, text="Enter username").pack(pady=3)
Entry(root, textvariable=username).pack(pady=3)

Label(root, text="Enter password length").pack(pady=3)
Entry(root, textvariable=passlen).pack(pady=3)

# Checkbox for capital letter requirement
Checkbutton(root, text="Capital Letter Required", command=toggle_capital).pack()

# Checkbox for special characters requirement
Checkbutton(root, text="Special Characters Required", command=special_var_toggle).pack()

Button(root, text="Generate Password", command=generate).pack(pady=7)
Entry(root, textvariable=passstr).pack(pady=3)
Button(root, text="Save and Copy to clipboard", command=copytoclipboard).pack()

# mainloop() is an infinite loop used to run the application when 
# it's in ready state 
root.mainloop()