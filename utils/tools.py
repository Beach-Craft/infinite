import random
import string

def id_generator():
    store = [] #It will contain passwords

    id_length = 2

    for i in range(id_length):# using string module to generate the password

        cap = random.choice(string.ascii_uppercase)

        store += cap

        small = random.choice(string.ascii_lowercase)

        store += small

        digit = random.choice(string.digits)

        store += digit

    id = "".join(store) #Making the password a string

    return id