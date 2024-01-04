import os
import requests
import shutil
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def copy_html(uri, destination_path):
    parsed_uri = urlparse(uri)

    if os.path.exists(destination_path):
        print("File already exists, skipping")
        return

    # Check if it's an HTTP or HTTPS link
    if parsed_uri.scheme in ["http", "https"]:
        download_html(uri, destination_path)
    # Check if it's a local path
    elif os.path.exists(uri):
        print("Found local file, copying")
        shutil.copy(uri, destination_path)
    else:
        return print("Not sure how to access file") 
        raise


def download_html(url, file_path):
    """ Downloads the webpage """
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(file_path, 'w') as file:
            file.write(response.text)
        print(f"HTML downloaded and saved as '{file_path}'")
    else:
        print("Failed to download HTML")
        

def convert_webpage_to_markdown(url):
    # Step 1: Fetch the webpage content
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch webpage. Status code: {response.status_code}")

    webpage_content = response.text

    # Step 2: Parse the HTML content (optional, based on what you want to convert)
    soup = BeautifulSoup(webpage_content, 'html.parser')
    # For example, if you just want the main content inside a specific tag:
    # content = soup.find('div', {'class': 'main-content'})

    # But for this example, we'll convert the entire content:
    content = soup.prettify()