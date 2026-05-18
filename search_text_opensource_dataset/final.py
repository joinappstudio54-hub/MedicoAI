import pandas as pd
import unicodedata
import re
import csv
import os

# ==============================
# CONFIG
# ==============================
BASE_DIR = os.path.dirname(__file__)

INPUT_FILE = os.path.join(
    BASE_DIR,
    "1stdata",
    "en.openfoodfacts.org.products.csv",
    "en.openfoodfacts.org.products.csv"
)

OUTPUT_FILE = "data_clean.csv"
CHUNK_SIZE = 100000

USE_COLUMNS = [
    'product_name',
    'generic_name',
    'categories_en',
    'ingredients_text',
    'energy-kcal_100g',
    'proteins_100g',
    'carbohydrates_100g',
    'fat_100g'
]

TEXT_COLUMNS = [
    'product_name',
    'generic_name',
    'categories_en',
    'ingredients_text'
]

NUMERIC_COLUMNS = [
    'energy-kcal_100g',
    'proteins_100g',
    'carbohydrates_100g',
    'fat_100g'
]

NON_FOOD_PATTERN = r"\b(?:shampoo|soap|cream|lotion|perfume|cosmetic|cleaner|detergent|toothpaste|gel|spray|dishwash|laundry|shaving|deodorant)\b"

TAXONOMY_MAP = {
      "Soups": r"\b(?:soup|soupe|potage|veloute|broth|bouillon|"
              r"chowder|bisque|consomme|minestrone|cream soup|puree soup)\b",
    "Supplements": r"\b(?:protein powder|protein bar|protein shake|whey|collagen|vitamin|supplement|bodybuilding)\b",
    "Sauces & Condiments": r"\b(?:sauce|ketchup|mayonnaise|mustard|vinegar|chutney|dressing|dip|marinade|gravy|paste|curry)\b",
    "Beverages": r"\b(?:drink|juice|tea|coffee|water|soda|cola|milkshake|smoothie|beer|wine|energy drink|sports drink)\b",
    "Sweets & Desserts": r"\b(?:cake|dessert|chocolate|cookie|ice cream|ice-cream|donut|brownie|sweet|candy|pastry|pudding|tart|muffin)\b",
    "Breakfast Foods": r"\b(?:oats|cereal|granola|jam|cornflakes|muesli|porridge|pancake|waffle|breakfast|bagel|toast)\b",
    "Snacks": r"\b(?:snack|chip|cracker|popcorn|biscuit|nachos|energy bar|granola bar|pretzel|jerky|trail mix)\b",
    "Fast Food": r"\b(?:pizza|burger|shawarma|kebab|sandwich|wrap|fries|hot dog|taco|burrito|ready meal|frozen meal|instant noodles|nugget|fast food)\b",
    "Grains & Carbs": r"\b(?:bread|rice|pasta|grain|wheat|noodle|flour|oats|noodles|cereal|tortilla|quinoa|barley|corn|mashed potato)\b",
    "Protein Foods": r"\b(?:meat|chicken|beef|fish|egg|lentil|tofu|pork|ham|bacon|turkey|sausage|beans|lentils|peas|seafood|salmon|tuna|shrimp|prawn)\b",
    "Dairy & Alternatives": r"\b(?:milk|cheese|yogurt|butter|cream|cottage cheese|ricotta|mozzarella|tofu|soy milk|almond milk|dairy|non-dairy)\b",
    "Fats & Oils": r"\b(?:oil|ghee|butter|margarine|lard|shortening|salad oil|cooking oil|olive oil)\b",
    "Fruits": r"\b(?:fruit|apple|banana|mango|orange|grape|berry|pear|melon|kiwi|pineapple|peach|apricot|cherry)\b",
    "Vegetables": r"\b(?:vegetable|tomato|potato|onion|carrot|broccoli|pepper|spinach|lettuce|cucumber|zucchini|eggplant|cabbage|cauliflower|celery)\b",
    "Restaurant Meals": r"\b(?:restaurant|takeaway|take-away|cafe|diner|bistro|pub|eatery|food court|restaurant-style|table service)\b",
    "Home-Cooked Meals": r"\b(?:homemade|home cooked|home-cooked|home style|home-style|from scratch|family meal|casserole|stew|soup|cooking at home)\b"
}

PRODUCT_CATEGORY_OVERRIDES = {
    "coca cola": "Beverages",
    "pepsi": "Beverages",
    "red bull": "Beverages",
    "nature valley": "Snacks",
    "granola bar": "Snacks",
    "protein bar": "Supplements",
    "whey protein": "Supplements",
    "chicken nuggets": "Protein Foods",
    "tomato ketchup": "Sauces & Condiments",
    "mayonnaise": "Sauces & Condiments",
    "spaghetti": "Grains & Carbs",
    "macaroni": "Grains & Carbs",
    "brown rice": "Grains & Carbs",
    "olive oil": "Fats & Oils",
    "almond milk": "Dairy & Alternatives",
    "soy milk": "Dairy & Alternatives",
    "cottage cheese": "Dairy & Alternatives",
    "frozen pizza": "Fast Food",
    "instant noodles": "Grains & Carbs",
    "energy drink": "Beverages",
    "sports drink": "Beverages",
    "ice cream": "Sweets & Desserts",
    "yogurt": "Dairy & Alternatives",
    "frozen meal": "Fast Food",
    "instant meal": "Fast Food",
    "chocolate bar": "Sweets & Desserts",
    "apple juice": "Beverages",
    "orange juice": "Beverages",
    "beer": "Beverages",
    "whiskey": "Beverages",
    "soup": "Soups",
}

