import requests

user_login = 'rfeldman9'
url = f'https://letterboxd.com/{user_login}/films/diary/'

r = requests.get(url)
with open('letterbox.html', 'w', encoding='utf-8') as output_file:
    output_file.write(r.text)
