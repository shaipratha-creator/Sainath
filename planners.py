from fastapi import APIRouter, HTTPException

from models.schemas import HomeRequest
from app.models.schemas import BudgetRequest

from app.models.schemas import (
    HomeRequest,
    PartyRequest,
    JewelryRequest,
)

from app.gemini_utils import (
    generate_recommendations,
)


router = APIRouter(
    tags=["Planners"]
)


# --------------------------------------------------
# Home
# --------------------------------------------------

@router.post(
    "/generate-home"
)
async def generate_home(
    payload: HomeRequest
):

    return await generate_recommendations(
        "home",
        payload.model_dump()
    )


# --------------------------------------------------
# Party
# --------------------------------------------------

@router.post(
    "/generate-party"
)
async def generate_party(
    payload: PartyRequest
):

    return await generate_recommendations(
        "party",
        payload.model_dump()
    )


# --------------------------------------------------
# Jewelry
# --------------------------------------------------

@router.post(
    "/generate-jewelry"
)
async def generate_jewelry(
    payload: JewelryRequest
):

    return await generate_recommendations(
        "jewelry",
        payload.model_dump()
    )


# --------------------------------------------------
# Recommendation details
# --------------------------------------------------

@router.post(
    "/recommendations-details"
)
async def recommendations_details(
    payload: dict
):

    planner = str(
        payload.get(
            "planner",
            "home"
        )
    ).lower()

    if planner not in {
        "home",
        "party",
        "jewelry"
    }:

        raise HTTPException(
            status_code=400,
            detail=(
                "Planner must be "
                "home, party or jewelry."
            ),
        )

    return await generate_recommendations(
        planner,
        payload
    )


# --------------------------------------------------
# History
# --------------------------------------------------

@router.get("/history")
async def history():

    return {
        "history": [],
        "message":
            "History storage is not configured yet.",
    }