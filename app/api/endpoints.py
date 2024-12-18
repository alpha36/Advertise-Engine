from fastapi import APIRouter
from app.models.request import RecommendBody

router = APIRouter()

@router.put("/advertise-recommendation")
def advertise_recommendation(request: RecommendBody):
     #ToDo de pus logica endpoint-ului