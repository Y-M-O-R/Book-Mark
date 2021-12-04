import requests

import csv


def check_urls(url):
    '''checks if url is working or has a problem with it'''
    response = requests.get(url)
    if response.status_code == 200:  # 200 OK
        return True
    if response.status_code == 204:  # 204 No Content
        print(204)

        return False
    if response.status_code == 400:  # 400 Bad Request
        print(400)

        return False


with open('book_mark_link_libary', 'r') as file: # gets saved bookmarks
    csv_reader = csv.DictReader(file)
    url_to_scrape = []
    for row in csv_reader:
        url_to_scrape.append(row['url'])
request_url = []

for url in url_to_scrape:
    connection = check_urls(url)
    if connection:# bookmark connected (http status code 200)
        print('-- connection')
        request = requests.get(url)
        request_url.append(request) # saves conected bookmark
    else:
        print('-- no_connection')

print(request_url[1].text)


