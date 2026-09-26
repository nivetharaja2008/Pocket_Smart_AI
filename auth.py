from fastapi import HTTPException, Request

from ..db import get_connection

from ..security import (
    create_access_token,
    decode_access_token,
    verify_password,
    hash_password
)


def register_user(
    name,
    email,
    password
):

    with get_connection() as connection:

        existing = connection.execute(
            """
            SELECT id
            FROM users
            WHERE email=?
            """,
            (email.lower(),)
        ).fetchone()

        if existing:

            raise HTTPException(
                status_code=409,
                detail=(
                    "An account with this "
                    "email already exists."
                )
            )

        cur = connection.execute(
            """
            INSERT INTO users(
                name,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                name.strip(),
                email.lower(),
                hash_password(password)
            )
        )

        return {
            "id": cur.lastrowid,
            "name": name.strip(),
            "email": email.lower()
        }


def authenticate(
    email,
    password
):

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM users
            WHERE email=?
            """,
            (email.lower(),)
        ).fetchone()

    if (
        not row
        or not verify_password(
            password,
            row["password_hash"]
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    return dict(row)


def current_user(
    request: Request
):

    uid = request.session.get(
        "user_id"
    )

    if not uid:
        return None

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT
                id,
                name,
                email,
                created_at
            FROM users
            WHERE id=?
            """,
            (uid,)
        ).fetchone()

    return dict(row) if row else None


def require_user(
    request: Request
):

    user = current_user(request)

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Please log in first."
        )

    return user


def user_from_bearer(
    request: Request
):

    auth = request.headers.get(
        "Authorization",
        ""
    )

    if not auth.startswith(
        "Bearer "
    ):
        return None

    try:

        payload = decode_access_token(
            auth[7:]
        )

        uid = int(
            payload["sub"]
        )

    except Exception:

        return None

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT
                id,
                name,
                email,
                created_at
            FROM users
            WHERE id=?
            """,
            (uid,)
        ).fetchone()

    return dict(row) if row else None


def login_session(
    request: Request,
    user
):

    request.session["user_id"] = user["id"]

    request.session["email"] = user["email"]

    return create_access_token(
        user["id"],
        user["email"]
    )