import requests
from pathlib import Path
from bs4 import BeautifulSoup

current_dir = Path.cwd()

main_page = requests.get('https://www.sirm.org/en/category/articles/covid-19-database/')
main_soup = BeautifulSoup(main_page.text, 'html.parser')
frame = main_soup.find('div', class_="page-nav td-pb-padding-side")
total_pages = int(frame.find('a', class_='last').text)

for i in range(total_pages):
    url = f"https://www.sirm.org/en/category/articles/covid-19-database/page/{i+1}/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    frame = soup.find_all('div', class_="td_module_19 td_module_wrap td-animation-stack td-meta-info-hide")
    for sub_frame in frame:
        title = sub_frame.find('h3').text.replace(': ', '_')
        img = sub_frame.find('img', class_="entry-thumb")['data-img-url']
        # Grep image
        image_request = requests.get(img)
        if image_request.ok:
            with open(current_dir / f"{title}.jpg", 'wb') as f:
                f.write(image_request.content)
        print(title, img, 'downloaded')