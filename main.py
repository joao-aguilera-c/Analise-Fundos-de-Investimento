from urllib.request import urlopen, Request

import requests
from bs4 import BeautifulSoup as bs

import zipfile
import os

URL = 'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/'
HIST_URL = 'HIST/'
FILETYPE = '.csv'
HIST_FILETYPE = '.zip'


def get_soup(url):
    return bs(requests.get(url).text, 'html.parser')


for link in get_soup(URL).findAll('a'):
    file_link = link.get('href')
    if FILETYPE in file_link:
        print('Baixando', file_link)
        with open(link.text, 'wb') as file:
            response = requests.get(URL + file_link)
            file.write(response.content)

    if HIST_URL in file_link:
        for hist_link in get_soup(URL + HIST_URL).findAll('a'):
            file_link = hist_link.get('href')
            if HIST_FILETYPE in file_link:
                print('Baixando e descomprimindo', file_link)
                remoteZip = urlopen(Request(URL + HIST_URL + file_link))
                file_name = file_link
                local_file = open(file_name, 'wb')
                local_file.write(remoteZip.read())
                local_file.close()

                with zipfile.ZipFile(file_name, 'r') as zip_ref:
                    zip_ref.extractall()

                os.remove(file_name)
