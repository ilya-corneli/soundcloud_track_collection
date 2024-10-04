from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def get_track_titles(driver):
    titles = set()
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, "a.sc-link-primary.soundTitle__title")
        for element in elements:
            title = element.text.strip()
            if title:
                titles.add(title)
        print(f"Found {len(titles)} titles in this iteration")
        if len(titles) == 0:
            print("DEBUG: Page source snippet:")
            print(driver.page_source[:1000])
    except Exception as e:
        print(f"Error in get_track_titles: {e}")
    return titles

service = Service(r"C:\Windows\System32\chromedriver-win64\chromedriver-win64\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

likes_url = "https://soundcloud.com/matisaxx/likes"
driver.get(likes_url)
print(f"Opened URL: {likes_url}")

print("Please accept cookies manually and press Enter when ready...")
input()

try:
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "soundList__item")))
    print("Initial content loaded")
except TimeoutException:
    print("Timeout waiting for initial content to load")
    print("DEBUG: Current page title:", driver.title)
    print("DEBUG: Current URL:", driver.current_url)

all_titles = set()
last_height = driver.execute_script("return document.body.scrollHeight")
scroll_pause_time = 5
no_new_tracks_count = 0
max_scrolls = 10

for scroll in range(max_scrolls):
    print(f"Scroll attempt {scroll + 1}")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

    new_titles = get_track_titles(driver)

    if len(new_titles - all_titles) == 0:
        no_new_tracks_count += 1
        print(f"No new tracks found. Count: {no_new_tracks_count}")
    else:
        no_new_tracks_count = 0
        print(f"Found {len(new_titles - all_titles)} new tracks")

    all_titles.update(new_titles)
    print(f"Total unique tracks so far: {len(all_titles)}")

    if no_new_tracks_count >= 3:
        print("No new tracks for 3 consecutive scrolls. Stopping.")
        break

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        print("Page height didn't change. Stopping.")
        break
    last_height = new_height

print("\nFinal results:")
for title in sorted(all_titles):
    print(title)

print(f"\nTotal unique tracks: {len(all_titles)}")

driver.quit()
print("Browser closed")