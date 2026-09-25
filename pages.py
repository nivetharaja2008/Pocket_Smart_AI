from pathlib import Path
from typing import Literal

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, Field


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# =========================
# PAGE ROUTES
# =========================

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={}
    )


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


@router.get("/planner/home")
async def home_planner(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="planner_name.html",
        context={}
    )


@router.get("/planner/party")
async def party_planner(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="planner_party.html",
        context={}
    )


@router.get("/planner/jewelry")
async def jewelry_planner(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="planner_jewelry.html",
        context={}
    )


# =========================
# USER REQUEST MODELS
# =========================

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


# =========================
# HOME PLANNER
# =========================

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


# =========================
# PARTY PLANNER
# =========================

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


# =========================
# JEWELRY PLANNER
# =========================

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


# =========================
# RECOMMENDATION DETAILS
# =========================

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