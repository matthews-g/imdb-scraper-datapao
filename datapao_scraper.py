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
            "title_id": []}  # Title_id is needed for oscars, can be removed later!

        self.top_page_data: BeautifulSoup = None # The data of the top page will be stored here.

        self.award_data_list = []  # Dedicated for storing award data.

        self.movie_dataframe = pd.DataFrame()  # Storing the data in dataframe.

    def clear_movie_data_dict(self) -> bool:
        """ Handy function for emptying movie data """

        for key in self.movie_data_dict: self.movie_data_dict[key].clear()

        print("Dictionary of the movie data have been cleaned!")
        return True

    def set_top_page_data(self) -> bool:
        """ Scrapes, parses IMDB top page data """

        response = requests.get(Scraper.URL, headers=Scraper.REQUEST_HEADERS, timeout=3)
        self.top_page_data = BeautifulSoup(response.text, "lxml")

        print("Top page data have been scraped!")
        return True

    def extract_movie_data(self) -> bool:
        """ Extracts title, rating, number of ratings from the source of top page. """

        if self.top_page_data is None:
            print("Top page data have not been scraped yet.")
            return False

        movie_data_list = self.top_page_data.find_all("tr")[1:self.max_movies + 1]  # First result is irrelevant

        for movie_data in movie_data_list:
            title = movie_data.find("td", {"class": "titleColumn"}).a.text
            rating = round(float(movie_data.find("span", {"name": "ir"})['data-value']), 1)
            number_of_ratings = int(movie_data.find("span", {"name": "nv"})['data-value'])
            title_id = movie_data.find('div', {'data-recordmetrics': 'true'})['data-tconst']

            self.movie_data_dict['title'].append(title)
            self.movie_data_dict['rating'].append(rating)
            self.movie_data_dict['number_of_ratings'].append(number_of_ratings)
            self.movie_data_dict['title_id'].append(title_id)

        print("Movie data have been extracted from the top page data!")
        return True

    def get_award_data(self) -> bool:
        """ Gets the award data of all the movies, not limited to Oscar wins... """

        if not self.movie_data_dict['title_id']:
            print("Title ID list cannot be empty.")
            return False

        award_url_list = [f"https://www.imdb.com/title/{title_id}/awards/" for title_id in
                          self.movie_data_dict['title_id']]

        print("\n") # The first iteration print will look better :)

        for award_index, award_url in enumerate(award_url_list):
            print(f"Scraping award data for movie {award_index+1}/{self.max_movies}")
            print(f"URL: {award_url}")
            print("\n")
            award_data = BeautifulSoup(requests.get(award_url, headers=Scraper.REQUEST_HEADERS, timeout=3).text, "lxml")
            self.award_data_list.append(award_data)

        print("Award data have been scraped for all movies.")
        return True

    def get_oscars(self) -> bool:
        """ Extract the count of oscars from the list of award data! """
        # Oscars are ALWAYS located at the top of the page, NO NEED FOR LOOPING!

        if not self.award_data_list:
            print("Award data list cannot be empty.")
            return False

        for award_data in self.award_data_list:
            oscar_data = award_data.find('td', {'class': 'title_award_outcome'})
            if oscar_data.b.text == 'Winner':
                self.movie_data_dict['number_of_oscars'].append(int(oscar_data['rowspan']))
            else:
                self.movie_data_dict['number_of_oscars'].append(0)

        print("Oscars have been extracted!")
        return True

    def set_dataframe(self) -> bool:
        """ Create the DataFrame and set it as the self.movie_dataframe variable """

        self.movie_dataframe = pd.DataFrame(data=self.movie_data_dict)
        self.movie_dataframe.drop('title_id', inplace=True, axis=1)

        print("Movie dataframe has been created!")
        return True

    def full_task(self) -> bool:
        """ Executing the full task as requested by Datapao... """
        self.set_top_page_data()
        self.extract_movie_data()
        self.get_award_data()
        self.get_oscars()
        self.set_dataframe()

        print("All required scraping tasks have been completed.")
        return True
