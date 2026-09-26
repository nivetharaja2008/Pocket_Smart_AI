import hashlib
import hmac
import os

from datetime import datetime, timedelta, timezone

import jwt

from .config import (
    SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """
    Securely hash a password using PBKDF2.
    """

    salt = os.urandom(16)

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        120_000
    )

    return (
        f"pbkdf2_sha256$120000$"
        f"{salt.hex()}$"
        f"{digest.hex()}"
    )


def verify_password(
    password: str,
    stored: str
) -> bool:

    try:

        (
            _,
            rounds,
            salt_hex,
            digest_hex
        ) = stored.split("$")

        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            bytes.fromhex(salt_hex),
            int(rounds)
        )

        return hmac.compare_digest(
            digest.hex(),
            digest_hex
        )

    except (
        ValueError,
        TypeError
    ):
        return False


def create_access_token(
    user_id: int,
    email: str
) -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(
    token: str
) -> dict:

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )