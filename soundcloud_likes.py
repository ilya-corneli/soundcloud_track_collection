from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import os

def get_track_data(driver):
    tracks_in_this_view = [] # Return a list to preserve order found
    try:
        # Find the container elements first
        container_elements = driver.find_elements(By.CSS_SELECTOR, "li.soundList__item")
        print(f"Found {len(container_elements)} track containers in current view.")

        for container in container_elements:
            try:
                # Find the title link *within* this container
                title_link = container.find_element(By.CSS_SELECTOR, "a.soundTitle__title.sc-link-dark")
                title = title_link.text.strip()
                url = title_link.get_attribute('href')

                if title and url:
                    tracks_in_this_view.append((title, url))
                else:
                    # Optional: Warn if title or URL is empty
                    # print(f"Warning: Found link but title or URL is empty in container: {container.text[:100]}...")
                    pass

            except NoSuchElementException:
                # This container might be an ad or something else without a standard title link
                # print(f"Warning: Could not find title link in container: {container.text[:100]}...")
                pass # Silently ignore containers without the expected title link
            except Exception as e_inner:
                print(f"Error processing a container: {e_inner}")

        # Optional debug print if the list is empty after processing containers
        # if not tracks_in_this_view and len(container_elements) > 0:
        #     print("DEBUG: Found containers but extracted no track data.")

    except Exception as e_outer:
        print(f"Error finding track containers: {e_outer}")

    return tracks_in_this_view

service = Service(r"C:\\files\\MEGA\\it\\Projects\\soundcloud_collection_name\\src\\chromedriver-win64\\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
# Do not initialize driver here yet
# driver = webdriver.Chrome(service=service, options=options)

# Ask user for the SoundCloud likes URL FIRST
likes_url = input("Please enter the full URL of the SoundCloud likes page: ").strip()
print(f"URL entered: {likes_url}")

# NOW initialize the driver
print("Initializing browser...")
driver = webdriver.Chrome(service=service, options=options)
print("Browser initialized.")

# Add a small delay before loading the page
time.sleep(1)

# likes_url = "https://soundcloud.com/matisaxx/likes" # Old hardcoded URL
print(f"Attempting to open URL: {likes_url}")
driver.get(likes_url)

# --- Remove manual cookie acceptance ---
# print("Please accept cookies manually and press Enter when ready...")
# input()

# +++ Add automatic cookie acceptance +++
cookie_button_id = "onetrust-accept-btn-handler"
try:
    print(f"Waiting for cookie accept button (ID: {cookie_button_id})...")
    cookie_wait = WebDriverWait(driver, 15) # Wait up to 15 seconds for the button
    accept_button = cookie_wait.until(
        EC.element_to_be_clickable((By.ID, cookie_button_id))
    )
    accept_button.click()
    print("Cookie button clicked automatically.")
    time.sleep(2) # Short pause after clicking
except TimeoutException:
    print("Cookie accept button did not appear within 15 seconds (might be already accepted or not present).")
except Exception as e:
    print(f"An error occurred while trying to click the cookie button: {e}")
# +++ End automatic cookie acceptance +++

try:
    print("Waiting for main content after handling cookies...")
    wait = WebDriverWait(driver, 60)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "soundList__item")))
    print("Initial content loaded or page ready")
    print("Waiting a few seconds for page to stabilize...")
    time.sleep(5)
except TimeoutException:
    print("Timeout waiting for initial content elements")
    print("DEBUG: Current page title:", driver.title)
    print("DEBUG: Current URL:", driver.current_url)

all_tracks = []
seen_urls = set()
last_height = driver.execute_script("return document.body.scrollHeight")
scroll_pause_time = 8 / 3 # Reduce pause time to approx 2.67 seconds
no_new_tracks_count = 0
max_scrolls = 350 # Increase scroll limit to 350 for large lists
scroll = 0

while scroll < max_scrolls:
    print(f"Scroll attempt {scroll + 1}")

    new_tracks_in_view = get_track_data(driver)

    added_count = 0
    for track_tuple in new_tracks_in_view:
        title, url = track_tuple
        if url not in seen_urls:
            all_tracks.append(track_tuple)
            seen_urls.add(url)
            added_count += 1

    if added_count == 0 and scroll > 0:
        no_new_tracks_count += 1
        print(f"No new unique tracks found in this view. Consecutive empty views: {no_new_tracks_count}")
    else:
        no_new_tracks_count = 0
        if added_count > 0:
             print(f"Added {added_count} new unique tracks from this view.")

    print(f"Total unique tracks collected so far: {len(all_tracks)}")

    if no_new_tracks_count >= 3:
        print("No new unique tracks added for 3 consecutive views. Stopping scroll.")
        break

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("Scrolling down...")
    time.sleep(scroll_pause_time)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        print("Page height did not increase after scroll and wait. Checking again...")
        time.sleep(scroll_pause_time / 2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
             print("Page height still unchanged. Likely end of content. Stopping scroll.")
             break

    last_height = new_height
    scroll += 1

if scroll >= max_scrolls:
    print(f"Reached maximum scroll limit ({max_scrolls}). Stopping.")

csv_filename = "soundcloud_likes.csv"
csv_fullpath = os.path.abspath(csv_filename)
print(f"\nAttempting to write CSV to: {csv_fullpath}")
try:
    with open(csv_fullpath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'URL'])
        for title, url in all_tracks:
            writer.writerow([title, url])
    print(f"\nSuccessfully wrote {len(all_tracks)} tracks to {csv_fullpath}")
except IOError as e:
    print(f"\nError writing to CSV file {csv_fullpath}: {e}")

print("\nFinal track list (in order found):")
if not all_tracks:
    print("No tracks found.")
else:
    for i, (title, url) in enumerate(all_tracks):
        print(f"{i+1}. {title} - {url}")
print(f"\nTotal unique tracks collected: {len(all_tracks)}")

driver.quit()
print("Browser closed")