import requests
import os
from dotenv import load_dotenv

load_dotenv()

url_login = os.getenv('URL_LOGIN')
login_payload = {
    'login_username': os.getenv('USERNAME'),
    'login_password': os.getenv('PASSWORD')
}

def login_cookies():
    login_session = requests.session().post(url_login, data=login_payload)
    cookies = login_session.cookies
    return cookies
