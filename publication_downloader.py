import webbrowser
import time


first_page=0
last_page=234

for page in range(first_page, last_page):
    url = f"https://research.wu.ac.at/de/publications/?publicationYear=2021&publicationYear=2022&publicationYear=2020&publicationYear=2019&publicationYear=2018&nofollow=true&format=&page={page}&export=xls"
    webbrowser.open(url)
    print(url)
    time.sleep(0.5)