from typing import Literal

from pydantic import (
    BaseModel,
    EmailStr,
    Field
)


class UserCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=80
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=128
    )


class LoginRequest(BaseModel):

    email: EmailStr

    password: str = Field(
        min_length=1,
        max_length=128
    )


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0
    )

    rooms: list[str] = Field(
        min_length=1
    )

    quantities: dict[str, int] = Field(
        default_factory=dict
    )

    style: str = Field(
        default="modern",
        max_length=80
    )

    location: str = Field(
        default="India",
        max_length=120
    )


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0
    )

    guests: int = Field(
        gt=0,
        le=10000
    )

    event_type: str = Field(
        min_length=2,
        max_length=80
    )

    venue: str = Field(
        default="Home / flexible venue",
        max_length=200
    )

    theme: str = Field(
        default="Elegant",
        max_length=80
    )

    location: str = Field(
        default="India",
        max_length=120
    )


class JewelryRequest(BaseModel):

    budget: float = Field(
        gt=0
    )

    occasion: str = Field(
        min_length=2,
        max_length=80
    )

    style: str = Field(
        default="Elegant",
        max_length=80
    )

    outfit_color: str = Field(
        default="Not specified",
        max_length=80
    )

    outfit_description: str = Field(
        default="",
        max_length=500
    )


class RecommendationDetailsRequest(BaseModel):

    planner: Literal[
        "home",
        "party",
        "jewelry"
    ]

    category: str = Field(
        min_length=1,
        max_length=100
    )

    budget: float = Field(
        gt=0
    )