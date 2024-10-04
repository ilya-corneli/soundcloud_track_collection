import requests
from bs4 import BeautifulSoup

def get_liked_tracks(url):
    """
    Функция для получения информации о понравившихся треках с SoundCloud.

    Args:
        url: URL страницы с лайками пользователя.

    Returns:
        Список словарей, где каждый словарь содержит информацию о треке 
        (исполнитель и название).
    """
    tracks = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for item in soup.find_all("li", class_="soundList__item"):
        artist = item.find("a", class_="soundTitle__username").text.strip()
        title = item.find("a", class_="sc-link-primary").text.strip()
        tracks.append({"artist": artist, "title": title})
    return tracks

# Замените на URL вашей страницы с лайками
likes_url = "https://soundcloud.com/ilyacorneli/likes" 

all_tracks = []
# SoundCloud загружает контент динамически, поэтому нужно обрабатывать несколько страниц
while likes_url:
    tracks = get_liked_tracks(likes_url)
    all_tracks.extend(tracks)

    # Поиск ссылки на следующую страницу
    next_page_link = soup.find("a", class_="  pagination-next")
    if next_page_link:
        likes_url = "https://soundcloud.com" + next_page_link["href"] 
    else:
        likes_url = None

# Вывод информации о треках
for track in all_tracks:
    print(f"Artist: {track['artist']}, Track: {track['title']}") 