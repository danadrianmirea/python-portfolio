import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

os.chdir(os.path.dirname(__file__))

def scrape_images(url, depth=0):
    scraped_images = set()
    to_scrape = [(url, 0)]
    img_folder = "img"
    os.makedirs(img_folder, exist_ok=True)

    while to_scrape:
        current_url, current_depth = to_scrape.pop(0)
        parsed_url = urlparse(current_url)

        if current_url is None:
            print(f"Skipping None URL")
            continue

        if current_url.startswith('mailto:'):
            print(f"Skipping mailto link: {current_url}")
            continue

        if not parsed_url.scheme:
            print(f"Skipping invalid URL: {current_url}")
            continue

        print(f"Scraping {current_url} at depth {current_depth}")
        if current_depth > depth:
            print(f"Skipping {current_url} (depth {current_depth} > {depth})")
            continue
        response = requests.get(current_url)
        print(f"Got response {response.status_code} for {current_url}")
        if response.status_code != 200:
            print(f"Skipping {current_url} (response {response.status_code})")
            continue
        soup = BeautifulSoup(response.content, 'html.parser')

        img_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg']
        for img in soup.find_all('img'):
            img_url = img.get('src')
            if img_url and img_url.startswith('/'):
                img_url = urljoin(current_url, img_url)
            if img_url and img_url not in scraped_images:
                scraped_images.add(img_url)
                img_path = os.path.basename(urlparse(img_url).path)
                img_ext = os.path.splitext(img_path)[1].lower()
                if img_ext in img_extensions:
                    try:
                        img_data = requests.get(img_url).content
                        img_name = os.path.basename(urlparse(img_url).path)
                        img_path = os.path.join(img_folder, img_name)
                        with open(img_path, 'wb') as img_file:
                            img_file.write(img_data)
                        print(f"Saved image {img_url} as {img_path}")
                    except Exception as e:
                        print(f"Failed to save image {img_url}: {e}")

        for a in soup.find_all('a'):
            href = a.get('href')
            if href and href.startswith('http'):
                print(f"Found link {href} on {current_url}")
            if href not in [i[0] for i in to_scrape]:
                to_scrape.append((href, current_depth + 1))

url = "https://www.wikipedia.org/"
scrape_images(url, 1)

