# session.py
from instagrapi import Client
import os, pickle
from dotenv import dotenv_values

def login():
    config = dotenv_values('.env')
    usr = config["USERNAME"]
    pwd = config["PASSWORD"]

    cl = Client()
    SESSION_FILE = "session.pkl"

    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "rb") as f:
            cl.set_settings(pickle.load(f))
        cl.login(usr, pwd)
    else:
        cl.login(usr, pwd)

    with open(SESSION_FILE, "wb") as f:
        pickle.dump(cl.get_settings(), f)

    return cl
