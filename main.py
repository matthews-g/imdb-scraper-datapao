from datapao_scraper import Scraper
from datapao_manipulator import DataManipulator
import pandas as pd

if __name__ == '__main__':
    TOP_MOVIES = 20

    top_scraper = Scraper(TOP_MOVIES)
    top_scraper.full_task()

    top_manipulator = DataManipulator(top_scraper.movie_dataframe)
    top_manipulator.full_task()

    # READ THE DATAFRAMES FROM THE SAVED JSON FILES

    original_dataframe = pd.read_json(top_manipulator.movie_dataframe_org_name)
    modified_dataframe = pd.read_json(top_manipulator.movie_dataframe_name)

    print("\n")
    print("Original dataframe below:")
    print(original_dataframe)
    print("\n")
    print("Modified dataframe below:")
    print(modified_dataframe)
    print("\n")
    input("PRESS ENTER TO EXIT")
    input("PRESS ENTER TO EXIT")

