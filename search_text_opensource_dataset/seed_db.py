"""
seed_db.py
----------
Reads data_clean.csv and inserts all records into PostgreSQL.
Run once (or re-run safely -- it skips existing categories and truncates food_items).

Usage:
    python seed_db.py
"""

import asyncio
import os
import math
import sys
import pandas as pd

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert as pg_insert

# Force UTF-8 output on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from database import engine, init_db, AsyncSessionLocal
from models import Category, FoodItem

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(__file__)
CSV_PATH   = os.path.join(BASE_DIR, "C:\\Users\\Bitech-Office\\Downloads\\search_text_opensource_dataset\\data_clean.csv")
BATCH_SIZE = 2000          # rows per DB insert batch


# ── Helpers ───────────────────────────────────────────────────────────────────
def safe_float(val):
    """Return float or None for missing/invalid values."""
    try:
        f = float(val)
        return None if math.isnan(f) else round(f, 3)
    except (TypeError, ValueError):
        return None


def safe_str(val, maxlen=None):
    s = str(val).strip() if val and str(val).strip() not in ("", "nan") else None
    if s and maxlen:
        s = s[:maxlen]
    return s


# ── Main seeder ───────────────────────────────────────────────────────────────
async def seed():
    print("[*] Initialising database tables ...")
    await init_db()

    # ── Load CSV ──────────────────────────────────────────────────────────────
    print(f"[*] Loading CSV: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH, engine="python", on_bad_lines="skip")
    df = df.fillna("")
    print(f"[OK] Loaded {len(df):,} rows")

    # ── Build category set ────────────────────────────────────────────────────
    category_names = sorted(
        {str(n).strip() for n in df["category_name"].unique() if str(n).strip()}
    )
    print(f"[*] Found {len(category_names)} unique categories")

    async with AsyncSessionLocal() as session:
        # Upsert categories (insert ignore on conflict)
        for name in category_names:
            stmt = (
                pg_insert(Category)
                .values(name=name)
                .on_conflict_do_nothing(index_elements=["name"])
            )
            await session.execute(stmt)
        await session.commit()
        print("[OK] Categories upserted")

        # Build name → id map
        result = await session.execute(
            text("SELECT id, name FROM categories")
        )
        cat_map: dict[str, int] = {row.name: row.id for row in result}

        # ── Truncate food_items before re-seeding ─────────────────────────────
        print("[*] Truncating food_items ...")
        await session.execute(text("TRUNCATE TABLE food_items RESTART IDENTITY CASCADE"))
        await session.commit()

        # ── Insert food_items in batches ──────────────────────────────────────
        total = len(df)
        print(f"[*] Inserting {total:,} food items in batches of {BATCH_SIZE} ...")

        batch = []
        inserted = 0

        for _, row in df.iterrows():
            cat_name  = str(row.get("category_name", "")).strip()
            cat_id    = cat_map.get(cat_name)

            record = {
                "product_name": safe_str(row.get("product_name"), 512) or "Unknown",
                "category_id":  cat_id,
                "calories":     safe_float(row.get("energy-kcal_100g")),
                "protein":      safe_float(row.get("proteins_100g")),
                "carbs":        safe_float(row.get("carbohydrates_100g")),
                "fat":          safe_float(row.get("fat_100g")),
                "ingredients":  safe_str(row.get("ingredients_text")),
            }
            batch.append(record)

            if len(batch) >= BATCH_SIZE:
                await session.execute(pg_insert(FoodItem), batch)
                await session.commit()
                inserted += len(batch)
                print(f"    -> {inserted:,} / {total:,} inserted ...")
                batch = []

        # flush remaining
        if batch:
            await session.execute(pg_insert(FoodItem), batch)
            await session.commit()
            inserted += len(batch)

        print(f"[DONE] {inserted:,} food items stored in PostgreSQL.")


if __name__ == "__main__":
    asyncio.run(seed())
