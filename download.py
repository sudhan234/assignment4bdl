import requests
import os
import zipfile
from bs4 import BeautifulSoup
from datetime import datetime
import yaml

with open("params.yaml", 'r') as f:
    params=yaml.safe_load(f)
    print(params)

def download_files(year, n_locs):
    base_url=f'https://www.ncei.noaa.gov/data/local-climatological-data/access/{year}'
    down_folder=f'downloaded_files/{year}'

    os.makedirs(down_folder, exist_ok=True)
    res=requests.get(base_url)
    if res.status_code==200:
        soup=BeautifulSoup(res.text, 'html.parser')
        table=soup.find('table')
        if table:
            anchors=table.find_all('a')
            anchors.reverse()
            num_files_downloaded=0

            for anchor in anchors:
                if num_files_downloaded>=n_locs:
                    break
                
                file_name=anchor.text
                if file_name.endswith('.csv'):
                    file_url=f'{base_url}/{file_name}'
                    try:
                        request_file=requests.get(file_url)
                        if request_file.status_code==200:
                            with open(os.path.join(down_folder, file_name), 'wb') as f:
                                f.write(request_file.content)
                            num_files_downloaded+=1
                            print(f'Downloaded: {file_name}')
                        else:
                            print(f'Download failed: {file_url}')
                    except Exception as e:
                        print(f"Error while downloading : {file_url}. Error: {e}")
        else:
            print('Table not found in page')
    else:
        print(f'failed to retrieve data in {year}')

download_files(params['year'], params['nlocs'])
