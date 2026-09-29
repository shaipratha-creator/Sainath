from typing import Optional

from pydantic import BaseModel, Field


# --------------------------------------------------
# Home Planner
# --------------------------------------------------

class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0
    )

    room_type: str = "Living Room"

    quantity: int = Field(
        default=1,
        ge=1
    )

    style: str = "Modern"

    requirements: Optional[str] = ""


# --------------------------------------------------
# Party Planner
# --------------------------------------------------

class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0
    )

    guests: int = Field(
        gt=0
    )

    event_type: str = "Birthday"

    venue: Optional[str] = ""

    requirements: Optional[str] = ""


# --------------------------------------------------
# Jewelry Planner
# --------------------------------------------------

class JewelryRequest(BaseModel):

    budget: float = Field(
        gt=0
    )

    occasion: str = "Wedding"

    style: str = "Traditional"

    outfit_color: Optional[str] = ""

    requirements: Optional[str] = ""


# --------------------------------------------------
# Register
# --------------------------------------------------

class RegisterRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: str

    password: str = Field(
        min_length=6,
        max_length=100
    )


# --------------------------------------------------
# Login
# --------------------------------------------------

class LoginRequest(BaseModel):

    email: str

    password: str