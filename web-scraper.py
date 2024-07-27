import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

url_login = os.getenv('URL_LOGIN')
url_scrape = os.getenv('URL_SCRAPE')
payload = {
    "login_username": os.getenv('USERNAME'),
    "login_password": os.getenv('PASSWORD')
}

with requests.session() as session:
    post = session.post(url_login, data=payload)

    # Periksa apakah login berhasil
    if post.status_code == 200:
        # Dapatkan cookie atau token sesi
        cookies = post.cookies
        
        index = 8
        while index < 700:
            str_index = str(index)
            # Buat request ke halaman yang ingin di-scrape
            response = session.get(url_scrape + str_index, cookies=cookies)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Ekstrak data
            results = soup.find_all('input')
            if not results[1]['value']:
                index += 1
                continue

            text_result = str_index + ","
            for result in results:
                if result['type']== 'text':
                    text_result += '"' + result['value'] + '"' + ',';
            print(text_result)
            index += 1
    else:
        print("Login gagal")
