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
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001784386455"))
#CHANNEL_ID = int(os.environ.get("CHANNEL_ID", ""))
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "784589736").split())
DB_URL = os.environ.get("DB_URL", "")
DB_NAME = os.environ.get("DB_NAME", "")
BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", True))

HEROKU_API_KEY = environ.get("HEROKU_API_KEY", "")
BT_STRT_TM = time.time()

#===============

PICS = (environ.get('PICS', 'https://telegra.ph/file/1c90d99d2bc0400310ade.jpg')).split()