PRINT_COLUMNS = [
    'product_name',
    'generic_name',
    'categories_en',
    'ingredients_text',
    'energy-kcal_100g',
    'proteins_100g',
    'carbohydrates_100g',
    'fat_100g',
    'category_name'
]

# ==============================
# HELPERS
# ==============================

def normalize_text(value):
    text = str(value).strip().lower()
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'\s+', ' ', text)
    return text


def is_english_text(value):
    text = str(value).strip().lower()
    if len(text) < 4:
        return False
    ascii_ratio = sum(1 for c in text if ord(c) < 128) / len(text)
    if ascii_ratio < 0.9:
        return False
    words = text.split()
    return any(word in words for word in ['chicken', 'beef', 'milk', 'bread', 'rice', 'juice', 'coffee', 'tea', 'sauce', 'cheese', 'butter', 'egg', 'fish', 'oil', 'cake', 'snack', 'fruit', 'vegetable', 'sugar', 'salt', 'protein', 'bar', 'noodle', 'pasta', 'water', 'drink', 'cereal', 'yogurt', 'meat', 'burger', 'pizza', 'fries', 'sandwich', 'chocolate', 'soup'])

print('🚀 Loading data in chunks...')

chunks = []
for chunk in pd.read_csv(
    INPUT_FILE,
    sep='\t',
    usecols=USE_COLUMNS,
    chunksize=CHUNK_SIZE,
    engine='python',
    on_bad_lines='skip',
    quoting=csv.QUOTE_NONE,
    encoding='utf-8',
    encoding_errors='ignore'
):
    chunks.append(chunk)

if not chunks:
    raise RuntimeError(f'No data loaded from {INPUT_FILE}')

df = pd.concat(chunks, ignore_index=True)
print('✅ Data loaded:', df.shape)

# ==============================
# TEXT NORMALIZATION
# ==============================
for col in TEXT_COLUMNS:
    if col not in df.columns:
        df[col] = ''
    df[col] = df[col].fillna('').apply(normalize_text)

# Drop rows with any empty text fields
text_mask = pd.DataFrame({
    col: df[col].astype(str).str.strip().replace({'': False}, regex=False).astype(bool)
    for col in TEXT_COLUMNS
})
df = df[text_mask.all(axis=1)]

# ==============================
# NUMERIC CLEANING
# ==============================
for col in NUMERIC_COLUMNS:
    df[col] = pd.to_numeric(df[col], errors='coerce')

print('➤ Numeric null counts:')
print(df[NUMERIC_COLUMNS].isna().sum())

df = df.dropna(subset=NUMERIC_COLUMNS)
df = df[(df['energy-kcal_100g'] > 0) &
        (df['proteins_100g'] >= 0) &
        (df['carbohydrates_100g'] >= 0) &
        (df['fat_100g'] >= 0)]

for col in NUMERIC_COLUMNS:
    df[col] = df[col].round(3)

print('✅ After numeric cleaning:', df.shape)

# ==============================
# TEXT AND DUPLICATE CLEANING
# ==============================
df = df[df['product_name'].str.len() > 3]
non_food_mask = df['product_name'].str.contains(NON_FOOD_PATTERN, na=False)
df = df[~non_food_mask]
print('✅ After non-food removal:', df.shape)

# Remove duplicates by product name + nutrition values
df['duplicate_key'] = (
    df['product_name'] + '|' +
    df['energy-kcal_100g'].astype(str) + '|' +
    df['proteins_100g'].astype(str) + '|' +
    df['carbohydrates_100g'].astype(str) + '|' +
    df['fat_100g'].astype(str)
)
df = df.drop_duplicates(subset=['duplicate_key'])
df = df.drop(columns=['duplicate_key'])
print('✅ After duplicate removal:', df.shape)

# ==============================
# ENGLISH FILTER
# ==============================
df['search_text'] = (
    df['product_name'] + ' ' +
    df['categories_en'] + ' ' +
    df['ingredients_text']
)

english_mask = df['search_text'].apply(is_english_text)
df = df[english_mask]
print('✅ After English filtering:', df.shape)

# ==============================
# CATEGORY ASSIGNMENT
# ==============================
df['category_name'] = ''
print('⚡ Assigning categories...')
combined_text = (
    df['product_name'] + ' ' +
    df['generic_name'].fillna('') + ' ' +
    df['categories_en'] + ' ' +
    df['ingredients_text']
)

for category, pattern in TAXONOMY_MAP.items():
    mask = df['categories_en'].str.contains(pattern, na=False)
    df.loc[(df['category_name'] == '') & mask, 'category_name'] = category

for category, pattern in TAXONOMY_MAP.items():
    mask = combined_text.str.contains(pattern, na=False)
    df.loc[(df['category_name'] == '') & mask, 'category_name'] = category

for phrase, category in PRODUCT_CATEGORY_OVERRIDES.items():
    mask = df['category_name'].eq('') & df['product_name'].str.contains(re.escape(phrase), na=False)
    df.loc[mask, 'category_name'] = category

# final fallback
df.loc[df['category_name'] == '', 'category_name'] = 'Other'

# Remove rows with empty text values
output_cols = ['product_name', 'generic_name', 'categories_en', 'ingredients_text', 'category_name']
for col in output_cols:
    df[col] = df[col].fillna('').astype(str).str.strip()
    df = df[~df[col].isin(['', 'unknown'])]

# Final production save
df = df[PRINT_COLUMNS]
df.to_csv(OUTPUT_FILE, index=False)
print(f'🎯 Cleaned dataset saved to: {OUTPUT_FILE}')
print('Final shape:', df.shape)
print('\nCategory distribution:')
print(df['category_name'].value_counts().to_string())