import requests
import pandas as pd
from bs4 import BeautifulSoup


class Scraper:
    URL = "https://www.imdb.com/chart/top/"

    REQUEST_HEADERS = {
        'authority': 'fls-na.amazon.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'content-type': 'text/plain;charset=UTF-8',
        'accept': '*/*',
        'origin': 'https://www.imdb.com',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.imdb.com/',
        'accept-language': 'hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7'}

    def __init__(self, max_movies=20):
        self.max_movies = max_movies  # Maximum number of top movies taken into consideration for data!

        self.movie_data_dict = {
            "title": [],
            "rating": [],
            "number_of_ratings": [],
            "number_of_oscars": [],
            "title_id": []} # Title_id is needed for oscars, can be removed later!

        self.top_page_data: BeautifulSoup = None

        self.award_data_list = [] # Dedicated for storing award data

        self.movie_dataframe = pd.DataFrame() # Storing the data in dataframes

    def clear_movie_data_dict(self) -> bool:
        """ Handy function for emptying movie data, returns True if successful! """

        for key in self.movie_data_dict: self.movie_data_dict[key].clear()
        return True

    def set_top_page_data(self) -> bool:
        """ Scrapes, parses IMDB top data, returns True if successful! """

        response = requests.get(Scraper.URL, headers=Scraper.REQUEST_HEADERS)
        self.top_page_data = BeautifulSoup(response.text, "lxml")
        return True

    def extract_movie_data(self):
        """ Extracts title, rating, number of ratings from the source of top page. """

        if self.top_page_data is None:
            print("Top page data has not been scraped yet.")
            return False

        movie_data_list = self.top_page_data.find_all("tr")[
                          1:self.max_movies+1]  # First result is irrelevant, could be modified if structure changes

        for movie_data in movie_data_list:
            title = movie_data.find("td", {"class": "titleColumn"}).a.text
            rating = round(float(movie_data.find("span", {"name": "ir"})['data-value']), 1)
            number_of_ratings = int(movie_data.find("span", {"name": "nv"})['data-value'])
            title_id = movie_data.find('div', {'data-recordmetrics': 'true'})['data-tconst']

            self.movie_data_dict['title'].append(title)
            self.movie_data_dict['rating'].append(rating)
            self.movie_data_dict['number_of_ratings'].append(number_of_ratings)
            self.movie_data_dict['title_id'].append(title_id)

        return True

    def get_award_data(self):
        # Oscars are located on a different page unfortunately, they have to be scraped independently..
        # You need to get the title ids and query each page like this
        # https://www.imdb.com/title/tt0111161/awards/
        # From here, you can get the number of awarded oscars...
        # This function scrapes the awards page, you can scrape oscars independently!

        if not self.movie_data_dict['title_id']:
            print("Title ID list cannot be empty.")
            return False


        award_url_list = [f"https://www.imdb.com/title/{title_id}/awards/" for title_id in self.movie_data_dict['title_id']]

        for award_url in award_url_list:
            award_data = BeautifulSoup(requests.get(award_url, headers=Scraper.REQUEST_HEADERS).text, "lxml")
            self.award_data_list.append(award_data)

        return True

    def get_oscars(self):
        """ Extract the count of oscars from the list of award data! """

        # Oscars are ALWAYS located at the top of the page, NO NEED FOR LOOPING!

        if not self.award_data_list:
            print("Award data list cannot be empty.")
            return False

        for award_data in self.award_data_list:
            oscar_data = award_data.find('td', {'class':'title_award_outcome'})
            if oscar_data.b.text == 'Winner':
                self.movie_data_dict['number_of_oscars'].append(int(oscar_data['rowspan']))
            else:
                self.movie_data_dict['number_of_oscars'].append(0)

        return True

    def set_dataframe(self):
        """ Create the DataFrame and set it as the self.movie_dataframe variable """

        self.movie_dataframe = pd.DataFrame(data=self.movie_data_dict)
        return True











        pass

imdb_scraper = Scraper(20)
imdb_scraper.set_top_page_data()
imdb_scraper.extract_movie_data()
imdb_scraper.get_award_data()
imdb_scraper.get_oscars()
imdb_scraper.set_dataframe()
print(imdb_scraper.movie_dataframe)
#self=imdb_scraper
input("ENTER") # breakpoint for the dev!
