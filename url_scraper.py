import json
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


SEARCH_TERM = "biryani"
OUTPUT_FILE = "urls.json"


def setup_driver():
    options = Options()

    # Uncomment if you want headless mode
    # options.add_argument("--headless=new")

    options.add_argument("--start-maximized")

    return webdriver.Chrome(options=options)


def click_show_more(driver):
    xpaths = [
        "//*[contains(text(),'Show More')]",
        "//*[contains(text(),'Show more')]",
        "//button[contains(.,'Show More')]",
        "//button[contains(.,'Show more')]"
    ]

    for xpath in xpaths:
        try:
            elements = driver.find_elements(By.XPATH, xpath)

            if elements:
                btn = elements[-1]

                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    btn
                )

                time.sleep(1)

                driver.execute_script(
                    "arguments[0].click();",
                    btn
                )

                print("Clicked Show More")

                return True

        except:
            pass

    return False


def scroll_until_end(driver):
    same_count = 0
    last_height = 0

    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

        time.sleep(3)

        click_show_more(driver)

        time.sleep(2)

        new_height = driver.execute_script(
            "return document.body.scrollHeight"
        )

        print("Height:", new_height)

        if new_height == last_height:
            same_count += 1
        else:
            same_count = 0

        if same_count >= 5:
            print("Reached end")
            break

        last_height = new_height


def extract_urls(driver):
    urls = set()

    # From links
    links = driver.find_elements(By.TAG_NAME, "a")

    for link in links:
        href = link.get_attribute("href")

        if href and "/results/recipe/?recipe=" in href:
            urls.add(href.split("#")[0])

    # From page source
    html = driver.page_source

    matches = re.findall(
        r'https://www\.edamam\.com/results/recipe/\?recipe=[^"\']+',
        html
    )

    urls.update(matches)

    return sorted(urls)


def main():
    url = (
        f"https://www.edamam.com/results/recipes/?search={SEARCH_TERM}"
    )

    driver = setup_driver()

    try:
        print("Opening:", url)

        driver.get(url)

        time.sleep(8)

        scroll_until_end(driver)

        recipe_urls = extract_urls(driver)

        print(f"\nTotal URLs Found: {len(recipe_urls)}")

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                recipe_urls,
                f,
                indent=2,
                ensure_ascii=False
            )

        print(f"Saved to {OUTPUT_FILE}")

        for u in recipe_urls[:20]:
            print(u)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()