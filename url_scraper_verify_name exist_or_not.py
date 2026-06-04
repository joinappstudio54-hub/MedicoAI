import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# The final, optimized list of modern foods from Food_Alphabet_Cheat_sheet_2.pdf
# final_food_list = [
#     "Asparagus", "Apple", "Apricot", "Anchovies", "Applesauce", "Artichokes", "Almonds", 
#     "Angel hair pasta", "Acai berry", "Avocado", "Almond butter", "Alfredo sauce", "Beef", 
#     "Beans", "Broccoli", "Beets", "Barley", "Bacon", "Biscuits", "Bread", "Bagel", "Burger", "Butter", 
#     "Burrito", "Banana", "Blackberry", "Blueberry", "Basil", "Bok choy", "Broccolini", 
#     "Brown rice", "Brioche", "Balsamic dressing", "Corn", "Carrots", "Cabbage", "Cauliflower", 
#     "Crab", "Cookies", "Cucumber", "Croutons", "Cantaloupe", "Clams", "Cranberry sauce", 
#     "Cashews", "Coconut", "Coffee", "Cod", "Caramel", "Cocoa", "Cream cheese", "Cranberries", 
#     "Couscous", "Chickpeas", "Cereal", "Cider", "Celery", "Cinnamon", "Caesar salad", 
#     "Cilantro", "Ceviche", "Tortilla chips", "Cheese", "Cherry", "Chicken", "Chili", 
#     "Cheeseburger", "Peanut butter", "Chocolate", "Cheddar cheese", "Chocolate chips", 
#     "Cheesecake", "Chutney", "Churros", "Chorizo", "Chia seeds", "Duck", "Donut", "Danish pastry", 
#     "Drumsticks", "Durian", "Dairy", "Deviled eggs", "Dill", "Dill pickles", "Dark chocolate", 
#     "Dates", "Dim sum", "Dragonfruit", "Dumplings", "Dijon mustard", "Eggs", "Eggplant", 
#     "Endive", "Egg roll", "Espresso", "English muffin", "Elbow macaroni", "Eggnog", 
#     "Enchiladas", "Edamame", "Elderberry", "Fish", "French fries", "Fruit", "Fajitas", 
#     "French toast", "Figs", "Fudge", "Fritters", "Frosting", "Fettuccine", "Falafel", 
#     "Feta cheese", "Flour", "Flax seeds", "Focaccia", "Fried rice", "Farmer's cheese", 
#     "Gelatin", "Ginger", "Ginger ale", "Ginger bread", "Gelato", "Garlic", "Gravy", 
#     "Green beans", "Grapes", "Granola", "Grapefruit", "Guacamole", "Grapeseed oil", 
#     "Green olives", "Garlic bread", "Goat milk", "Gyoza", "Guava", "Gumbo", "Gouda cheese", 
#     "Gnocchi", "Ham", "Horseradish", "Hamburger", "Hot dog", "Honeydew melon", "Halibut", 
#     "Honey", "Hot chocolate", "Ketchup", "Hollandaise sauce", "Hummus", "Herbs", "Hash browns", 
#     "Ice cream", "Iced tea", "Icing", "Iceberg lettuce", "Italian bread", "Curry", "Irish stew", 
#     "Instant coffee", "Instant oatmeal", "Italian dressing", "Juice", "Jelly", "Jam", "Jerky", 
#     "Jalapeño", "Jambalaya", "Jasmine rice", "Jackfruit", "Jicama", "Kale", "Kiwi", "Kidney beans", 
#     "Kumquat", "Kielbasa", "Kimchi", "Kombucha", "Lima beans", "Leeks", "Lentils", "Liver", 
#     "Lettuce", "Lasagna", "Lemons", "Limes", "Lobster", "Linguine", "Lemonade", "Lamb", 
#     "Legumes", "Licorice", "Lemongrass", "Mustard", "Macaroni", "Mushroom", "Milk", "Melon", 
#     "Muffin", "Marshmallows", "Mozzarella", "Mango", "Marmalade", "Mahi mahi", "Minestrone", 
#     "Margarine", "Maple syrup", "Mayonnaise", "Mashed potatoes", "Mackerel", "Miso", "Manicotti", 
#     "Mousse", "Meatloaf", "Millet", "Matcha", "Noodles", "Nuts", "Nachos", "Nectarines", 
#     "Chicken nuggets", "Naan bread", "Nori seaweed", "Nutella", "Onion", "Okra", "Orange", 
#     "Oatmeal", "Omelet", "Olives", "Oysters", "Octopus", "Oregano", "Oat milk", "Onion rings", 
#     "Oyster mushrooms", "Pasta", "Pickles", "Peas", "Potato", "Potato chips", "Parsley", 
#     "Pumpkin", "Peppers", "Parsnips", "Pork", "Popcorn", "Pistachios", "Pie", "Peanuts", 
#     "Pizza", "Pudding", "Peaches", "Pears", "Plum", "Prunes", "Pancake", "Pastry", "Pineapple", 
#     "Peppermint", "Papaya", "Pretzels", "Pecans", "Pepperoni", "Pine nuts", "Perogies", 
#     "Pimentos", "Pinto beans", "Paprika", "Parmesan cheese", "Prawns", "Potstickers", "Pizza", 
#     "Poutine", "Protein bars", "Passionfruit", "Plantain", "Pesto", "Peking duck", "Paella", 
#     "Pita bread", "Polenta", "Prosciutto", "Quiche", "Quail", "Quince", "Quesadilla", "Quinoa", 
#     "Rutabaga", "Rhubarb", "Radish", "Rice", "Ribs", "Rolls", "Rye bread", "Raspberry", 
#     "Ravioli", "Rigatoni", "Raisins", "Ratatouille", "Relish", "Romaine lettuce", "Red lentils", 
#     "Refried beans", "Risotto", "Ramen", "Radicchio", "Ricotta cheese", "Romano cheese", 
#     "Spinach", "Squash", "Soybean", "Steak", "Spaghetti", "Salad", "Swiss cheese", "Soup", 
#     "Sandwich", "Sausage", "Scallops", "Sushi", "Sauce", "Sundae", "Stuffing", "Strawberry", 
#     "Snow peas", "Salami", "Stew", "Salmon", "Sunflower seeds", "Swordfish", "Squid", 
#     "Sesame seeds", "Swiss chard", "Sour cream", "Sardines", "Salsa", "Tzatziki", "Souvlaki", 
#     "Sashimi", "Sesame oil", "Spinach dip", "Sweet potato", "Smoothie", "Samosa", "Snapper", 
#     "Split peas", "Scones", "Sorbet", "String cheese", "Souffle", "Sourdough bread", 
#     "Shish kabob", "Pasta shells", "Shepherd's pie", "Shrimp", "Sherbet", "Shallot", 
#     "Shredded wheat", "Shortbread", "Shortcake", "Shiitake mushrooms", "Tomato", "Turnip", 
#     "Turkey", "Tapioca", "Toast", "Taco", "Tuna", "Tortillas", "Tangerine", "Tabasco sauce", 
#     "Tamale", "Tater tots", "Tempura", "Tofu", "Tempeh", "Tortellini", "Tamarind", "Tabbouleh", 
#     "Teriyaki", "Torte", "Trifle", "Truffle", "Turmeric", "Tahini", "Thighs", 
#     "Thousand island dressing", "Thyme", "Upside-down cake", "Udon noodles", "Vegetables", 
#     "Venison", "Veal", "Vermicelli", "Vinegar", "Vanilla", "Vine leaves", "Vegetable soup", 
#     "Vinaigrette", "Watercress", "Wax beans", "Watermelon", "Wheat bread", "Chicken wings", 
#     "Waffles", "Walnuts", "Wafers", "Water", "Wontons", "Wasabi", "Wild rice", "Yam", 
#     "Yellow squash", "Yogurt", "Egg yolk", "Yellow beans", "Yucca", "Yuzu fruit", "Zucchini", 
#     "Ziti", "Zested lemon",
#     # --- Added Edamam Official Dish Types ---
#     "Biscuits and cookies", "Bread", "Cereals", "Condiments and sauces", "Desserts", 
#     "Drinks", "Egg", "Ice cream and custard", "Main course", "Pancake", "Pasta", 
#     "Pastry", "Pies and tarts", "Pizza", "Preps", "Preserve", "Salad", "Sandwiches", 
#     "Seafood", "Side dish", "Soup", "Special occasions", "Starter", "Sweets",

