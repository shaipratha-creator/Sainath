from app.gemini_utils import (
    generate_recommendations
)


async def get_recommendations(
    planner: str,
    data: dict
) -> dict:


    return await generate_recommendations(
        planner,
        data
    )