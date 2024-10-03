import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

fin = []
url_login = os.getenv('URL_LOGIN')
url_scrape = os.getenv('URL_ABSEN')
login_payload = {
    "login_username": os.getenv('USERNAME'),
    "login_password": os.getenv('PASSWORD')
}

kelas_asal = 22
jadwal_kegiatan = 8
absen_number = 0
absen_kelas = 0

with requests.session() as session:
    login_session = session.post(url_login, data=login_payload)
    cookies = login_session.cookies

    while kelas_asal < 47: # 22 - 47
        print("absen kelas : ", absen_kelas)
        while jadwal_kegiatan < 13: # 8 - 12
            absen_number = absen_kelas
            print("absen number : ", absen_number)

            absen_payload = {
                "unit_sekolah_asal": 1,
                "kelas_asal": kelas_asal, # 22 - 47
                "jadwal_kegiatan": jadwal_kegiatan, # 8 - 12
                "tanggal": "2024-10-03",
                "cetak_harian": "PRINT",
                "bulan": 10,
                "tahun": 2024,
            }

            absen_session = session.post(url_scrape, cookies=cookies, data=absen_payload)
            absen_html = BeautifulSoup(absen_session.text, 'html.parser')
            if 'putri' in absen_html.find(string="putri"):
                continue

            absen_table = absen_html.find(class_="gridtable")

            for row in absen_table.find_all('tr'):

                cells = row.find_all('td')
                if cells == []:
                    continue
                data = [cell.text.strip() for cell in cells]
                if jadwal_kegiatan == 8:
                    fin.append(data[3:5])
                else:
                    fin[absen_number].append(data[4])

                absen_number += 1
            jadwal_kegiatan += 1
        jadwal_kegiatan = 8
        absen_kelas = absen_number
        kelas_asal += 1
    print(fin)

