from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def get_liked_tracks(driver):
    """
    Функция для получения информации о понравившихся треках.
    """
    tracks = []
    soup = BeautifulSoup(driver.page_source, "html.parser")

    for item in soup.find_all("li", class_="soundList__item"):
        artist = item.find("a", class_="soundTitle__username").text.strip()
        title = item.find("a", class_="sc-link-primary").text.strip()
        tracks.append({"artist": artist, "title": title})
    return tracks

# Инициализация WebDriver (замените на путь к вашему ChromeDriver)
service = Service(r"C:\Windows\System32\chromedriver-win64\chromedriver-win64\chromedriver.exe")  # Используем сырую строку для пути
driver = webdriver.Chrome(service=service)

# Замените на URL вашей страницы с лайками
likes_url = "https://soundcloud.com/ilyacorneli/likes"
driver.get(likes_url)

# Ожидание загрузки начального контента
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "soundList__item")))

all_tracks = []
# Прокрутка страницы вниз и загрузка новых треков
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Дайте время на загрузку новых элементов

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

    tracks = get_liked_tracks(driver)
    all_tracks.extend(tracks)

# Вывод информации о треках
for track in all_tracks:
    print(f"Artist: {track['artist']}, Track: {track['title']}")

driver.quit()