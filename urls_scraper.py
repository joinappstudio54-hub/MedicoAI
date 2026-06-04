import json
import os
import re
import time
import random
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Full list of terms provided by user
SEARCH_TERM = [
    "Asparagus", "Apple", "Apricot", "Anchovies", "Applesauce", "Artichokes", "Almonds",
    "Angel hair pasta", "Acai berry", "Avocado", "Almond butter", "Alfredo sauce", "Beef",
    "Beans", "Broccoli", "Beets", "Barley", "Biscuits", "Bread", "Bagel", "Burger", "Butter",
    "Burrito", "Banana", "Blackberry", "Blueberry", "Basil", "Bok choy", "Broccolini", "Beverages",

    "Aloo Gobi",         
    "Biryani",          
    "Butter Chicken",   
    "Barfi",
    "Chaat",
    "Sabzi",          
    "Chana Masala",    
    "Curry",  
    "Chicken Korma",    
    "Chapli Kabab",   
    "Daal Makhani",    
    "Gulab Jamun",     
    "Sweets",          
    "Kheer",          
    "Lassi",            
    "Karahi",   
    "Paneer Tikka",     
    "Palak Paneer", 
    "Paneer", 
    "Pulao",    
    "Kofta", 
    "Malai",        
    "Roti",            
    "Kabab",
    "Kebabs",      
    "Tikka Masala",   
    "Juices",
    "Corn",
    "Buns",
    # --------------------------------------
    "Brown rice", "Brioche", "Balsamic dressing", "Corn", "Carrots", "Cabbage", "Cauliflower",
    "Crab", "Cookies", "Cucumber", "Croutons", "Cantaloupe", "Clams",
    "Cashews", "Coconut", "Coffee", "Cod", "Caramel", "Cocoa", "Cream cheese",
    "Couscous", "Chickpeas", "Cereal", "Celery", "Cinnamon",
    "Cilantro", "Ceviche", "Tortilla chips", "Cheese", "Cherry", "Chicken", "Chili",
    "Peanut butter", "Chocolate", "Cheddar cheese", "Chocolate chips", "Cookies","Croissants","Mini croissants","Cupcakes",
    "Cheesecake", "Chutney", "Churros", "Chia seeds", "Donut",
    "Danish pastry", "Drumsticks", "Durian", "Dairy", "Deviled eggs", "Dill",
    "Dill pickles", "Dark chocolate", "Dates", "Dim sum", "Dragonfruit",
    "Dumplings", "Dijon mustard", "Eggs", "Eggplant", "Endive", "Egg roll",
    "Espresso", "English muffin", "Elbow macaroni", "Eggnog", "Enchiladas",
    "Edamame", "Elderberry", "Fish", "French fries", "Fruit", "Fajitas",
    "French toast", "Figs", "Fudge", "Fritters", "Frosting", "Fettuccine",
    "Falafel", "Feta cheese", "Flour", "Flax seeds", "Focaccia",
    "Farmer's cheese", "Gelatin", "Ginger", "Ginger ale", "Ginger bread",
    "Gelato", "Garlic", "Gravy", "Green beans", "Grapes", "Granola",
    "Grapefruit", "Guacamole", "Grapeseed oil", "Green olives", "Garlic bread",
    "Goat milk", "Gyoza", "Guava", "Gumbo", "Gouda cheese", "Gnocchi",
    "Horseradish", "Hamburger", "Hot dog", "Honeydew melon", "Halibut",
    "Honey", "Hot chocolate", "Ketchup", "Hollandaise sauce", "Hummus",
    "Herbs", "Hash browns", "Ice cream", "Iced tea", "Icing",
    "Iceberg lettuce", "Italian bread", "Irish stew",
    "Instant coffee", "Instant oatmeal", "Italian dressing", "Juice", "Jelly",
    "Jam", "Jerky", "Jalapeño", "Jambalaya", "Jasmine rice", "Jackfruit",
    "Jicama", "Kale", "Kiwi", "Korma", "Kidney beans", "Kumquat", "Kimchi",
    "Kombucha", "Lima beans", "Leeks", "Lentils", "Liver", "Lettuce",
    "Lasagna", "Lemons", "Limes", "Lobster", "Linguine", "Lemonade", "Lamb",
    "Legumes", "Licorice", "Lemongrass","Momos", "Mustard", "Macaroni", "Mushroom",
    "Milk", "Melon", "Muffin", "Marshmallows", "Mozzarella", "Mango",
    "Marmalade", "Mahi mahi", "Minestrone", "Margarine", "Maple syrup",
    "Mayonnaise", "Mashed potatoes", "Mackerel", "Miso", "Manicotti",
    "Mousse", "Meatloaf", "Millet", "Matcha", "Noodles", "Nuts", "Nachos",
    "Nectarines", "Chicken nuggets", "Naan bread", "Nori seaweed", "Nutella",
    "Onion", "Okra", "Orange", "Oatmeal", "Omelet", "Olives", "Oysters",
    "Octopus", "Oregano", "Oat milk", "Onion rings", "Oyster mushrooms",
    "Pickles", "Peas", "Potato", "Potato chips", "Parsley", "Pumpkin",
    "Peppers", "Parsnips", "Popcorn", "Pistachios", "Pie",
    "Peanuts", "Pudding", "Peaches", "Pears", "Plum", "Prunes",
    "Pancake", "Pastry", "Pineapple", "Peppermint", "Papaya",
    "Pretzels", "Pecans", "Pine nuts", "Perogies",
    "Pimentos", "Pinto beans", "Paprika", "Parmesan cheese",
    "Prawns", "Poutine", "Protein bars", "Passionfruit",
    "Plantain", "Pesto", "Peking duck", "Paella", "Pita bread",
    "Polenta", "Quiche", "Quail", "Quince",
    "Quesadilla", "Quinoa", "Rutabaga", "Rhubarb", "Radish",
    "Ribs", "Rolls", "Rye bread", "Raspberry", "Ravioli",
    "Rigatoni", "Raisins", "Ratatouille", "Relish", "Romaine lettuce",
    "Red lentils", "Refried beans", "Risotto", "Ramen",
    "Radicchio", "Ricotta cheese", "Romano cheese", "Spinach",
    "Squash", "Soybean", "Steak", "Spaghetti", "Swiss cheese",
    "Sandwich", "Scallops", "Sushi", "Sauce",
    "Sundae", "Stuffing", "Strawberry", "Snow peas",
    "Stew", "Salmon", "Sunflower seeds", "Swordfish", "Squid",
    "Sesame seeds", "Swiss chard", "Sour cream", "Sardines",
    "Salsa", "Tzatziki", "Souvlaki", "Sashimi", "Sesame oil",
    "Spinach dip", "Sweet potato", "Smoothie", "Samosa",
    "Snapper", "Split peas", "Scones", "Sorbet", "String cheese",
    "Souffle", "Sourdough bread", "Shish kabob", "Pasta shells",
    "Shepherd's pie", "Shrimp", "Sherbet", "Shallot",
    "Shredded wheat",
    "Shiitake mushrooms", "Tomato", "Turnip", "Turkey",
    "Tapioca", "Toast", "Taco", "Tuna", "Tortillas",
    "Tangerine", "Tabasco sauce", "Tamale", "Tater tots",
    "Tempura", "Tofu", "Tempeh", "Tortellini", "Tamarind",
    "Tabbouleh", "Teriyaki", "Torte", "Trifle", "Truffle",
    "Turmeric", "Tahini", "Thighs", "Thyme",
    "Upside-down cake", "Udon noodles", "Venison", "Veal",
    "Vermicelli", "Vinegar", "Vanilla", "Vine leaves",
    "Vinaigrette", "Watercress", "Wax beans", "Watermelon",
    "Wheat bread", "Chicken wings", "Waffles", "Walnuts",
    "Wafers", "Water", "Wontons", "Wasabi", "Wild rice",
    "Yam", "Yellow squash", "Yogurt", "Egg yolk",
    "Yellow beans", "Yucca", "Zucchini",
    "Ziti", "Zested lemon", "Pasta",

    # Dish Types
    "Biscuits and cookies", "Cereals", "Condiments and sauces",
    "Desserts", "Drinks", "Egg", "Ice cream and custard",
    "Main course", "Pies and tarts",
    "Preps", "Preserve", "Seafood", "Side dish",
    "Special occasions", "Starter", "Breakfast", "brunch", "Lunch/Dinner", "Snack", "Teatime",

    # Cuisines
    "American", "Asian", "British", "Caribbean",
    "Central Europe", "Chinese", "Eastern Europe",
    "French", "Greek", "Indian", "Italian",
    "Japanese", "Korean", "Kosher", "Mediterranean",
    "Mexican", "Middle Eastern", "Nordic",
    "South American", "South East Asian", "World"
]

