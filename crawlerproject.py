from bs4 import BeautifulSoup as bs
import requests
import os
from urllib.parse import urljoin

def get_html_content(url):
    r = requests.get(url)
    soup = bs(r.content, 'lxml')
    return soup

def download_images(images):
    if not os.path.exists('downloaded_images'):
        os.makedirs('downloaded_images')

    for i, img_url in enumerate(images):
        img_data = requests.get(img_url).content
        with open(os.path.join('downloaded_images', f'image_{i + 1}.jpg'), 'wb') as f:
            f.write(img_data)

def download_pdfs(pdf_urls, base_url):
    if not os.path.exists('downloaded_pdfs'):
        os.makedirs('downloaded_pdfs')

    for i, pdf_url in enumerate(pdf_urls):
        absolute_url = urljoin(base_url, pdf_url)
        pdf_data = requests.get(absolute_url).content
        with open(os.path.join('downloaded_pdfs', f'file_{i + 1}.pdf'), 'wb') as f:
            f.write(pdf_data)

def get_images_and_links(soup, base_url):
    choice = int(input("\nTo retrieve Images press (1)\nTo retrieve Hyperlinks press (2)\n"))

    if choice == 1:
        images = [item.get('src') or item.get('data-src') for item in soup.select('[src^="http"], [data-src^="http"]')]
        print("Images(src):")
        print(images)
        download_images(images)
        print("Images downloaded successfully to the 'downloaded_images' directory.")
        x = input("Do you want the hyperlinks?:(yes/no)\n").lower()
        if x == "yes":
            hyperlinks = [urljoin(base_url, item.get('href')) for item in soup.select('[href^="http"]')]
            print("Hyperlinks:")
            print(hyperlinks)
            z = input("Do you want to download the PDFs?: (yes/no)\n")
            if z == "yes":
                pdfs = [item.get('href') for item in soup.select('[href$=".pdf"]')]
                download_pdfs(pdfs, base_url)  # Pass base_url to download_pdfs
                print("PDFs downloaded successfully to the 'downloaded_pdfs' directory.")
            else:
                print("Goodbye Sir")

    else:
        hyperlinks = [urljoin(base_url, item.get('href')) for item in soup.select('[href^="http"]')]
        print("Hyperlinks:")
        print(hyperlinks)
        z = input("Do you want to download the PDFs?: (yes/no)\n")
        if z == "yes":
            pdfs = [item.get('href') for item in soup.select('[href$=".pdf"]')]
            download_pdfs(pdfs, base_url)  # Pass base_url to download_pdfs
            print("PDFs downloaded successfully to the 'downloaded_pdfs' directory.")
        else:
            y = input("Do you want the Images?:(yes/no)\n").lower()
            if y == "yes":
                images = [item.get('src') for item in soup.select('[src^="http"]')]
                print("Images(src):")
                print(images)
                download_images(images)
                print("Images downloaded successfully to the 'downloaded_images' directory.")
            else:
                print("Goodbye Sir")

def main():
    user_url = input('Enter your URL:\n').lower()
    base_url = user_url  # Set the base URL as the user-provided URL for simplicity
    soup = get_html_content(user_url)
    get_images_and_links(soup, base_url)

if __name__ == "__main__":
    main()