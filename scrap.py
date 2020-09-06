import requests
from bs4 import BeautifulSoup
import glob
import json
import pandas as pd

session = requests.Session()


def total_pages():
    print('Total Pages')
    respons = session.get('https://gundamnesia.com/shop')
    soup = BeautifulSoup(respons.text, features='html.parser')
    page_item = soup.find('ul', attrs={'class': 'page-numbers'})
    pages = []

    for items in page_item.find_all('a'):
        item = items.get_text()
        pages.append(item)

    del pages[-1]
    last_pages = pages[-1]
    return int(last_pages)


def get_url(pages):
    print(f'Getting Url Page {pages}')
    page = pages
    respons = session.get(f'https://gundamnesia.com/shop/page/{page}')
    soup = BeautifulSoup(respons.text, features='html.parser')
    titles = soup.find_all('h3', attrs={'class': 'heading-title product-name'})
    urls = []
    for title in titles:
        url = title.find('a')['href']
        urls.append(url)

    return urls


def get_detail(url):
    print(f'Get Detail {url}')

    respons = session.get(url)

    soup = BeautifulSoup(respons.text, features='html.parser')

    title = soup.find('h1', attrs={'class': 'product_title entry-title'}).text.strip()

    categories = soup.find('span', attrs={'class': 'cat-links'}).text.strip()

    stock_area = soup.find('p', attrs={'class': 'availability stock in-stock'})
    stock = stock_area.find('span').text.strip()

    dict_data = {
        'title': title,
        'stock': stock,
        'categories': categories,
    }
    'Create JSON file'
    with open(f'./results/{url.replace("https://gundamnesia.com/shop/", "").replace("/", "-")}.json', 'w') as outfile:
        json.dump(dict_data, outfile)


def creat_csv_excel():
    print('Creating CSV...')
    datas = []
    files = glob.glob('./results/*.json')
    for file in files:
        print(file)
        with open(file) as json_file:
            data = json.load(json_file)
            datas.append(data)

    'Create csv data'
    df = pd.DataFrame(datas)
    df.to_csv('results.csv', index=False)

    'Create xlsx Data'
    df = pd.DataFrame(datas)
    writer = pd.ExcelWriter('results.xlsx', engine='xlsxwriter')

    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()


def run():
    total_page = total_pages()
    total_urls = []

    for x in range(total_page):
        x += 1
        urls = get_url(x)
        total_urls += urls

    'Write JSON file'
    with open('urls.json', 'w') as outfile:
        json.dump(total_urls, outfile)

    'Read JSON file'
    with open('urls.json') as json_file:
        urls = json.load(json_file)

    for url in urls:
        get_detail(url)

    creat_csv_excel()


if __name__ == '__main__':
    run()
