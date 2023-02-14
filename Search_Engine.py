import requests
from bs4 import BeautifulSoup
import lxml
import wikipedia

class SearchEngine:
    def __init__(self, word):
        self.library_soup = ""
        self.wiki_soup = ""
        self.final_library_links = ""
        self.final_wiki_links = ""
        self.library_link = 'https://openlibrary.org/search?q='
        self.wiki_link = 'https://en.wikipedia.org/wiki/'
        self.word = word
        self.library_links_list = []
        self.wiki_links_list = []

    def get_response(self):
        word_list = self.word.split(' ')

        for i in range(0, len(word_list)):
            if i < len(word_list) - 1:
                self.library_link += word_list[i] + '+'
            else:
                self.library_link += word_list[i] + '&mode=everything'

        self.wiki_link += self.word
        try:
            library_soup = BeautifulSoup(requests.get(self.library_link).text, 'lxml')
            wiki_soup = BeautifulSoup(requests.get(self.wiki_link).text, 'lxml')
            self.final_library_links = library_soup.find_all('a', class_='results')
            self.final_wiki_links = wiki_soup.find_all('p')
        except:
            return None

    def get_data(self):
        try:
            self.get_response()
            for books in self.final_library_links:
                self.library_links_list.append({"title":books.getText() , "link":books.get('href')})

            for text in self.final_wiki_links:
                self.wiki_links_list.append(text.getText())

            self.library_links_list = self.library_links_list[:10]
            self.wiki_links_list = self.wiki_links_list[:8]
        except:
            return None

    def library_search(self):
        self.get_data()
        if self.get_data == None:
            self.library_links_list = []
            
        return self.library_links_list

    def wiki_search(self):
        self.get_data()
        if self.get_data == None:
            self.wiki_links_list = []
        return self.wiki_links_list
