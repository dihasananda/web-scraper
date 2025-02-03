import requests
import os
import csv
import sys
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

url_login = os.getenv('URL_LOGIN')
url_scrape = os.getenv('URL_ABSEN')
login_payload = {
    'login_username': os.getenv('USERNAME'),
    'login_password': os.getenv('PASSWORD')
}

data_absen = [] # variable untuk menyimpan hasil

unit_sekolah_asal = 1
list_kelas_asal = list(range(22, 48)) # 22 - 47
list_jadwal_kegiatan = [8, 9, 10, 11, 12, 21, 22, 25] # 8 - 12
absen_number = 0
absen_kelas = 0
tanggal = "2024-12-03"
bulan = sys.argv[1]
tahun = "2024"

with requests.session() as session:
    login_session = session.post(url_login, data=login_payload)
    cookies = login_session.cookies
    print('login success')

    for kelas_asal in list_kelas_asal:
        for jadwal_kegiatan in list_jadwal_kegiatan:
            absen_number = absen_kelas

            absen_payload = {
                'unit_sekolah_asal': unit_sekolah_asal,
                'kelas_asal': kelas_asal,
                'jadwal_kegiatan': jadwal_kegiatan, 
                'tanggal': tanggal,
                'cetak_perbulan': 'PRINT',
                'bulan': bulan,
                'tahun': tahun,
            }

            absen_session = session.post(url_scrape, cookies=cookies, data=absen_payload)
            absen_html = BeautifulSoup(absen_session.text, 'html.parser')

            absen_table = absen_html.find(class_='gridtable')

            for row in absen_table.find_all('tr'):
                cells = row.find_all('td')
                if cells == []:
                    continue
                data = [cell.text.strip() for cell in cells]
                if jadwal_kegiatan == 8:
                    data_absen.append([data[2].replace('Kelas ', '').replace(' - Putra', ''), data[1], int(data[7])])
                else:
                    data_absen[absen_number].append(int(data[7]))

                absen_number += 1
                
        absen_kelas = absen_number
        print('load :', absen_kelas)

with open('/mnt/c/Users/Asus/Desktop/data ' + bulan +'.csv', 'w') as f:
     
    write = csv.writer(f, delimiter=";")
     
    write.writerow(['kelas', 'nama', 'subuh', 'dhuha', 'dhuhur','ashar', 'magrib', 'ashar-pi', 'dhuhur-pi', 'isya-pi'])
    write.writerows(data_absen)
