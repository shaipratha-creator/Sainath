from fastapi import (
    APIRouter,
    HTTPException,
)

from app.models.schemas import (
    RegisterRequest,
    LoginRequest,
)


router = APIRouter(
    tags=["Authentication"]
)


# Demo-only in-memory users
_users = {}


# --------------------------------------------------
# Register
# --------------------------------------------------

@router.post(
    "/register"
)
async def register(
    payload: RegisterRequest
):

    email = (
        payload.email
        .strip()
        .lower()
    )

    if email in _users:

        raise HTTPException(
            status_code=409,
            detail="Email is already registered.",
        )

    _users[email] = {

        "name":
            payload.name,

        "password":
            payload.password,
    }

    return {

        "message":
            "Registration successful.",

        "user": {

            "name":
                payload.name,

            "email":
                email,
        },
    }


# --------------------------------------------------
# Login
# --------------------------------------------------

@router.post(
    "/login"
)
async def login(
    payload: LoginRequest
):

    email = (
        payload.email
        .strip()
        .lower()
    )

    user = _users.get(email)

    if (
        not user
        or user["password"]
        != payload.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    return {

        "message":
            "Login successful.",

        "user": {

            "name":
                user["name"],

            "email":
                email,
        },
    }


# --------------------------------------------------
# Logout
# --------------------------------------------------

@router.post(
    "/logout"
)
async def logout():

    return {
        "message":
            "Logout successful."
    }


# --------------------------------------------------
# Token
# --------------------------------------------------

@router.post(
    "/token"
)
async def token(
    payload: LoginRequest
):

    email = (
        payload.email
        .strip()
        .lower()
    )

    user = _users.get(email)

    if (
        not user
        or user["password"]
        != payload.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials.",
        )

    return {

        "access_token":
            f"demo-token-{email}",

        "token_type":
            "bearer",
    }


# --------------------------------------------------
# Session info
# --------------------------------------------------

@router.get(
    "/session-info"
)
async def session_info():

    return {

        "logged_in":
            False,

        "message":
            "Demo session endpoint.",
    }


# --------------------------------------------------
# Session data
# --------------------------------------------------

@router.get(
    "/session-data"
)
async def session_data():

    return {

        "user":
            None,

        "data":
            [],
    }
