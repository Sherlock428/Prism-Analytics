from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import uuid4
from datetime import datetime
from decimal import Decimal
from enum import Enum
import hashlib
import secrets

class ImprovementCategory(Enum):
    Food_QUALITY = "food_quality"
    SERVICE_SPEED = "service_speed"
    STAFF_ATITUDE = "staff_atitude"
    CLEANLINESS = "cleanliness"
    PRICE = "price"
    LOCALE = "locale"
    OTHERS = "others"

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    full_name: str = Field(min_length=5, max_length=100)
    email: str = Field(unique=True, index=True)
    password: str = Field(min_length=6, max_length=100)
    is_active: bool = Field(default=True)
    at_created: datetime = Field(default_factory=datetime.utcnow)

    business: List["Business"] = Relationship(back_populates="owner")
    subscription: Optional["Subscription"] = Relationship(back_populates="user")

    def set_password(self, plain_password):
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256((plain_password + salt).encode('utf-8'))
        self.password = f"{salt}${hash_obj.hexdigest()}"

    def check_password(self, plain_password):
        try:
            salt, storage_hash = self.password.split("$")
            hash_obj = hashlib.sha256((plain_password + salt).encode('utf-8'))

            return hash_obj.hexdigest() == storage_hash
        except ValueError:
            return False
        
class Business(SQLModel, table=True):
    __tablename__ = "business"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=250)
    email: str
    logo_url: Optional[str] = None
    google_maps_links: Optional[str] = None
    qr_code_url: Optional[str] = None
    create_at: datetime = Field(default_factory=datetime.utcnow)

    owner_id: str = Field(foreign_key="users.id")

    owner: User = Relationship(back_populates="business")
    feedbacks: List["Feedback"] = Relationship(back_populates="business")

class Feedback(SQLModel, table=True):
    __tablename__ = "feedbacks"

    id: Optional[int] = Field(default=None, primary_key=True)
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None
    improvement_option: Optional[str] = None
    created_date: datetime = Field(default_factory=datetime.utcnow)

    business_id: int = Field(foreign_key="business.id")

    business: "Business" = Relationship(back_populates="feedbacks")

class FeedbackImprovement(SQLModel, table=True):
    feedback_id: int = Field(foreign_key="feedbacks.id")
    category: "ImprovementCategory" = Field(primary_key=True)
class Subscription(SQLModel, table=True):
    __tablename__ = "subscriptions"

    id: Optional[int] = Field(default=None, primary_key=True)
    plan: str = Field(max_length=100)
    price: Decimal
    is_active: bool
    start_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None

    user_id: str = Field(foreign_key="users.id", unique=True)

    user: User = Relationship(back_populates="subscription")