import csv

import requests
from bs4 import  BeautifulSoup
class menu:
    '''tempory replace with gui'''
    def remove_book_mark(self):
        pass
    def append_book_mark(self):
        pass

class save_book_marks:
    def __init__(self):
        pass

    def read_book_mark(self):
        '''read book marks saved'''
        self.book_marked = None
        with open('book_mark_link_libary', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                print(row['title'], row['url'])

    def append_book_mark(self, title = str, url = str, *args): # fix append adds headers every append
        '''append book marks saved'''
        for arg in args:
            for arg in arg:

                # goes throughj argument and checks weateher it is an TITLE/URL

                if arg[0:5].split()[0] == 'TITLE':
                    title = arg.strip('TITLEURL')
                elif arg[0:5].split()[0] == 'URL':
                    url = arg.strip('TITLEURL')
                with open('book_mark_link_libary', 'a', newline='') as file:
                    csv_writer = csv.DictWriter(file, ['title', 'url'], delimiter=',')

                    row = {'title': f'{title}', 'url': f'{url}'}
                    csv_writer.writerow(row)

        with open('book_mark_link_libary', 'a', newline='') as file:
            csv_writer = csv.DictWriter(file, ['title', 'url'], delimiter = ',')
            csv_writer.writeheader()
            row =  {'title':f'{title}', 'url':f'{url}'}
            csv_writer.writerow(row)

    def remove_book_mark(self, title = str, url = str):
        '''remove book mark saved'''
        with open('book_mark_link_libary', 'r') as file:
            csv_reader = csv.DictReader(file)
            csv_new_row = [] # save bookmarks that are not removed to rewrite csv doc
            for row in csv_reader: # removes bookmark
                if title == row['title'] and url == row['url']:
                    del row
                else:
                    csv_new_row.append(row)

        with open('book_mark_link_libary', 'w', newline='') as file: # rewrites csv file without removed book marks
            csv_writer = csv.DictWriter(file, ['title', 'url'], delimiter=',')
            csv_writer.writeheader()
            for row in csv_new_row:
                csv_writer.writerow(row)

save_books = save_book_marks() # todo add to menu

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

class book_shelf:
    def __init__(self):
        self.request_url = [] # requests of all book marks
        self.book_mark_header = [] # chapter titles
        self.header_url = {}
    def book_in_stock(self): # checks if bookmarks works and requests it
        with open('book_mark_link_libary', 'r') as file: # gets saved bookmarks
            csv_reader = csv.DictReader(file)
            url_to_scrape = []
            for row in csv_reader:
                url_to_scrape.append(row['url'])
                self.book_mark_header.append(row['title'])
                self.header_url = row['title'] # todo save bookmarks with chapters to csv
                
            
        for index, url in enumerate(url_to_scrape):

            connection = check_urls(url)
            if connection:# bookmark connected (http status code 200)
                print(f'-- connection {index}/{len(url_to_scrape)-1}')
                request = requests.get(url)
                self.request_url.append(request) # saves conected bookmark
            else:
                print(f'-- no_connection {index}/{len(url_to_scrape)-1}')


    def borrow_book_mark(self):
        return  self.request_url, self.book_mark_header


requested_book = book_shelf() # todo add to menu
requested_book.book_in_stock()
requests, chapter_header = requested_book.borrow_book_mark()


# todo first p tag == summuray
# todo find optimal time for requests


def get_book_marks(requests, chapter_header, header_url):
    links, chapters = [], []
    chapter_header_header = {}

    x = 0
    for request in requests: # goes through all bookmark requests and scrapes them
        bs4_request = BeautifulSoup(request.text, features="html.parser")
        request_book_marks = bs4_request.find('div', {'class': 'page-content-listing single-page'})
        try:
            book_marks = request_book_marks.findAll('a')
        except AttributeError:
            print('error',request_book_marks)
            book_marks = None
        try:
            for link in book_marks: # gets links
                links.append(link.get('href'))
            for chapter in book_marks:
                chapters.append(chapter.string) # gets chapters

            chapter_header_header[chapter_header[x]]=chapters
            x+=1
            chapters = []

            #print(chapters)
        except TypeError:
            print('None BookMark')

    print(chapter_header_header)
    #print(chapter_header_header)
    with open('book_mark_chapter.csv','w', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=list(chapter_header_header.keys()))
        csv_writer.writeheader()
        row = chapter_header_header
        csv_row = []
        #  csv_writer.writerow(row)
        for i in row:
            #print(i)
            csv_row.append([])

        #print(row)




get_book_marks(requests, chapter_header,1)


print('code executed+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')