#     # --- Added Edamam Official Cuisine Types ---
#     "American", "Asian", "British", "Caribbean", "Central Europe", "Chinese", 
#     "Eastern Europe", "French", "Greek", "Indian", "Italian", "Japanese", 
#     "Korean", "Kosher", "Mediterranean", "Mexican", "Middle Eastern", "Nordic", 
#     "South American", "South East Asian", "World"
# ]


# final
final_food_list = [
    "Asparagus", "Apple", "Apricot", "Anchovies", "Applesauce", "Artichokes", "Almonds",
    "Angel hair pasta", "Acai berry", "Avocado", "Almond butter", "Alfredo sauce", "Beef",
    "Beans", "Broccoli", "Beets", "Barley", "Bacon", "Biscuits", "Bread", "Bagel", "Burger", "Butter",
    "Burrito", "Banana", "Blackberry", "Blueberry", "Basil", "Bok choy", "Broccolini","Baverages",
    "Brown rice", "Brioche", "Balsamic dressing", "Corn", "Carrots", "Cabbage", "Cauliflower",
    "Crab", "Cookies", "Cucumber", "Croutons", "Cantaloupe", "Clams",
    "Cashews", "Coconut", "Coffee", "Cod", "Caramel", "Cocoa", "Cream cheese",
    "Couscous", "Chickpeas", "Cereal", "Cider", "Celery", "Cinnamon",
    "Cilantro", "Ceviche", "Tortilla chips", "Cheese", "Cherry", "Chicken", "Chili",
    "Peanut butter", "Chocolate", "Cheddar cheese", "Chocolate chips",
    "Cheesecake", "Chutney", "Churros", "Chorizo", "Chia seeds", "Duck", "Donut",
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
    "Goat milk", "Gyoza", "Guava", "Gumbo", "Gouda cheese", "Gnocchi", "Ham",
    "Horseradish", "Hamburger", "Hot dog", "Honeydew melon", "Halibut",
    "Honey", "Hot chocolate", "Ketchup", "Hollandaise sauce", "Hummus",
    "Herbs", "Hash browns", "Ice cream", "Iced tea", "Icing",
    "Iceberg lettuce", "Italian bread", "Curry", "Irish stew",
    "Instant coffee", "Instant oatmeal", "Italian dressing", "Juice", "Jelly",
    "Jam", "Jerky", "Jalapeño", "Jambalaya", "Jasmine rice", "Jackfruit",
    "Jicama", "Kale", "Kiwi", "Kidney beans", "Kumquat", "Kielbasa", "Kimchi",
    "Kombucha", "Lima beans", "Leeks", "Lentils", "Liver", "Lettuce",
    "Lasagna", "Lemons", "Limes", "Lobster", "Linguine", "Lemonade", "Lamb",
    "Legumes", "Licorice", "Lemongrass", "Mustard", "Macaroni", "Mushroom",
    "Milk", "Melon", "Muffin", "Marshmallows", "Mozzarella", "Mango",
    "Marmalade", "Mahi mahi", "Minestrone", "Margarine", "Maple syrup",
    "Mayonnaise", "Mashed potatoes", "Mackerel", "Miso", "Manicotti",
    "Mousse", "Meatloaf", "Millet", "Matcha", "Noodles", "Nuts", "Nachos",
    "Nectarines", "Chicken nuggets", "Naan bread", "Nori seaweed", "Nutella",
    "Onion", "Okra", "Orange", "Oatmeal", "Omelet", "Olives", "Oysters",
    "Octopus", "Oregano", "Oat milk", "Onion rings", "Oyster mushrooms",
    "Pickles", "Peas", "Potato", "Potato chips", "Parsley", "Pumpkin",
    "Peppers", "Parsnips", "Pork", "Popcorn", "Pistachios", "Pie",
    "Peanuts", "Pudding", "Peaches", "Pears", "Plum", "Prunes",
    "Pancake", "Pastry", "Pineapple", "Peppermint", "Papaya",
    "Pretzels", "Pecans", "Pepperoni", "Pine nuts", "Perogies",
    "Pimentos", "Pinto beans", "Paprika", "Parmesan cheese",
    "Prawns", "Potstickers", "Poutine", "Protein bars", "Passionfruit",
    "Plantain", "Pesto", "Peking duck", "Paella", "Pita bread",
    "Polenta", "Prosciutto", "Quiche", "Quail", "Quince",
    "Quesadilla", "Quinoa", "Rutabaga", "Rhubarb", "Radish",
    "Ribs", "Rolls", "Rye bread", "Raspberry", "Ravioli",
    "Rigatoni", "Raisins", "Ratatouille", "Relish", "Romaine lettuce",
    "Red lentils", "Refried beans", "Risotto", "Ramen",
    "Radicchio", "Ricotta cheese", "Romano cheese", "Spinach",
    "Squash", "Soybean", "Steak", "Spaghetti", "Swiss cheese",
    "Sandwich", "Sausage", "Scallops", "Sushi", "Sauce",
    "Sundae", "Stuffing", "Strawberry", "Snow peas", "Salami",
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
    "Ziti", "Zested lemon",

    # Dish Types
    "Biscuits and cookies", "Cereals", "Condiments and sauces",
    "Desserts", "Drinks", "Egg", "Ice cream and custard",
    "Main course", "Pancake", "Pastry", "Pies and tarts",
    "Preps", "Preserve", "Seafood", "Side dish",
    "Special occasions", "Starter", "Sweets",

    # Cuisines
    "American", "Asian", "British", "Caribbean",
    "Central Europe", "Chinese", "Eastern Europe",
    "French", "Greek", "Indian", "Italian",
    "Japanese", "Korean", "Kosher", "Mediterranean",
    "Mexican", "Middle Eastern", "Nordic",
    "South American", "South East Asian", "World"
]


