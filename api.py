import json

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile
)

from ..config import (
    MAX_UPLOAD_MB,
    UPLOAD_DIR,
    GEMINI_API_KEY
)

from ..db import get_connection

from ..models.schemas import (
    HomeRequest,
    PartyRequest,
    JewelryRequest,
    RecommendationDetailsRequest,
    UserCreate,
    LoginRequest
)

from ..security import create_access_token

from ..services.auth import (
    register_user,
    authenticate,
    current_user,
    require_user,
    user_from_bearer,
    login_session
)

from ..services.catalog import (
    search_catalog
)

from ..services.gemini_utils import (
    generate_home,
    generate_party,
    generate_jewelry
)


router = APIRouter()


def save_history(
    user_id,
    planner,
    request_obj,
    response_obj
):

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO recommendations(
                user_id,
                planner,
                request_json,
                response_json
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                planner,
                json.dumps(
                    request_obj,
                    default=str
                ),
                json.dumps(
                    response_obj,
                    default=str
                )
            )
        )


def api_user(request: Request):

    return (
        current_user(request)
        or user_from_bearer(request)
    )


@router.post("/register")
async def register(
    payload: UserCreate,
    request: Request
):

    user = register_user(
        payload.name,
        payload.email,
        payload.password
    )

    token = login_session(
        request,
        user
    )

    return {

        "message":
            "Registration successful",

        "user":
            user,

        "access_token":
            token
    }


@router.post("/login")
async def login(
    payload: LoginRequest,
    request: Request
):

    user = authenticate(
        payload.email,
        payload.password
    )

    token = login_session(
        request,
        user
    )

    return {

        "message":
            "Login successful",

        "user": {
            "id":
                user["id"],

            "name":
                user["name"],

            "email":
                user["email"]
        },

        "access_token":
            token
    }


@router.post("/logout")
async def logout(
    request: Request
):

    request.session.clear()

    return {
        "message":
            "Logged out"
    }


@router.post("/token")
async def token(
    payload: LoginRequest
):

    user = authenticate(
        payload.email,
        payload.password
    )

    return {

        "access_token":
            create_access_token(
                user["id"],
                user["email"]
            ),

        "token_type":
            "bearer"
    }


@router.get("/session-info")
async def session_info(
    request: Request
):

    user = api_user(request)

    return {

        "logged_in":
            bool(user),

        "user":
            user
    }


@router.get("/session-data")
async def session_data(
    request: Request
):

    user = require_user(
        request
    )

    with get_conn() as conn:

        row = conn.execute(
            """
            SELECT COUNT(*) AS total
            FROM recommendations
            WHERE user_id=?
            """,
            (user["id"],)
        ).fetchone()

    return {

        "user":
            user,

        "recommendation_count":
            row["total"],

        "session_keys":
            list(
                request.session.keys()
            )
    }


@router.get("/history")
async def history(
    request: Request
):

    user = require_user(
        request
    )

    with get_conn() as conn:

        rows = conn.execute(
            """
            SELECT
                id,
                planner,
                request_json,
                response_json,
                created_at

            FROM recommendations

            WHERE user_id=?

            ORDER BY id DESC

            LIMIT 50
            """,
            (user["id"],)
        ).fetchall()

    result = []

    for row in rows:

        result.append({

            "id":
                row["id"],

            "planner":
                row["planner"],

            "request":
                json.loads(
                    row["request_json"]
                ),

            "response":
                json.loads(
                    row["response_json"]
                ),

            "created_at":
                row["created_at"]
        })

    return result


@router.post("/generate-home")
async def generate_home_api(
    payload: HomeRequest,
    request: Request
):

    result = generate_home(
        payload
    )

    user = api_user(
        request
    )

    if user:

        save_history(
            user["id"],
            "home",
            payload.model_dump(),
            result
        )

    return result


@router.post("/generate-party")
async def generate_party_api(
    payload: PartyRequest,
    request: Request
):

    result = generate_party(
        payload
    )

    user = api_user(
        request
    )

    if user:

        save_history(
            user["id"],
            "party",
            payload.model_dump(),
            result
        )

    return result


@router.post("/generate-jewelry")
async def generate_jewelry_api(
    request: Request,

    budget: float = Form(...),

    occasion: str = Form(...),

    style: str = Form("Elegant"),

    outfit_color: str = Form(
        "Not specified"
    ),

    outfit_description: str = Form(""),

    outfit_image: UploadFile | None = File(
        None
    )
):

    if budget <= 0:

        raise HTTPException(
            status_code=422,
            detail=(
                "Budget must be "
                "greater than zero."
            )
        )

    image_bytes = None

    mime = None

    if (
        outfit_image
        and outfit_image.filename
    ):

        if (
            not outfit_image.content_type
            or not outfit_image.content_type.startswith(
                "image/"
            )
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only image files "
                    "are allowed."
                )
            )

        image_bytes = (
            await outfit_image.read()
        )

        if len(image_bytes) > (
            MAX_UPLOAD_MB * 1024 * 1024
        ):

            raise HTTPException(
                status_code=413,
                detail=(
                    f"Image must be "
                    f"smaller than "
                    f"{MAX_UPLOAD_MB} MB."
                )
            )

        mime = outfit_image.content_type

    payload = JewelryRequest(
        budget=budget,
        occasion=occasion,
        style=style,
        outfit_color=outfit_color,
        outfit_description=outfit_description
    )

    result = generate_jewelry(
        payload,
        image_bytes,
        mime
    )

    user = api_user(
        request
    )

    if user:

        save_history(
            user["id"],
            "jewelry",
            payload.model_dump(),
            result
        )

    return result


@router.post(
    "/recommendations-details"
)
async def recommendation_details(
    payload: RecommendationDetailsRequest,
    request: Request
):

    require_user(
        request
    )

    items = search_catalog(
        [payload.category],
        payload.budget,
        10
    )

    return {

        "planner":
            payload.planner,

        "category":
            payload.category,

        "recommendations":
            items
    }


@router.get("/startup")
async def startup_status():

    return {

        "status":
            "ready",

        "gemini_configured":
            bool(GEMINI_API_KEY)
    }


@router.get("/health")
async def health():

    return {
        "status":
            "ok"
    }