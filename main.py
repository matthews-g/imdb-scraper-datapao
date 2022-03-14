from datapao_scraper import Scraper
from datapao_manipulator import DataManipulator

toptwenty = Scraper(20)
toptwenty.full_task()
print(toptwenty.movie_dataframe)

toptwenty_manipulator = DataManipulator(toptwenty.movie_dataframe)
toptwenty_manipulator.full_task()
print(toptwenty_manipulator.movie_dataframe)

