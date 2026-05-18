from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import AsyncGenerator

from search_text_opensource_dataset.database import init_db, get_db
from search_text_opensource_dataset.models import Category, FoodItem

# ── Lifespan: create tables on startup ────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="🍽️ AI Food Search API", lifespan=lifespan)


# ── Serialisers ───────────────────────────────────────────────────────────────
def food_to_dict(item: FoodItem, category_name: str | None = None) -> dict:
    return {
        "id":           item.id,
        "product_name": item.product_name,
        "category_id":  item.category_id,
        "category":     category_name,
        "calories":     item.calories,
        "protein":      item.protein,
        "carbs":        item.carbs,
        "fat":          item.fat,
        "ingredients":  item.ingredients,
    }


def cat_to_dict(cat: Category) -> dict:
    return {"id": cat.id, "name": cat.name}


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
async def home():
    return {"message": "API is running 🚀"}


# ---------- Categories --------------------------------------------------------

@app.get("/categories")
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).order_by(Category.name))
    cats   = result.scalars().all()
    return {"success": True, "count": len(cats), "data": [cat_to_dict(c) for c in cats]}


@app.get("/categories/{category_id}")
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    cat = await db.get(Category, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found.")
    return {"success": True, "data": cat_to_dict(cat)}



# rewrote

# ---------- Food Items --------------------------------------------------------

@app.get("/foods")
async def get_all_food_items(
    limit: int = 50,
    skip:  int = 0,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(FoodItem, Category.name.label("category_name"))
        .join(Category, FoodItem.category_id == Category.id, isouter=True)
        .offset(skip)
        .limit(limit)
    )
    rows  = (await db.execute(stmt)).all()
    data  = [food_to_dict(item, cat_name) for item, cat_name in rows]
    return {"success": True, "count": len(data), "data": data}


@app.get("/foods/search")
async def search_food(
    q:     str = Query(..., min_length=2, description="Search term"),
    top_n: int = Query(10, ge=1, le=100),
    db:    AsyncSession = Depends(get_db),
):
    pattern = f"%{q.lower()}%"
    stmt = (
        select(FoodItem, Category.name.label("category_name"))
        .join(Category, FoodItem.category_id == Category.id, isouter=True)
        .where(
            or_(
                func.lower(FoodItem.product_name).like(pattern),
                func.lower(FoodItem.ingredients).like(pattern),
            )
        )
        .limit(top_n)
    )
    rows = (await db.execute(stmt)).all()
    data = [food_to_dict(item, cat_name) for item, cat_name in rows]
    return {"success": True, "count": len(data), "data": data}


@app.get("/foods/{food_id}")
async def get_food_by_id(food_id: int, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(FoodItem, Category.name.label("category_name"))
        .join(Category, FoodItem.category_id == Category.id, isouter=True)
        .where(FoodItem.id == food_id)
    )
    row = (await db.execute(stmt)).first()
    if not row:
        raise HTTPException(status_code=404, detail="Food item not found.")
    item, cat_name = row
    return {"success": True, "data": food_to_dict(item, cat_name)}


@app.get("/foods/category/{category_id}")
async def get_food_by_category(
    category_id: int,
    limit: int = 50,
    skip:  int  = 0,
    db: AsyncSession = Depends(get_db),
):
    # verify category exists
    cat = await db.get(Category, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found.")

    stmt = (
        select(FoodItem)
        .where(FoodItem.category_id == category_id)
        .offset(skip)
        .limit(limit)
    )
    items = (await db.execute(stmt)).scalars().all()
    data  = [food_to_dict(item, cat.name) for item in items]
    return {"success": True, "count": len(data), "data": data}