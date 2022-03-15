import unittest
from datapao_scraper import Scraper
from datapao_manipulator import DataManipulator
import pandas as pd
from bs4 import BeautifulSoup

scraper_object = Scraper(20)  # A proper object that is suitable for testing the functions
data_manipulator_object = DataManipulator(scraper_object.movie_dataframe)  # Will be reassigned during tests!


class TestAInitParam(unittest.TestCase):
    """ Test if the constructor parameters are INCORRECT """

    def test_scraper(self):
        """ Scraper has to be tested by the extract_movie_data_function """

        bad_scraper = Scraper('20')  # Using string instead of int as constructor parameter
        bad_scraper.set_top_page_data()
        self.assertRaises(TypeError, bad_scraper.extract_movie_data)

    def test_manipulator(self):
        """ DataManipulator will throw an AttributeError at init """

        self.assertRaises(AttributeError, DataManipulator, 123)  # 123 is the constructor parameter for DataManipulator
        bad_manipulator = DataManipulator(pd.DataFrame())  # Constructor parameter is an empty dataframe...
        self.assertRaises(KeyError, bad_manipulator.penalizer_review)  # Key can not be found on an empty dataframe...


class TestBScraperFunctions(unittest.TestCase):
    """ MONOLITHIC TEST FOR EXECUTION SPEED """

    def test_1_dictionary_cleaner(self):
        """ Tests if the dictionary cleaner works correctly... """

        self.assertTrue(scraper_object.clear_movie_data())  # Function executed

        for key in scraper_object.movie_data_dict:
            self.assertFalse(scraper_object.movie_data_dict[key])  # All values in dict are indeed empty

        self.assertFalse(scraper_object.award_data_list)  # Make sure the award data list is empty...
        self.assertIsNone(scraper_object.top_page_data)  # Top page data must be empty!

    def test_2_top_page_scraper(self):
        """ Tests if the top page scraper works correctly regarding data gathering """

        self.assertTrue(scraper_object.set_top_page_data())  # Function executed
        self.assertEqual(type(scraper_object.top_page_data), BeautifulSoup)  # Variable type correct

    def test_3_top_page_data_extractor(self):
        """ Check if the movie data is extractor is working correctly... """

        top_page_data = scraper_object.top_page_data

        scraper_object.top_page_data = None
        self.assertFalse(scraper_object.extract_movie_data())  # Top page data is empty, must return False

        scraper_object.top_page_data = top_page_data  # Reacquire top page data
        self.assertTrue(scraper_object.extract_movie_data())  # Top page data is correct now, if True, function is good

    def test_4_award_data(self):
        """ Test if the scraping of the award data is correct... """

        title_id_list = scraper_object.movie_data_dict['title_id']

        scraper_object.movie_data_dict['title_id'] = []  # Now the title id is an empty list
        self.assertFalse(scraper_object.get_award_data())  # The function must return False now

        scraper_object.movie_data_dict['title_id'] = title_id_list  # Original value reassigned
        self.assertTrue(scraper_object.get_award_data())  # The function must return True now

    def test_5_oscars(self):
        """ Test to make sure the Oscars extraction is working correctly... """

        award_data_list = scraper_object.award_data_list

        scraper_object.award_data_list = []  # Award data list emptied
        self.assertFalse(scraper_object.get_oscars())  # Must return False

        scraper_object.award_data_list = award_data_list  # Original value reassigned
        self.assertTrue(scraper_object.get_oscars())  # Must return True

    def test_6_dataframe(self):
        """ Tests for checking if the dataframe is in correct format... """

        self.assertTrue(scraper_object.set_dataframe())  # Must return True
        self.assertTrue(len(scraper_object.movie_dataframe['title']) == scraper_object.max_movies)  # DF row count must
        # be equal to the max movie number!

    def test_7_full_task(self):
        """ Aggregator/helper function for the simple execution of all the previously tested methods... """

        self.assertTrue(scraper_object.full_task)  # Must return True if execution is successful!


class TestCDataManipulatorFunctions(unittest.TestCase):
    """ MONOLITHIC TEST FOR EXECUTION SPEED """

    def test_1_set_movie_dataframe(self):
        """ Helper function to set the DF in the data_manipulator_object so no need to recall the prev functions """

        global data_manipulator_object
        data_manipulator_object = DataManipulator(scraper_object.movie_dataframe)
        return True

    def test_2_penalizer_review(self):
        """ Tests if the penalizer function executes correctly """

        self.assertTrue(data_manipulator_object.penalizer_review())  # Must return True!

    def test_3_awarder_oscar(self):
        """ Tests if the oscar awarder function executes correctly """

        self.assertTrue(data_manipulator_object.awarder_oscar())  # Must return True!

    def test_4_sorter(self):
        """ Tests if the sorter function for the manipulated dataframe works correctly"""

        self.assertTrue(data_manipulator_object.sort_dataframe())  # Must return True!

    def test_5_saver(self):
        """ Tests if the saver function for works correctly """

        self.assertTrue(data_manipulator_object.save_dataframes())  # Must return True!

    def test_6_full_task(self):
        """ Tests if the aggregator function executes correctly, especially when recalling the previous functions... """

        self.assertTrue(data_manipulator_object.full_task())  # Must return True

    def test_7_dataframe_ratings(self):
        """ Checks if the new ratings are correct in the dataframe... """

        self.assertEqual(round(data_manipulator_object.movie_dataframe['rating'][0], 1),
                         9.7)  # "LOTR" ADJ. RATING 2022-03-15
        self.assertEqual(round(data_manipulator_object.movie_dataframe['rating'][1], 1),
                         9.3)  # "FOR.GUMP" ADJ. RATING 2022-03-15


if __name__ == '__main__':
    unittest.main()