OUTPUT_FILE = "urls.json"
PROGRESS_FILE = "progress.json"

def setup_driver():
    options = Options()
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
            for btn in elements:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                    time.sleep(random.uniform(1.2, 2.0))
                    driver.execute_script("arguments[0].click();", btn)
                    print("Clicked 'Show More'")
                    return True
        except Exception:
            pass
    return False

def scroll_until_end(driver):
    same_count = 0
    last_height = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2.5, 4.0))

        click_show_more(driver)
        time.sleep(1.5)

        new_height = driver.execute_script("return document.body.scrollHeight")
        print("Current Page Height:", new_height)

        if new_height == last_height:
            same_count += 1
        else:
            same_count = 0

        if same_count >= 5:
            print("Reached the end of pagination for this term.")
            break
        last_height = new_height

def extract_recipe_urls(driver, keyword):
    urls = set()
    keyword_suffix = f"/search={keyword.lower().replace(' ', '-')}"

    # 1. Parse using standard href attributes (Reliable)
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        try:
            href = link.get_attribute("href")
            if href and "/results/recipe/?recipe=" in href:
                base_recipe_url = href.split("#")[0].split("&")[0]
                # Ensure clean formatting append
                urls.add(f"{base_recipe_url}{keyword_suffix}")
        except Exception:
            continue

    # 2. Raw HTML fallback matching
    html = driver.page_source
    matches = re.findall(r'https://www\.edamam\.com/results/recipe/\?recipe=[^"\']+', html)
    for match in matches:
        base_recipe_url = match.split("#")[0].split("&")[0]
        urls.add(f"{base_recipe_url}{keyword_suffix}")

    return list(urls)

