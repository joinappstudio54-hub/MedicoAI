import json
import time
import re
import os
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


FILE = "urls.json"
OUTPUT = "recipes.json"
IMAGE_DIR = "recipe_images"

# Create image folder automatically
os.makedirs(IMAGE_DIR, exist_ok=True)


# ---------------- DRIVER ----------------
def setup_driver():
    options = Options()

    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )


# ---------------- LOAD URLS ----------------
def load_urls():
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------- HELPERS ----------------
def safe_text(driver, by, value):
    try:
        return driver.find_element(by, value).text.strip()
    except:
        return None


def safe_attr(driver, by, value, attr):
    try:
        return driver.find_element(by, value).get_attribute(attr)
    except:
        return None


# ---------------- CLEAN FILENAME ----------------
def clean_filename(name):
    return re.sub(r'[^a-zA-Z0-9]', '_', name)


# ---------------- DOWNLOAD IMAGE ----------------
def download_image(url, title):

    try:
        if not url:
            return None

        filename = clean_filename(title) + ".jpg"

        filepath = os.path.join(IMAGE_DIR, filename)

        # Skip if already exists
        if os.path.exists(filepath):
            print("Image already exists:", filename)
            return filepath

        response = requests.get(url, timeout=20)

        if response.status_code == 200:

            with open(filepath, "wb") as f:
                f.write(response.content)

            print("Downloaded image:", filename)

            return filepath

    except Exception as e:
        print("Image download error:", e)

    return None


# ---------------- SCRAPE EDAMAM ----------------
def scrape_edamam(driver, url):

    driver.get(url)

    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    time.sleep(2)

    data = {}

    # ---------------- TITLE ----------------
    data["title"] = safe_text(driver, By.TAG_NAME, "h1")

    # ---------------- IMAGE ----------------
    image_url = safe_attr(
        driver,
        By.CSS_SELECTOR,
        "img[itemprop='image']",
        "src"
    )

    data["image"] = image_url

    # Download image immediately
    image_path = download_image(
        image_url,
        data["title"] or f"recipe_{int(time.time())}"
    )

    data["image_path"] = image_path

    # ---------------- INGREDIENTS ----------------
    ingredients = []

    try:
        items = driver.find_elements(
            By.CSS_SELECTOR,
            "li[itemprop='ingredients']"
        )

        for i in items:
            txt = i.text.strip()

            if txt:
                ingredients.append(txt)

    except:
        pass

    data["ingredients"] = ingredients

    # ---------------- INSTRUCTIONS ----------------
    instructions = None

    try:
        btn = driver.find_element(
            By.XPATH,
            "//a[contains(., 'Instructions')]"
        )

        instructions = btn.get_attribute("href")

    except:
        pass

    data["instructions"] = instructions

    # ---------------- NUTRITION ----------------
    nutrition = {}

    try:
        lines = driver.find_elements(
            By.CSS_SELECTOR,
            "#nutrition-list .line"
        )

        for l in lines:

            try:
                key = l.find_element(By.TAG_NAME, "h2").text.strip()

                val = l.text.replace(key, "").strip()

                nutrition[key] = val

            except:
                continue

    except:
        pass

    data["nutrition"] = nutrition

    # ---------------- SOURCE URL ----------------
    data["source_url"] = url

    return data


# ---------------- MAIN ----------------
def run():

    driver = setup_driver()

    urls = load_urls()

    urls = [u for u in urls if u and "recipe=" in u]

    print("Total URLs:", len(urls))

    results = []

    for i, url in enumerate(urls):

        print(f"\n[{i+1}/{len(urls)}] {url}")

        try:

            data = scrape_edamam(driver, url)

            results.append(data)

            # Save incrementally
            with open(OUTPUT, "w", encoding="utf-8") as f:

                json.dump(
                    results,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

            print("Saved:", data.get("title"))

            time.sleep(1)

        except Exception as e:

            print("Error:", e)

            continue

    driver.quit()

    print("\nDONE → Total:", len(results))


if __name__ == "__main__":
    run()