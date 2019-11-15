# coding: UTF-8

import os
from os import path
from os.path import dirname
from dotenv import load_dotenv

dotenv_path = path.join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

DEVELOPER_KEY = os.environ.get("DEVELOPER_KEY")