def main():
    master_dict = {}
    completed_keywords = []

    # State Recovery Checkpoint Integration
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                master_dict = json.load(f)
                print(f"[RECOVERY] Loaded existing categorical items from {OUTPUT_FILE}.")
        except Exception:
            print("[RECOVERY WARNING] Resetting execution output matrix dict object structures.")

    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                completed_keywords = json.load(f)
                print(f"[RECOVERY] {len(completed_keywords)} categories verified complete. Skipping items.")
        except Exception:
            completed_keywords = []

    driver = setup_driver()

    try:
        for term in SEARCH_TERM:
            if term in completed_keywords:
                print(f"Skipping completed term lookup mapping: '{term}'")
                continue

            encoded_term = quote(term)
            url = f"https://www.edamam.com/results/recipes/?search={encoded_term}"
            
            print(f"\n--- Initiating targeted keyword context category: {term} ---")
            driver.get(url)
            
            # Allow page to fully execute scripts initially
            time.sleep(random.uniform(5.5, 7.5))

            # Scroll completely to the absolute end of the page before extraction
            scroll_until_end(driver)
            
            # Extract everything once the target page is fully expanded
            term_urls = extract_recipe_urls(driver, term)
            
            # Save into dictionary map format requested
            master_dict[term.lower()] = sorted(term_urls)
            completed_keywords.append(term)
            
            print(f"Scraped Category '{term}': Added {len(term_urls)} references.")

            # Live Incremental Saving Checkpoint
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(master_dict, f, indent=2, ensure_ascii=False)

            with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
                json.dump(completed_keywords, f, indent=2, ensure_ascii=False)
                
            time.sleep(random.uniform(4.0, 6.0))

        print(f"\nSUCCESS: Processing completed cleanly! Categorical dictionary object stored in {OUTPUT_FILE}.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()