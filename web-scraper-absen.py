import requests
import os
import csv
from dotenv import load_dotenv
from bs4 import BeautifulSoup
# import pandas as pd

load_dotenv()

fin = []
url_login = os.getenv('URL_LOGIN')
url_scrape = os.getenv('URL_ABSEN')
login_payload = {
    'login_username': os.getenv('USERNAME'),
    'login_password': os.getenv('PASSWORD')
}

kelas_asal = 22
jadwal_kegiatan = 8
absen_number = 0
absen_kelas = 0

with requests.session() as session:
    login_session = session.post(url_login, data=login_payload)
    cookies = login_session.cookies

    while kelas_asal < 48: # 22 - 47
        while jadwal_kegiatan < 13: # 8 - 12
            absen_number = absen_kelas

            absen_payload = {
                'unit_sekolah_asal': 1,
                'kelas_asal': kelas_asal, # 22 - 47
                'jadwal_kegiatan': jadwal_kegiatan, # 8 - 12
                'tanggal': '2024-10-04',
                'cetak_harian': 'PRINT',
                'bulan': 10,
                'tahun': 2024,
            }

            absen_session = session.post(url_scrape, cookies=cookies, data=absen_payload)
            absen_html = BeautifulSoup(absen_session.text, 'html.parser')
            if 'Putri' in absen_html.get_text():
                break

            absen_table = absen_html.find(class_='gridtable')

            for row in absen_table.find_all('tr'):

                cells = row.find_all('td')
                if cells == []:
                    continue
                data = [cell.text.strip() for cell in cells]
                if jadwal_kegiatan == 8:
                    fin.append([data[2].replace('Kelas ', '').replace(' - Putra', ''), data[3], 0])
                if data[4] == 'Belum Presensi':
                    fin[absen_number][2] += 1

                absen_number += 1
            jadwal_kegiatan += 1
        jadwal_kegiatan = 8
        absen_kelas = absen_number
        kelas_asal += 1
        print('load :', absen_kelas)

with open('/mnt/c/Users/Asus/Desktop/data.csv', 'w') as f:
     
    # using csv.writer method from CSV package
    write = csv.writer(f)
     
    write.writerow(['kelas', 'nama', 'absen'])
    write.writerows(fin)

# df = pd.DataFrame(fin)
# writer = pd.ExcelWriter('/mnt/c/Users/Asus/Desktop/test.xlsx', engine='xlsxwriter')
# df.to_excel(writer, index=False)
# writer.save()
