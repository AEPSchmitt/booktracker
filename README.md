# Booktracker
Keep track of the books you read using [Google Sheets](https://docs.google.com/spreadsheets/d/1SmtFQJw4FF7adj_B1clWbI8AHtPOJHwa4bOvNHtAcXE/copy).
Export the sheet as **bookstats.csv** and feed that to **booktracker.py** for some interactive stats about your reading history.

# Requirements
0. Python libraries: [**Plotly**](https://pypi.org/project/plotly/), [**Pillow**](https://pypi.org/project/Pillow/), [**pandas**](https://pypi.org/project/pandas/)
1. A CSV file named [**bookstats.csv**](https://docs.google.com/spreadsheets/d/1SmtFQJw4FF7adj_B1clWbI8AHtPOJHwa4bOvNHtAcXE/copy) with the following format:
   
| Title  | Series | Author | Author Gender | Pages  | Release year | Start date  | Finish date | Pages accumulated  | Avg. Pages per day | Bechdel  | Formatted start date |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| string  | string  | string  | F/M  | int | int | YYYY-MM-DD | YYYY-MM-DD | int | int | Y/N | Month DD, YYYY |

( [download starter here](https://docs.google.com/spreadsheets/d/1SmtFQJw4FF7adj_B1clWbI8AHtPOJHwa4bOvNHtAcXE/copy) )

2. Cover images for each book as **.png** files, placed in the **/covers/** folder. Covers have to be named exactly the same as the book title, but without capital letters and with spaces replaced by __underscores__). Like this:
![bookcovers_example](https://github.com/AEPSchmitt/booktracker/assets/9079958/7c8c4c30-ef50-4940-aac4-1b3217be3430)

# Example
[A live example can be found here](https://aepschmitt.dk/books/timeline/)


