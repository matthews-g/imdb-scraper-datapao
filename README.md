# imdb-scraper-datapao
IMDB top movies scraper and data manipulation tool created for Datapao.
![Screenshot of success](https://github.com/matthews-g/imdb-scraper-datapao/blob/master/datapao_scraper_success.PNG)

## Installation
- [Create virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
- Clone repo `git clone https://github.com/matthews-g/imdb-scraper-datapao.git`
- Install requirements: `pip install requirements.txt`

## Usage
- [Lazy to read? Check main.py for example usage.](https://github.com/matthews-g/imdb-scraper-datapao/blob/master/main.py)

The project contains two important modules.
- **Scraper**
- **Manipulator**

The **Scraper** module/class, is created for the scraping related tasks, which (in this case) means scraping the data of the top 20 movies, getting award data for each of them, where it extracts the won oscars.
The extracted data is stored in a Pandas DataFrame, where the Manipulator will make use of it.

The **Manipulator** module/class is created for the data manipulation-related tasks, which (in this case) means manipulating the review score based on review count and won oscars.
After these calculations are completed, the DataFrame will be sorted and saved, alongside the original, unmodified DataFrame, in a JSON format (in the working directory).

Both of the classes contain a function `full_task`, which executes all the required tasks for the completion of the assignment. You only have to use this function. As I have written before, check [main.py](https://github.com/matthews-g/imdb-scraper-datapao/blob/master/main.py) for reference.
The `full_task` cleans the relevant data before scraping it, so it avoids duplicated elements, making it suitable for continuous scraping in a loop (execute every 5 minutes for example, as you wish...).

## Tests

The monolithic unit tests can be executed with
`python -m unittest datapao_tester.py`.
It must pass all 16 tests to work correctly, which involve invalid input data, checks of the correct working of the methods, and the mathematical correctness of the calculated data. The latter could differ due to exposure to changes regarding ratings.
