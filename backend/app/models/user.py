from sqlalchemy import Column, Integer, String, Enum
import enum
from app.database import Base


class UserRole(enum.Enum):
    guest = "guest"
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
