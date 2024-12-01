import requests
import os 

def shorten_link(orig_url, url_name):
  #galing tong API KEY sa cuttly para makapagshorten tayo ng links gamit yung website o domain nila 
    API_KEY = "2f90b4e797b258ab9ca5b3777fb312f2d1f03"
    BASE_URL = "https://cutt.ly/api/api.php"
    
    payload = {'key': API_KEY, 'short': orig_url, 'name': url_name}
    request = requests.get(BASE_URL, params=payload)
    data = request.json()

    print('')

    try:
        title = data['url']['title']
        short_link = data['url']['shortLink']

        print('Title: ', title)
        print('Link: ', short_link)
    except:
        status = data['url']['status']
        print('Error Status: ', status)

os.system('cls')
link = input('Paste your link here: ')
name = input('Enter your desired name for the link(Leave empty if not): ')

shorten_link(link, name)
