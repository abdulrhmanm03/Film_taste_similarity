from bs4 import BeautifulSoup
import requests

ratings_map = {
        '½': 1,
        '★': 2,
        '★½': 3,
        '★★': 4,
        '★★½': 5,
        '★★★': 6,
        '★★★½': 7,
        '★★★★': 8,
        '★★★★½': 9,
        '★★★★★': 10
}

user_data = {}

def main(soup):
        poster_container = soup.find_all(class_ = 'poster-container')

        for film in poster_container:
            if film.find(class_="rating"):
                poster = film.find(class_='poster')
                film_id = poster.get('data-film-id')
                rating = film.find(class_="rating").text
                user_data[film_id] = ratings_map[rating]

def scrap(username, q):
    
    url = f'https://letterboxd.com/{username}/films/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    print(f"getting {username} data....")
    main(soup)
    paginate_page = soup.find_all(class_ = "paginate-page")
    if paginate_page:
        n = int(paginate_page[-1].text)
        for i in range(2, n+1):
            
            url = f'https://letterboxd.com/{username}/films/page/{i}'
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            main(soup)
       
    
    q.put(user_data)
    print(f"{username} done") 