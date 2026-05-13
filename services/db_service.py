from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from db.models import Category, FoodItem


# ── Category helpers ───────────────────────────────────────────────────────────

async def get_or_create_category(db: AsyncSession, name: str) -> Category:
    """Return existing category or create a new one (case-insensitive match)."""
    result = await db.execute(
        select(Category).where(func.lower(Category.name) == name.strip().lower())
    )
    category = result.scalars().first()

    if not category:
        category = Category(name=name.strip().title())
        db.add(category)
        await db.flush()   # get ID without committing

    return category


async def get_all_categories(db: AsyncSession) -> list[Category]:
    result = await db.execute(select(Category).order_by(Category.name))
    return result.scalars().all()


# ── FoodItem helpers ───────────────────────────────────────────────────────────

async def save_food_items(db: AsyncSession, items: list[dict], image_hash: str) -> list[FoodItem]:
    """
    Persist each Gemini-analysed food item.
    Resolves (or creates) the category row first, then inserts the food item.
    All writes happen in one transaction — caller must commit.
    """
    saved = []
    for item in items:
        category = await get_or_create_category(db, item.get("category", "Uncategorised"))

        food = FoodItem(
            product_name = item.get("product_name", ""),
            category_id  = category.id,
            calories     = item.get("calories", ""),
            protein      = item.get("protein",  ""),
            carbs        = item.get("carbs",    ""),
            fat          = item.get("fat",      ""),
            ingredients  = item.get("ingredients", ""),
            image_hash   = image_hash,
        )
        db.add(food)
        saved.append(food)

    await db.flush()   # populate IDs before returning
    return saved


async def get_all_food_items(db: AsyncSession) -> list[FoodItem]:
    result = await db.execute(
        select(FoodItem).order_by(FoodItem.created_at.desc())
    )
    return result.scalars().all()


async def get_food_by_id(db: AsyncSession, food_id: int) -> FoodItem | None:
    result = await db.execute(select(FoodItem).where(FoodItem.id == food_id))
    return result.scalars().first()


async def get_food_by_category_id(db: AsyncSession, category_id: int) -> list[FoodItem]:
    result = await db.execute(
        select(FoodItem)
        .where(FoodItem.category_id == category_id)
        .order_by(FoodItem.created_at.desc())
    )
    return result.scalars().all()


async def search_food(db: AsyncSession, query: str) -> list[FoodItem]:
    """Search by product name or ingredients (case-insensitive ILIKE)."""
    pattern = f"%{query.strip()}%"
    result = await db.execute(
        select(FoodItem)
        .where(
            or_(
                FoodItem.product_name.ilike(pattern),
                FoodItem.ingredients.ilike(pattern),
            )
        )
        .order_by(FoodItem.created_at.desc())
    )
    return result.scalars().all()
