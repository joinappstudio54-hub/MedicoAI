from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from db.database import Base


class Category(Base):
    __tablename__ = "categories"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(100), unique=True, nullable=False)  # e.g. "Pizza", "Beverages"
    # created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.timezone('Asia/Karachi', func.now()))
    # One category → many food items
    food_items = relationship("FoodItem", back_populates="category", lazy="selectin")


class FoodItem(Base):
    __tablename__ = "food_items"

    id           = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(200), nullable=False)
    category_id  = Column(Integer, ForeignKey("categories.id"), nullable=False)
    calories     = Column(String(50),  default="")
    protein      = Column(String(50),  default="")
    carbs        = Column(String(50),  default="")
    fat          = Column(String(50),  default="")
    ingredients  = Column(Text,        default="")
    image_hash   = Column(String(32),  nullable=True)   # MD5 for duplicate detection
    # created_at   = Column(DateTime(timezone=True), server_default=func.now())

    created_at   = Column(DateTime(timezone=True), server_default=func.timezone('Asia/Karachi', func.now())) 
    
    # Relation back to category
    category = relationship("Category", back_populates="food_items", lazy="selectin")

    @property
    def category_name(self) -> str:
        return self.category.name if self.category else ""
