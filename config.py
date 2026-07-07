import os

import time
from os import getenv
from dotenv import load_dotenv
from os import environ

    

if os.path.exists("local.env"):
    load_dotenv("local.env")
load_dotenv()


admins = {}
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "784589736").split()))
OWNER_ID = int(environ["OWNER_ID"])

LOGG_CHANNEL = int(os.environ.get("LOGG_CHANNEL", "-1001784386455"))
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001784386455"))
LOG_GROUP = int(os.environ.get("LOG_GROUP", "-1001821837889"))
AUTH_CHATS = environ.get("AUTH_CHATS").split()
AUTH_CHATS = [int(_x) for _x in AUTH_CHATS]
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "784589736").split())


#Database
DB_URL = os.environ.get("DB_URL", "")
DB_NAME = os.environ.get("DB_NAME", "")
BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", True))

HEROKU_API_KEY = environ.get("HEROKU_API_KEY", "")
BT_STRT_TM = time.time()

#===============

PICS = (environ.get('PICS', 'https://telegra.ph/file/1c90d99d2bc0400310ade.jpg')).split()

DOWNLOAD_DIR = "downloads"
    
    # Ensure download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


COOKIES_FILE = os.getenv("COOKIES_FILE", "fcookies.txt")
