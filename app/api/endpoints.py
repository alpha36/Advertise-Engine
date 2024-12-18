from fastapi import APIRouter
from app.models.request import RecommendBody
from app.urlcategorizer.urlcategorizer import categorize

router = APIRouter()

@router.post("/advertise-recommendation")
def advertise_recommendation(request: RecommendBody):
    categorize(request.url)