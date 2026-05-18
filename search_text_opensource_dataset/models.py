from datetime import datetime, timezone
from sqlalchemy import (
    BigInteger, Integer, String, Float, Text,
    ForeignKey, DateTime, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from search_text_opensource_dataset.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # relationship back to food items
    food_items: Mapped[list["FoodItem"]] = relationship("FoodItem", back_populates="category")

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name!r}>"


class FoodItem(Base):
    __tablename__ = "food_items"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True
    )
    calories: Mapped[float | None] = mapped_column(Float, nullable=True)
    protein: Mapped[float | None] = mapped_column(Float, nullable=True)
    carbs: Mapped[float | None] = mapped_column(Float, nullable=True)
    fat: Mapped[float | None] = mapped_column(Float, nullable=True)
    ingredients: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # relationship
    category: Mapped["Category"] = relationship("Category", back_populates="food_items")

    def __repr__(self) -> str:
        return f"<FoodItem id={self.id} name={self.product_name!r}>"
