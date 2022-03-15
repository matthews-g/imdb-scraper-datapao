import pandas as pd


class DataManipulator:

    REVIEW_DEVIATION_THRESHOLD = 100000
    REVIEW_POINT_DEDUCT = 0.1

    OSCAR_METRICS = {
        # Key = Threshold for won oscar count, Value = Addition to the review score.
        2: 0.3,
        5: 0.5,
        10: 1, 
        11: 1.5 # From 11 oscars and beyond, 1.5 points will be added
    }

    def __init__(self, movie_dataframe: pd.DataFrame):
        self.movie_dataframe = movie_dataframe
        self.movie_dataframe_org = movie_dataframe.copy()  # Making a copy of the original DF

        movie_df_len = len(movie_dataframe)
        self.movie_dataframe_name = f'imdb_top_{movie_df_len}_manipulated.json'
        self.movie_dataframe_org_name = f'imdb_top_{movie_df_len}_original.json'

    def penalizer_review(self) -> bool:
        """ Penalizes the rating by the deviation counts of 100 000 from the top rating score """

        max_reviews = self.movie_dataframe['number_of_ratings'].max()

        penalty_points = [int(((max_reviews - rating_number) / DataManipulator.REVIEW_DEVIATION_THRESHOLD)) *
                          DataManipulator.REVIEW_POINT_DEDUCT
                          for rating_number in self.movie_dataframe['number_of_ratings']]

        self.movie_dataframe['rating'] = [v - penalty_points[i] for i, v in self.movie_dataframe['rating'].iteritems()]

        print("Penalizing the score by review numbers have been completed.")
        return True

    def awarder_oscar(self) -> bool:
        """ Awards the rating plus points according to the number of oscars of a given movie! """

        oscar_reward_points = []
        max_key = max(DataManipulator.OSCAR_METRICS.keys())

        for index, oscar_number in self.movie_dataframe['number_of_oscars'].iteritems():
            if oscar_number <= 0:
                oscar_reward_points.append(0)
                continue

            elif oscar_number >= max_key:
                oscar_reward_points.append(DataManipulator.OSCAR_METRICS[max_key])
                continue

            for oscar_points in DataManipulator.OSCAR_METRICS:
                if oscar_number <= oscar_points:
                    oscar_reward_points.append(DataManipulator.OSCAR_METRICS[oscar_points])
                    break

        self.movie_dataframe['rating'] = [v + oscar_reward_points[i]
                                          for i, v in self.movie_dataframe['rating'].iteritems()]

        print("Rating awarder based on won Oscars have been completed!")
        return True

    def sort_dataframe(self) -> bool:
        """ Sorting modified data by the new ratings """

        self.movie_dataframe.sort_values(by='rating', ascending=False, inplace=True, ignore_index=True)

        print("Movie dataframe has been sorted by rating (descending).")
        return True

    def save_dataframes(self) -> bool:
        """ This function saves both the original and modified dataframes..."""
        # For the correct format of Hungarian characters, this approach is required.

        with open(self.movie_dataframe_name, 'w', encoding='utf-8') as file:
            self.movie_dataframe.to_json(file, force_ascii=False)

        with open(self.movie_dataframe_org_name, 'w', encoding='utf-8') as file:
            self.movie_dataframe_org.to_json(file, force_ascii=False)

        print("Original and manipulated dataframes have been saved as JSON!")
        return True

    def full_task(self):
        """ Executing the full task as requested by Datapao... """

        self.penalizer_review()
        self.awarder_oscar()
        self.sort_dataframe()
        self.save_dataframes()

        print("All the data manipulation tasks requested by Datapao have been executed successfully.")
        return True  # When everything has executed successfully!