def check_food_items():
    options = webdriver.ChromeOptions()
    # Keep the browser open after running
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Tracking results
    successful_matches = []
    failed_matches = []
    
    # ⚠️ For demo safety, testing the first 10 items. Remove `[:10]` to test all 300+ items!
    test_items = final_food_list
    
    print(f"🚀 Starting validation check for {len(test_items)} food items...\n")
    
    try:
        for food in test_items:
            # Construct direct URL search
            encoded_food = food.replace(" ", "%20")
            search_url = f"https://www.edamam.com/results/recipes/?search={encoded_food}"
            
            driver.get(search_url)
            time.sleep(2) # Give the page adequate time to render dynamically
            
            # Edamam shows an error text container if no recipes match the keyword
            page_source = driver.page_source
            if "We couldn't find any matches" in page_source or "Double check your search" in page_source:
                print(f"❌ NOT FOUND: '{food}' returned no results.")
                failed_matches.append(food)
            else:
                print(f"✅ VERIFIED: '{food}' has active recipe matches.")
                successful_matches.append(food)
                
    except Exception as e:
        print(f"An error occurred mid-process: {e}")
        
    finally:
        # Final console breakdown report
        print("\n--- 📊 FINAL REPORT ---")
        print(f"Total Checked: {len(test_items)}")
        print(f"Valid Ingredients: {len(successful_matches)}")
        print(f"Failed Ingredients: {len(failed_matches)}")
        if failed_matches:
            print(f"Items to reconsider: {failed_matches}")
        print("-----------------------")

if __name__ == "__main__":
    check_food_items()