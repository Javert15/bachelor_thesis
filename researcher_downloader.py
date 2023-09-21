import webbrowser


first_page=0
last_page=24

for page in range(first_page, last_page):
    url = f"https://research.wu.ac.at/de/persons/?showAdvanced=false&allConcepts=true&inferConcepts=true&originalSearch=&improvedLayoutOrganisationUuid=&format=&publicationYearsOld=10&publicationYear=2014&publicationYear=2015&publicationYear=2016&publicationYear=2017&publicationYear=2018&publicationYear=2019&publicationYear=2020&publicationYear=2021&publicationYear=2022&publicationYear=2023&nofollow=true&page={page}&export=xls"
    webbrowser.open(url)
    print(url)