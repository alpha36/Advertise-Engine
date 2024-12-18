import random

from fastapi import APIRouter
from app.models.request import RecommendBody
from app.urlcategorizer.urlcategorizer import categorize
from app.models.db_schema import category_map

router = APIRouter()

@router.post("/advertise-recommendation")
def advertise_recommendation(request: RecommendBody):
    category = categorize(request.url)

    random_key = random.choice(list(category_map[category].keys()))
    random_value = category_map[category][random_key]

    return {
        "imageUrl": random_value,
        "linkUrl": request.url,
        "type": random_key
    }